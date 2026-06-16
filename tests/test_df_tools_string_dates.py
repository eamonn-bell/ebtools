import pandas as pd
import pytest

from ebtools.general.df_tools_string_dates import (
    day_of_the_year_number,
    week_number,
    week_starting,
    weekday_number,
)


def test_week_number_returns_iso_week_for_string_date():
    assert week_number("2024-01-01") == 1


def test_week_number_handles_iso_year_boundary():
    assert week_number("2024-12-31") == 1


def test_week_number_accepts_timestamp():
    assert week_number(pd.Timestamp("2024-06-15")) == 24


def test_weekday_number_returns_monday_zero():
    assert weekday_number("2024-01-01") == 0


def test_weekday_number_returns_sunday_six():
    assert weekday_number("2024-01-07") == 6


def test_day_of_the_year_number_returns_first_day():
    assert day_of_the_year_number("2024-01-01") == 1


def test_day_of_the_year_number_handles_leap_year():
    assert day_of_the_year_number("2024-12-31") == 366


def test_day_of_the_year_number_handles_non_leap_year():
    assert day_of_the_year_number("2023-12-31") == 365


def test_week_starting_returns_default_monday_string():
    df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=14, freq="D")})

    result = week_starting(df, week=1, year=2024)

    assert result == "01 January 2024"


def test_week_starting_returns_selected_weekday_string():
    df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=14, freq="D")})

    result = week_starting(df, week=1, year=2024, weekday="Wed")

    assert result == "03 January 2024"


def test_week_starting_uses_custom_return_format():
    df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=14, freq="D")})

    result = week_starting(df, week=1, year=2024, return_format="%Y-%m-%d")

    assert result == "2024-01-01"


def test_week_starting_does_not_mutate_input_dataframe():
    df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=14, freq="D")})
    original = df.copy(deep=True)

    week_starting(df, week=1, year=2024)

    pd.testing.assert_frame_equal(df, original)


def test_week_starting_rejects_invalid_weekday_key():
    df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=14, freq="D")})

    with pytest.raises(KeyError):
        week_starting(df, week=1, year=2024, weekday="Monday")


def test_week_starting_rejects_no_matching_date():
    df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=7, freq="D")})

    with pytest.raises(IndexError):
        week_starting(df, week=3, year=2024)


def test_week_starting_requires_datetime_like_column():
    df = pd.DataFrame({"Date": ["2024-01-01"]})

    with pytest.raises(AttributeError, match=".dt accessor"):
        week_starting(df, week=1, year=2024)
