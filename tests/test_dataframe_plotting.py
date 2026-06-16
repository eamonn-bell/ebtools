import numpy as np
import pandas as pd
import pytest

from ebtools.general.dataframe_plotting import (
    _calendar_month_holder,
    _calendar_week_holder,
    _normalise_month_weeks,
    _normalise_year_weeks,
    _prepare_calendar_data,
    make_full_plotting_df,
    make_full_year_pivot,
    make_pivot_calendar,
)


def test_make_full_year_pivot_fills_missing_dates():
    df = pd.DataFrame(
        {"value": [1, 2]},
        index=pd.to_datetime(["2024-01-03", "2024-12-30"]),
    )

    result = make_full_year_pivot(df)

    assert result.index.min() == pd.Timestamp("2024-01-01")
    assert result.index.max() == pd.Timestamp("2024-12-31")
    assert len(result) == 366
    assert pd.isna(result.loc["2024-01-01", "value"])


def test_make_full_year_pivot_preserves_partial_range_when_fill_disabled():
    df = pd.DataFrame(
        {"value": [1, 2]},
        index=pd.to_datetime(["2024-01-03", "2024-01-05"]),
    )

    result = make_full_year_pivot(df, start_fill=False, end_fill=False)

    assert result.index.min() == pd.Timestamp("2024-01-03")
    assert result.index.max() == pd.Timestamp("2024-01-05")


def test_make_full_year_pivot_rejects_invalid_period():
    df = pd.DataFrame({"value": [1]}, index=pd.to_datetime(["2024-01-01"]))

    with pytest.raises(ValueError, match="period must be"):
        make_full_year_pivot(df, period="month")


def test_make_full_plotting_df_selects_month_from_full_year():
    index = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    df = pd.DataFrame({"value": range(len(index))}, index=index)

    result = make_full_plotting_df(df, year=2024, month=2, calendar_year=True)

    assert result.index.min() == pd.Timestamp("2024-02-01")
    assert result.index.max() == pd.Timestamp("2024-02-29")


def test_make_full_plotting_df_without_year_uses_partial_range_by_default():
    df = pd.DataFrame(
        {"value": [1, 2]},
        index=pd.to_datetime(["2024-01-03", "2024-01-05"]),
    )

    result = make_full_plotting_df(df)

    assert result.index.min() == pd.Timestamp("2024-01-03")
    assert result.index.max() == pd.Timestamp("2024-01-05")


def test_make_full_plotting_df_without_year_can_fill_calendar_year():
    df = pd.DataFrame(
        {"value": [1]},
        index=pd.to_datetime(["2024-01-03"]),
    )

    result = make_full_plotting_df(df, calendar_year=True)

    assert result.index.min() == pd.Timestamp("2024-01-01")
    assert result.index.max() == pd.Timestamp("2024-12-31")


def test_calendar_month_holder_returns_six_week_layout():
    result = _calendar_month_holder(unit_value=2)

    assert result.columns.to_list() == ["SP", "Weekday", "Week"]
    assert len(result) == 2 * 7 * 6
    assert result["SP"].head(4).to_list() == [1, 2, 1, 2]
    assert result["Weekday"].head(4).to_list() == [0, 0, 1, 1]
    assert result["Week"].iloc[-1] == 5


def test_calendar_week_holder_returns_one_week_layout():
    result = _calendar_week_holder(unit_value=2)

    assert result.columns.to_list() == ["SP", "Weekday"]
    assert len(result) == 2 * 7
    assert result["SP"].head(4).to_list() == [1, 2, 1, 2]
    assert result["Weekday"].head(4).to_list() == [0, 0, 1, 1]


def test_prepare_calendar_data_melts_selected_year():
    df = pd.DataFrame(
        {1: [10], 2: [20]},
        index=pd.to_datetime(["2024-01-01"]),
    )

    result = _prepare_calendar_data(df, year=2024, full_year=False)

    assert result.columns.to_list() == ["SP", "value", "Weekday", "Week"]
    assert result["SP"].to_list() == [1, 2]
    assert result["value"].to_list() == [10, 20]
    assert result["Weekday"].to_list() == [0, 0]


def test_normalise_month_weeks_rebases_first_week_to_zero():
    df = pd.DataFrame({"Week": [5, 5, 6]})

    result = _normalise_month_weeks(df, month=2)

    assert result["Week"].to_list() == [0, 0, 1]


def test_normalise_month_weeks_corrects_january_prior_year_week():
    df = pd.DataFrame({"Week": [52, 1, 1]})

    result = _normalise_month_weeks(df, month=1)

    assert result["Week"].to_list() == [0, 1, 1]


def test_normalise_year_weeks_sets_january_prior_year_week_to_zero():
    df = pd.DataFrame(
        {"Week": [52, 1]},
        index=pd.to_datetime(["2024-01-01", "2024-01-08"]),
    )

    result = _normalise_year_weeks(df)

    assert result["Week"].to_list() == [0, 1]


def test_normalise_year_weeks_moves_december_next_year_week_to_end():
    df = pd.DataFrame(
        {"Week": [52, 1]},
        index=pd.to_datetime(["2024-12-23", "2024-12-31"]),
    )

    result = _normalise_year_weeks(df)

    assert result["Week"].to_list() == [52, 53]


def test_make_pivot_calendar_returns_month_layout():
    index = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    df = pd.DataFrame(
        np.arange(len(index) * 48).reshape(len(index), 48),
        index=index,
        columns=range(1, 49),
    )

    result = make_pivot_calendar(df, year=2024, form="month", unit="hh")

    assert result.columns.to_list() == list(range(1, 13))
    assert len(result) == 48 * 7 * 6


def test_make_pivot_calendar_returns_week_layout():
    index = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    df = pd.DataFrame(
        np.arange(len(index) * 48).reshape(len(index), 48),
        index=index,
        columns=range(1, 49),
    )

    result = make_pivot_calendar(df, year=2024, form="week", unit="hh")

    assert 0 in result.columns
    assert len(result) == 48 * 7


def test_make_pivot_calendar_rejects_invalid_form():
    index = pd.date_range("2024-01-01", "2024-01-07", freq="D")
    df = pd.DataFrame(
        np.arange(len(index) * 48).reshape(len(index), 48),
        index=index,
        columns=range(1, 49),
    )

    with pytest.raises(ValueError, match="form must be"):
        make_pivot_calendar(df, year=2024, form="day", unit="hh")


def test_make_pivot_calendar_rejects_invalid_unit():
    index = pd.date_range("2024-01-01", "2024-01-07", freq="D")
    df = pd.DataFrame(
        np.arange(len(index) * 48).reshape(len(index), 48),
        index=index,
        columns=range(1, 49),
    )

    with pytest.raises(KeyError):
        make_pivot_calendar(df, year=2024, form="week", unit="bad")
