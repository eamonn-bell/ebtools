import pandas as pd
import pytest

from ebtools.general.dataframe_dates import add_buffer_days, add_columns


def test_add_buffer_days_moves_date_backward_and_forward():
    assert add_buffer_days("2024-01-10", direction="start", days=2) == "2024-01-08"
    assert add_buffer_days("2024-01-10", direction="end", days=3) == "2024-01-13"


def test_add_buffer_days_rejects_invalid_direction():
    with pytest.raises(ValueError, match="direction must be"):
        add_buffer_days("2024-01-10", direction="middle")


def test_add_columns_adds_expected_date_columns():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01", "2024-04-01"])})

    result = add_columns(df.copy(), col="Date")

    assert {"Year", "Week", "Day", "DayYear", "Delivery_Year", "Month_start"}.issubset(
        result.columns
    )
    assert result["Year"].to_list() == [2024, 2024]
    assert result["Delivery_Year"].to_list() == ["2023_24", "2024_25"]
    assert result["Month_start"].to_list() == [
        pd.Timestamp("2024-01-01"),
        pd.Timestamp("2024-04-01"),
    ]


def test_add_columns_does_not_mutate_input_dataframe():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"])})
    original = df.copy(deep=True)

    result = add_columns(df, col="Date")

    pd.testing.assert_frame_equal(df, original)
    assert result is not df


def test_add_columns_rejects_missing_date_column():
    df = pd.DataFrame({"Other": ["2024-01-01"]})

    with pytest.raises(KeyError):
        add_columns(df, col="Date")
