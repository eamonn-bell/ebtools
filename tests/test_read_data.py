import pandas as pd
import pytest

from ebtools.general.read_data import (
    load_hh_data,
    read_from_csv,
    read_from_parquet,
    read_from_xlsx,
)


def _write_hh_csv(path, no_periods=48):
    period_cols = [f"P{i}" for i in range(1, no_periods + 1)]
    df = pd.DataFrame(
        [
            ["2024-01-01", 111, "Site A", *range(1, no_periods + 1)],
            ["2024-01-01", 222, "Site B", *range(101, 101 + no_periods)],
            ["2024-01-02", 111, "Site A", *range(201, 201 + no_periods)],
        ],
        columns=["Date", "MPAN", "Name", *period_cols],
    )
    df.to_csv(path, index=False)
    return df


def test_read_from_csv_loads_valid_file(tmp_path):
    expected = pd.DataFrame({"Date": ["2024-01-01"], "Price": [10.5]})
    expected.to_csv(tmp_path / "prices.csv", index=False)

    result = read_from_csv(tmp_path, "prices.csv")

    pd.testing.assert_frame_equal(result, expected)


def test_read_from_csv_rejects_wrong_extension(tmp_path):
    with pytest.raises(ValueError, match="expected file_type"):
        read_from_csv(tmp_path, "prices.txt")


def test_read_from_xlsx_loads_named_sheet(tmp_path):
    expected = pd.DataFrame({"Date": ["2024-01-01"], "Price": [10.5]})
    other = pd.DataFrame({"value": [1]})

    with pd.ExcelWriter(tmp_path / "prices.xlsx") as writer:
        other.to_excel(writer, sheet_name="Other", index=False)
        expected.to_excel(writer, sheet_name="Prices", index=False)

    result = read_from_xlsx(tmp_path, "prices.xlsx", sheet_name="Prices")

    pd.testing.assert_frame_equal(result, expected)


def test_read_from_xlsx_can_return_all_sheets(tmp_path):
    first = pd.DataFrame({"value": [1]})
    second = pd.DataFrame({"value": [2]})

    with pd.ExcelWriter(tmp_path / "prices.xlsx") as writer:
        first.to_excel(writer, sheet_name="First", index=False)
        second.to_excel(writer, sheet_name="Second", index=False)

    result = read_from_xlsx(tmp_path, "prices.xlsx", sheet_name=None)

    assert list(result) == ["First", "Second"]
    pd.testing.assert_frame_equal(result["First"], first)
    pd.testing.assert_frame_equal(result["Second"], second)


def test_read_from_xlsx_rejects_wrong_extension(tmp_path):
    with pytest.raises(ValueError, match="expected file_type"):
        read_from_xlsx(tmp_path, "prices.csv")


def test_read_from_parquet_loads_valid_file(tmp_path):
    expected = pd.DataFrame({"Date": ["2024-01-01"], "Price": [10.5]})
    expected.to_parquet(tmp_path / "prices.parquet", index=False)

    result = read_from_parquet(tmp_path, "prices.parquet")

    pd.testing.assert_frame_equal(result, expected)


def test_read_from_parquet_rejects_wrong_extension(tmp_path):
    with pytest.raises(ValueError, match="expected file_type"):
        read_from_parquet(tmp_path, "prices.csv")


def test_load_hh_data_loads_csv_pivot_and_aggregates_mpan(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    result = load_hh_data(
        tmp_path,
        "hh.csv",
        date_col_name="Date",
        mpan_col_name="MPAN",
    )

    assert result.index.name == "Date"
    assert result.columns.to_list() == list(range(1, 49))
    assert result.loc[pd.Timestamp("2024-01-01"), 1] == 102
    assert result.loc[pd.Timestamp("2024-01-02"), 48] == 248


def test_load_hh_data_filters_mpan_and_trims_dates(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    result = load_hh_data(
        tmp_path,
        "hh.csv",
        start_date="2024-01-02",
        end_date="2024-01-02",
        date_col_name="Date",
        mpan_col_name="MPAN",
        select_mpan=111,
    )

    assert result.index.to_list() == [pd.Timestamp("2024-01-02")]
    assert result.iloc[0, 0] == 201


def test_load_hh_data_can_return_time_columns(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    result = load_hh_data(
        tmp_path,
        "hh.csv",
        date_col_name="Date",
        cols_as_time=True,
    )

    assert result.columns[0] == "00:00"
    assert result.columns[1] == "00:30"
    assert result.columns[-1] == "23:30"


def test_load_hh_data_can_return_melted_output(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    result = load_hh_data(
        tmp_path,
        "hh.csv",
        date_col_name="Date",
        mpan_col_name="MPAN",
        select_mpan=111,
        pivot_format=False,
    )

    assert result.columns.to_list() == ["Date", "SP", "Outturn"]
    assert result.loc[0, "Date"] == pd.Timestamp("2024-01-01")
    assert result.loc[0, "SP"] == 1
    assert result.loc[0, "Outturn"] == 1


def test_load_hh_data_can_keep_mpan_in_melted_output(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    result = load_hh_data(
        tmp_path,
        "hh.csv",
        date_col_name="Date",
        mpan_col_name="MPAN",
        aggregate_by_mpan=False,
        drop_mpan_col=False,
        pivot_format=False,
    )

    assert result.columns.to_list() == ["Date", "MPAN", "SP", "Outturn"]
    assert set(result["MPAN"]) == {111, 222}


def test_load_hh_data_loads_xlsx_named_sheet(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")
    hh = pd.read_csv(tmp_path / "hh.csv")
    other = pd.DataFrame({"value": [1]})

    with pd.ExcelWriter(tmp_path / "hh.xlsx") as writer:
        other.to_excel(writer, sheet_name="Other", index=False)
        hh.to_excel(writer, sheet_name="HH", index=False)

    result = load_hh_data(
        tmp_path,
        "hh.xlsx",
        date_col_name="Date",
        sheet_name="HH",
    )

    assert result.index.name == "Date"
    assert result.columns.to_list() == list(range(1, 49))


def test_load_hh_data_rejects_sheet_name_none(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")
    hh = pd.read_csv(tmp_path / "hh.csv")

    with pd.ExcelWriter(tmp_path / "hh.xlsx") as writer:
        hh.to_excel(writer, sheet_name="HH", index=False)

    with pytest.raises(ValueError, match="single worksheet"):
        load_hh_data(tmp_path, "hh.xlsx", date_col_name="Date", sheet_name=None)


def test_load_hh_data_rejects_bad_file_type(tmp_path):
    with pytest.raises(ValueError, match="expected file_type"):
        load_hh_data(tmp_path, "hh.txt", date_col_name="Date")


def test_load_hh_data_rejects_unsupported_no_periods(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    with pytest.raises(ValueError, match="no_periods"):
        load_hh_data(tmp_path, "hh.csv", date_col_name="Date", no_periods=12)


def test_load_hh_data_rejects_missing_date_column(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    with pytest.raises(KeyError, match="Missing"):
        load_hh_data(tmp_path, "hh.csv", date_col_name="Missing")


def test_load_hh_data_rejects_missing_mpan_column(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    with pytest.raises(KeyError, match="Missing"):
        load_hh_data(tmp_path, "hh.csv", date_col_name="Date", mpan_col_name="Missing")


def test_load_hh_data_rejects_select_mpan_without_mpan_column(tmp_path):
    _write_hh_csv(tmp_path / "hh.csv")

    with pytest.raises(ValueError, match="mpan_col_name"):
        load_hh_data(tmp_path, "hh.csv", date_col_name="Date", select_mpan=111)
