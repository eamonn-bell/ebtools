import pandas as pd
import pytest

from ebtools.general.dataframe_filtering import (
    df_cutoff,
    df_filter,
    drop_empty_df_cols,
    melt_df,
)


def test_df_filter_includes_matching_scalar_term():
    df = pd.DataFrame({"category": ["a", "b", "a"], "value": [1, 2, 3]})

    result = df_filter(df, colname="category", term="a")

    assert result["value"].to_list() == [1, 3]


def test_df_filter_excludes_matching_list_terms():
    df = pd.DataFrame({"category": ["a", "b", "c"], "value": [1, 2, 3]})

    result = df_filter(df, colname="category", term=["a", "c"], include=False)

    assert result["category"].to_list() == ["b"]


def test_df_filter_returns_copy():
    df = pd.DataFrame({"category": ["a", "b"], "value": [1, 2]})

    result = df_filter(df, colname="category", term="a")
    result.loc[result.index[0], "value"] = 99

    assert df.loc[0, "value"] == 1


def test_df_filter_rejects_missing_column():
    df = pd.DataFrame({"category": ["a"]})

    with pytest.raises(KeyError):
        df_filter(df, colname="missing", term="a")


def test_df_cutoff_keeps_dates_after_or_equal_target():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01", "2024-01-02"])})

    result = df_cutoff(df, target_date="2024-01-02", colname="Date", direction="after")

    assert result["Date"].to_list() == [pd.Timestamp("2024-01-02")]
    assert result.index.to_list() == [0]


def test_df_cutoff_keeps_dates_before_target_without_resetting_index():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01", "2024-01-02"])})

    result = df_cutoff(
        df,
        target_date="2024-01-02",
        colname="Date",
        direction="before",
        reset_index=False,
    )

    assert result["Date"].to_list() == [pd.Timestamp("2024-01-01")]
    assert result.index.to_list() == [0]


def test_df_cutoff_rejects_invalid_direction():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"])})

    with pytest.raises(ValueError, match="direction must be"):
        df_cutoff(df, target_date="2024-01-01", colname="Date", direction="during")


def test_df_cutoff_rejects_missing_column():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"])})

    with pytest.raises(KeyError):
        df_cutoff(df, target_date="2024-01-01", colname="Missing")


def test_drop_empty_df_cols_removes_all_zero_columns():
    df = pd.DataFrame({"empty": [0, 0], "value": [0, 1]})

    result = drop_empty_df_cols(df)

    assert result.columns.to_list() == ["value"]


def test_drop_empty_df_cols_keeps_nan_only_columns():
    df = pd.DataFrame({"missing": [None, None], "value": [1, 2]})

    result = drop_empty_df_cols(df)

    assert result.columns.to_list() == ["missing", "value"]


def test_melt_df_converts_pivot_dataframe_to_long_form():
    df = pd.DataFrame(
        {1: [10, 30], 2: [20, 40]},
        index=pd.to_datetime(["2024-01-01", "2024-01-02"]),
    )

    result = melt_df(df, interval_type="SP", value_name="value")

    assert result.columns.to_list() == ["Date", "SP", "value"]
    assert result["value"].to_list() == [10, 20, 30, 40]


def test_melt_df_renames_named_index_to_date():
    df = pd.DataFrame(
        {1: [10]},
        index=pd.Index(pd.to_datetime(["2024-01-01"]), name="TradingDate"),
    )

    result = melt_df(df, interval_type="SP", value_name="value")

    assert result.columns.to_list() == ["Date", "SP", "value"]
