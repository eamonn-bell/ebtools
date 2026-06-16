import numpy as np
import pandas as pd
import pytest

from ebtools.general.dataframe_selection import select_days, select_weeks, select_year


def _long_sp_dataframe() -> pd.DataFrame:
    rows = []
    iso_week_one_monday = {
        2023: "2023-01-02",
        2024: "2024-01-01",
    }

    for year, start_date in iso_week_one_monday.items():
        for date in pd.date_range(start_date, periods=7, freq="D"):
            for sp in [1, 2]:
                rows.append(
                    {
                        "Date": date,
                        "SP": sp,
                        "TD": year + sp,
                        "Year": year,
                        "Week": date.isocalendar().week,
                        "Day": date.dayofweek,
                    }
                )

    return pd.DataFrame(rows)


def test_select_year_without_full_year_returns_matching_year_rows():
    index = pd.date_range("2023-12-30", "2025-01-02", freq="D")
    df = pd.DataFrame({"value": range(len(index))}, index=index)

    result = select_year(df, year=2024, full_year=False)

    assert result.index.min() == pd.Timestamp("2024-01-01")
    assert result.index.max() == pd.Timestamp("2024-12-31")
    assert len(result) == 366


def test_select_year_with_full_year_reindexes_to_complete_leap_year():
    df = pd.DataFrame(
        {"value": [1, 2]},
        index=pd.to_datetime(["2024-01-03", "2024-12-30"]),
    )

    result = select_year(df, year=2024, full_year=True)

    assert result.index.min() == pd.Timestamp("2024-01-01")
    assert result.index.max() == pd.Timestamp("2024-12-31")
    assert len(result) == 366
    assert pd.isna(result.loc["2024-01-01", "value"])


def test_select_year_can_add_buffer_to_full_year_index():
    df = pd.DataFrame(
        {"value": [1]},
        index=pd.to_datetime(["2024-01-01"]),
    )

    result = select_year(
        df,
        year=2024,
        full_year=True,
        add_buffer=True,
        buffer_days=2,
    )

    assert result.index.min() == pd.Timestamp("2023-12-30")
    assert result.index.max() == pd.Timestamp("2025-01-02")
    assert result.loc["2024-01-01", "value"] == 1


def test_select_year_can_reindex_efa_periods():
    df = pd.DataFrame(
        {"value": [1]},
        index=pd.to_datetime(["2023-12-31 23:00:00"]),
    )

    result = select_year(df, year=2024, full_year=True, period="efa")

    assert result.index.min() == pd.Timestamp("2023-12-31 23:00:00")
    assert result.index[1] == pd.Timestamp("2024-01-01 03:00:00")


def test_select_year_rejects_invalid_period_when_reindexing():
    df = pd.DataFrame(
        {"value": [1]},
        index=pd.to_datetime(["2024-01-01"]),
    )

    with pytest.raises(ValueError, match="period must be"):
        select_year(df, year=2024, full_year=True, period="month")


def test_select_weeks_pivots_selected_week_by_year():
    df = _long_sp_dataframe()

    result = select_weeks(
        df,
        week=1,
        value_col="TD",
        average_col=False,
        make_week_full=False,
    )

    assert result.columns.to_list() == [2023, 2024]
    assert result.index.names == ["Week", "Day", "SP"]
    assert result.loc[(1, 0, 1), 2023] == 2024
    assert result.loc[(1, 0, 1), 2024] == 2025


def test_select_weeks_can_add_average_column():
    df = _long_sp_dataframe()

    result = select_weeks(
        df,
        week=1,
        value_col="TD",
        average_col=True,
        average_all=True,
        average_type="float",
        make_week_full=False,
    )

    assert "Average" in result.columns
    assert result.loc[(1, 0, 1), "Average"] == np.mean([2024, 2025])


def test_select_weeks_replaces_zero_with_nan():
    df = _long_sp_dataframe()
    df.loc[0, "TD"] = 0

    result = select_weeks(
        df,
        week=1,
        value_col="TD",
        average_col=False,
        make_week_full=False,
    )

    assert pd.isna(result.loc[(1, 0, 1), 2023])


def test_select_weeks_can_replace_zero_with_custom_value():
    df = _long_sp_dataframe()
    df.loc[0, "TD"] = 0

    result = select_weeks(
        df,
        week=1,
        value_col="TD",
        average_col=False,
        make_week_full=False,
        replace_zero=-1,
    )

    assert result.loc[(1, 0, 1), 2023] == -1


def test_select_weeks_adds_missing_calendar_columns():
    df = _long_sp_dataframe().drop(columns=["Year", "Week", "Day"])

    result = select_weeks(
        df,
        week=1,
        value_col="TD",
        average_col=False,
        make_week_full=False,
    )

    assert result.columns.to_list() == [2023, 2024]
    assert result.loc[(1, 0, 1), 2023] == 2024


def test_select_weeks_supports_custom_periods_per_day_for_full_week():
    df = _long_sp_dataframe()

    result = select_weeks(
        df,
        week=1,
        value_col="TD",
        average_col=False,
        make_week_full=True,
        periods_per_day=2,
    )

    assert len(result) == 14


def test_select_weeks_rejects_invalid_average_type():
    df = _long_sp_dataframe()

    with pytest.raises(ValueError, match="average_type"):
        select_weeks(
            df,
            week=1,
            value_col="TD",
            average_type="decimal",
            make_week_full=False,
        )


def test_select_days_returns_matching_weekday_across_years():
    df = _long_sp_dataframe()

    result = select_days(
        df,
        date="2024-01-03",
        value_col="TD",
        average_col=False,
    )

    assert set(result.index.get_level_values("Day")) == {2}


def test_select_days_supports_custom_columns_and_replacement():
    df = _long_sp_dataframe().rename(
        columns={
            "Date": "Settlement Date",
            "SP": "Period",
            "TD": "Demand",
        }
    )
    df.loc[4, "Demand"] = 0

    result = select_days(
        df,
        date="2024-01-03",
        date_col="Settlement Date",
        sp_col="Period",
        value_col="Demand",
        average_col=False,
        replace_zero=-1,
    )

    assert result.index.names == ["Week", "Day", "Period"]
    assert set(result.index.get_level_values("Day")) == {2}
    assert result.loc[(1, 2, 1), 2023] == -1
