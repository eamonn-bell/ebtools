import pandas as pd
import pytest

from ebtools.general.sp_efa_dataframe import (
    add_date_efa_cols,
    add_efa_datetime_col,
    add_sp_and_efa_from_datetime,
    add_sp_from_datetime_col,
    add_sp_start_end_datetimes,
    add_sp_to_efa_column,
)


def test_add_sp_from_datetime_col_returns_copy():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01 00:00:00", "2024-01-01 00:30:00"])})
    original = df.copy(deep=True)

    result = add_sp_from_datetime_col(df)

    pd.testing.assert_frame_equal(df, original)
    assert result["SP"].to_list() == [1, 2]


def test_add_sp_from_datetime_col_rejects_missing_column():
    with pytest.raises(KeyError, match="Missing"):
        add_sp_from_datetime_col(pd.DataFrame({"Date": []}), datetime_col="Missing")


def test_add_sp_from_datetime_col_rejects_non_half_hour_datetime():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01 00:15:00"])})

    with pytest.raises(ValueError, match="half-hour"):
        add_sp_from_datetime_col(df)


def test_add_sp_start_end_datetimes_returns_copy():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"]), "SP": [1]})
    original = df.copy(deep=True)

    result = add_sp_start_end_datetimes(df)

    pd.testing.assert_frame_equal(df, original)
    assert result.loc[0, "SP_start"] == pd.Timestamp("2024-01-01 00:00:00")
    assert result.loc[0, "SP_end"] == pd.Timestamp("2024-01-01 00:30:00")


def test_add_sp_start_end_datetimes_can_add_start_or_end_only():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"]), "SP": [2]})

    start_result = add_sp_start_end_datetimes(df, position="start")
    end_result = add_sp_start_end_datetimes(df, position="end")

    assert "SP_start" in start_result.columns
    assert "SP_end" not in start_result.columns
    assert "SP_end" in end_result.columns
    assert "SP_start" not in end_result.columns


def test_add_sp_start_end_datetimes_rejects_invalid_position():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"]), "SP": [1]})

    with pytest.raises(ValueError, match="position"):
        add_sp_start_end_datetimes(df, position="middle")


def test_add_sp_start_end_datetimes_rejects_invalid_sp():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"]), "SP": [49]})

    with pytest.raises(ValueError, match="range 1 to 48"):
        add_sp_start_end_datetimes(df)


def test_add_sp_to_efa_column_returns_copy():
    df = pd.DataFrame({"SP": [1, 23, 47]})
    original = df.copy(deep=True)

    result = add_sp_to_efa_column(df)

    pd.testing.assert_frame_equal(df, original)
    assert result["EFA"].to_list() == [1, 4, 1]


def test_add_sp_to_efa_column_rejects_missing_column():
    with pytest.raises(KeyError, match="Missing"):
        add_sp_to_efa_column(pd.DataFrame({"SP": []}), sp_col="Missing")


def test_add_efa_datetime_col_returns_copy():
    df = pd.DataFrame({"Date": ["2023-03-14"], "EFA": [1]})
    original = df.copy(deep=True)

    result = add_efa_datetime_col(df)

    pd.testing.assert_frame_equal(df, original)
    assert result.loc[0, "EFA_Datetime"] == "2023-03-13T23:00:00"


def test_add_efa_datetime_col_rejects_missing_column():
    with pytest.raises(KeyError, match="Missing"):
        add_efa_datetime_col(pd.DataFrame({"Date": []}), efa_col="Missing")


def test_add_date_efa_cols_returns_copy():
    df = pd.DataFrame({"Datetime": ["2023-03-13T23:00:00", "2023-03-14T11:00:00"]})
    original = df.copy(deep=True)

    result = add_date_efa_cols(df, datetime_col="Datetime")

    pd.testing.assert_frame_equal(df, original)
    assert result["Date"].to_list() == ["2023-03-14", "2023-03-14"]
    assert result["EFA"].to_list() == [1, 4]


def test_add_date_efa_cols_rejects_missing_column():
    with pytest.raises(KeyError, match="Missing"):
        add_date_efa_cols(pd.DataFrame({"Datetime": []}), datetime_col="Missing")


def test_add_sp_and_efa_from_datetime_returns_copy():
    df = pd.DataFrame({"Datetime": pd.to_datetime(["2023-03-14 11:15:00"])})
    original = df.copy(deep=True)

    result = add_sp_and_efa_from_datetime(df, colname="Datetime")

    pd.testing.assert_frame_equal(df, original)
    assert result.loc[0, "SP"] == 23
    assert result.loc[0, "EFA"] == 4
    assert "SP_start_datetime" not in result.columns


def test_add_sp_and_efa_from_datetime_rejects_missing_column():
    with pytest.raises(KeyError, match="Missing"):
        add_sp_and_efa_from_datetime(pd.DataFrame({"Datetime": []}), colname="Missing")
