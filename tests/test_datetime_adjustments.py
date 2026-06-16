import pandas as pd
import pytest

from ebtools.general.datetime_adjustments import (
    roll_back_by_month_df,
    roll_back_by_month_str,
    start_of_delivery_year,
)


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-01-01", "2023-04-01"),
        ("2024-03-31", "2023-04-01"),
        ("2024-04-01", "2024-04-01"),
        (pd.Timestamp("2024-12-31"), "2024-04-01"),
    ],
)
def test_start_of_delivery_year_returns_april_boundary(date, expected):
    assert start_of_delivery_year(date) == pd.Timestamp(expected)


@pytest.mark.parametrize(
    "date, n_months, expected",
    [
        ("2022-10-23", 6, "2022-04-23"),
        ("2022-01-15", 2, "2021-11-15"),
        ("2024-03-31", 1, "2024-02-29"),
        ("2023-03-31", 1, "2023-02-28"),
    ],
)
def test_roll_back_by_month_str_as_string(date, n_months, expected):
    assert roll_back_by_month_str(date, n_months=n_months) == expected


def test_roll_back_by_month_str_as_timestamp():
    result = roll_back_by_month_str(
        "2024-03-31",
        n_months=1,
        as_string=False,
    )

    assert result == pd.Timestamp("2024-02-29")


def test_roll_back_by_month_df_updates_column():
    df = pd.DataFrame(
        {
            "date": ["2022-10-23", "2024-03-31", "2023-03-31"],
            "value": [1, 2, 3],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2022-04-23", "2023-09-30", "2022-09-30"]),
        name="date",
    )

    result = roll_back_by_month_df(df, col_name="date", n_months=6)

    pd.testing.assert_series_equal(result["date"], expected)
    pd.testing.assert_frame_equal(df, original)


def test_roll_back_by_month_df_uses_custom_date_format():
    df = pd.DataFrame({"date": ["31/03/2024"]})

    result = roll_back_by_month_df(
        df,
        col_name="date",
        n_months=1,
        date_format="%d/%m/%Y",
    )

    assert result.loc[0, "date"] == pd.Timestamp("2024-02-29")
