import pandas as pd
import pytest

from ebtools.general.datetime_dataframe import (
    add_first_of_month_col_from_date_col,
    add_first_of_month_col_from_int_cols,
    convert_datetime_sp_end,
    convert_datetime_sp_start,
)


def test_convert_datetime_sp_start_adds_start_column():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2023-01-13 14:35:00",
                    "2024-03-14 20:00:00",
                    "2024-03-14 23:59:00",
                ]
            ),
            "value": [1, 2, 3],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(
            [
                "2023-01-13 14:30:00",
                "2024-03-14 20:00:00",
                "2024-03-14 23:30:00",
            ]
        ),
        name="SP_start_datetime",
    )

    result = convert_datetime_sp_start(df, colname="Date")

    pd.testing.assert_series_equal(result["SP_start_datetime"], expected)
    pd.testing.assert_frame_equal(df, original)
    assert "SP_start_datetime" not in df.columns


def test_convert_datetime_sp_start_accepts_string_datetimes():
    df = pd.DataFrame({"Date": ["2024-03-14 14:35:00"]})

    result = convert_datetime_sp_start(df, colname="Date")

    assert result.loc[0, "SP_start_datetime"] == pd.Timestamp("2024-03-14 14:30:00")


def test_convert_datetime_sp_start_rejects_missing_column():
    df = pd.DataFrame({"Date": ["2024-03-14 14:35:00"]})

    with pytest.raises(KeyError):
        convert_datetime_sp_start(df, colname="missing")


def test_convert_datetime_sp_end_adds_end_column():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                [
                    "2023-01-13 14:35:00",
                    "2024-03-14 20:00:00",
                    "2024-03-14 23:59:00",
                ]
            ),
            "value": [1, 2, 3],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(
            [
                "2023-01-13 15:00:00",
                "2024-03-14 20:30:00",
                "2024-03-15 00:00:00",
            ]
        ),
        name="SP_end_datetime",
    )

    result = convert_datetime_sp_end(df, colname="Date")

    pd.testing.assert_series_equal(result["SP_end_datetime"], expected)
    pd.testing.assert_frame_equal(df, original)
    assert "SP_end_datetime" not in df.columns


def test_convert_datetime_sp_end_accepts_string_datetimes():
    df = pd.DataFrame({"Date": ["2024-03-14 23:59:00"]})

    result = convert_datetime_sp_end(df, colname="Date")

    assert result.loc[0, "SP_end_datetime"] == pd.Timestamp("2024-03-15 00:00:00")


def test_convert_datetime_sp_end_rejects_missing_column():
    df = pd.DataFrame({"Date": ["2024-03-14 14:35:00"]})

    with pytest.raises(KeyError):
        convert_datetime_sp_end(df, colname="missing")


def test_add_first_of_month_col_from_date_col_adds_month_start_column():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-02-15", "2023-12-31"]),
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2024-02-01", "2023-12-01"]),
        name="Date_Month",
    )

    result = add_first_of_month_col_from_date_col(df, date_col="Date")

    pd.testing.assert_frame_equal(df, original)
    assert result.columns.to_list() == ["Date", "value", "Date_Month"]
    pd.testing.assert_series_equal(result["Date_Month"], expected)


def test_add_first_of_month_col_from_date_col_uses_custom_output_name():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-02-15", "2023-12-31"]),
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2024-02-01", "2023-12-01"]),
        name="Month_Start",
    )

    result = add_first_of_month_col_from_date_col(
        df,
        date_col="Date",
        date_month_col_name="Month_Start",
    )

    pd.testing.assert_frame_equal(df, original)
    assert "Month_Start" not in df.columns
    pd.testing.assert_series_equal(result["Month_Start"], expected)


def test_add_first_of_month_col_from_date_col_accepts_string_dates():
    df = pd.DataFrame({"Date": ["2024-02-15", "2023-12-31"]})
    expected = pd.Series(
        pd.to_datetime(["2024-02-01", "2023-12-01"]),
        name="Date_Month",
    )

    result = add_first_of_month_col_from_date_col(df, date_col="Date")

    pd.testing.assert_series_equal(result["Date_Month"], expected)


def test_add_first_of_month_col_from_date_col_rejects_missing_column():
    df = pd.DataFrame({"Date": ["2024-02-15"]})

    with pytest.raises(KeyError):
        add_first_of_month_col_from_date_col(df, date_col="missing")


def test_add_first_of_month_col_from_int_cols_with_year_and_month():
    df = pd.DataFrame(
        {
            "Year": [2024, 2023],
            "Month": [2, 12],
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2024-02-01", "2023-12-01"]),
        name="Date_Month",
    )

    result = add_first_of_month_col_from_int_cols(
        df,
        year_col="Year",
        month_col="Month",
    )

    pd.testing.assert_frame_equal(df, original)
    assert "Date_Month" not in df.columns
    pd.testing.assert_series_equal(result["Date_Month"], expected)


def test_add_first_of_month_col_from_int_cols_with_year_month_and_day():
    df = pd.DataFrame(
        {
            "Year": [2024, 2023],
            "Month": [2, 12],
            "Day": [15, 31],
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2024-02-15", "2023-12-31"]),
        name="Date_Month",
    )

    result = add_first_of_month_col_from_int_cols(
        df,
        year_col="Year",
        month_col="Month",
        day_col="Day",
    )

    pd.testing.assert_frame_equal(df, original)
    assert "Date_Month" not in df.columns
    pd.testing.assert_series_equal(result["Date_Month"], expected)


def test_add_first_of_month_col_from_int_cols_uses_custom_output_name():
    df = pd.DataFrame(
        {
            "yr": [2024, 2023],
            "mo": [2, 12],
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2024-02-01", "2023-12-01"]),
        name="Month_Start",
    )

    result = add_first_of_month_col_from_int_cols(
        df,
        year_col="yr",
        month_col="mo",
        date_month_col_name="Month_Start",
    )

    pd.testing.assert_frame_equal(df, original)
    assert "Month_Start" not in df.columns
    pd.testing.assert_series_equal(result["Month_Start"], expected)


def test_add_first_of_month_col_from_int_cols_rejects_missing_column():
    df = pd.DataFrame({"Year": [2024], "value": [1]})

    with pytest.raises(KeyError):
        add_first_of_month_col_from_int_cols(
            df,
            year_col="Year",
            month_col="Month",
        )
