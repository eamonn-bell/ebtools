import numpy as np
import pandas as pd
import pytest

from ebtools.general.dataframe_processing import (
    df_round_to_decimal,
    non_numeric_pivot,
    unique_element_count,
)


def test_unique_element_count_ignores_null_values():
    df = pd.DataFrame({"category": ["a", "a", "b", None, np.nan]})

    assert unique_element_count(df, "category") == 2


def test_unique_element_count_rejects_missing_column():
    df = pd.DataFrame({"category": ["a"]})

    with pytest.raises(KeyError):
        unique_element_count(df, "missing")


def test_non_numeric_pivot_aggregates_string_values():
    df = pd.DataFrame(
        {
            "Date": ["2024-01-01", "2024-01-01"],
            "label": ["a", "b"],
            "value": ["x", "y"],
        }
    )

    result = non_numeric_pivot(df, index="Date", columns="label", values="value")

    assert result.loc["2024-01-01", "a"] == "x"
    assert result.loc["2024-01-01", "b"] == "y"


def test_non_numeric_pivot_joins_multiple_values_per_cell():
    df = pd.DataFrame(
        {
            "Date": ["2024-01-01", "2024-01-01"],
            "label": ["a", "a"],
            "value": ["x", "y"],
        }
    )

    result = non_numeric_pivot(df, index="Date", columns="label", values="value")

    assert result.loc["2024-01-01", "a"] == "xy"


def test_df_round_to_decimal_rounds_selected_columns_without_mutating_input():
    df = pd.DataFrame({"a": [1.234], "b": [5.678]})

    result = df_round_to_decimal(df, colname=["a", "b"], decimals=1)

    assert result.loc[0, "a"] == 1.2
    assert result.loc[0, "b"] == 5.7
    assert df.loc[0, "a"] == 1.234


def test_df_round_to_decimal_accepts_single_column_name():
    df = pd.DataFrame({"a": [1.234], "b": [5.678]})

    result = df_round_to_decimal(df, colname="a", decimals=2)

    assert result.loc[0, "a"] == 1.23
    assert result.loc[0, "b"] == 5.678


def test_df_round_to_decimal_rejects_missing_column():
    df = pd.DataFrame({"a": [1.234]})

    with pytest.raises(KeyError):
        df_round_to_decimal(df, colname="missing")
