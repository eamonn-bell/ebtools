import pandas as pd
import pytest

from ebtools.general.save_data import (
    save_to_csv,
    save_to_parquet,
    save_to_xlsx,
)


def test_save_to_csv_writes_without_index_by_default(tmp_path):
    df = pd.DataFrame({"value": [1, 2]})

    save_to_csv(df, tmp_path, "out.csv")

    result = pd.read_csv(tmp_path / "out.csv")
    pd.testing.assert_frame_equal(result, df)


def test_save_to_csv_can_write_index(tmp_path):
    df = pd.DataFrame({"value": [1, 2]}, index=pd.Index(["a", "b"], name="id"))

    save_to_csv(df, tmp_path, "out.csv", index=True)

    result = pd.read_csv(tmp_path / "out.csv")
    expected = pd.DataFrame({"id": ["a", "b"], "value": [1, 2]})
    pd.testing.assert_frame_equal(result, expected)


def test_save_to_csv_rejects_wrong_extension(tmp_path):
    df = pd.DataFrame({"value": [1]})

    with pytest.raises(ValueError, match="expected file_type"):
        save_to_csv(df, tmp_path, "out.txt")


def test_save_to_xlsx_writes_single_dataframe(tmp_path):
    df = pd.DataFrame({"value": [1, 2]})

    save_to_xlsx(df, tmp_path, "out.xlsx", sheet_name="Data")

    result = pd.read_excel(tmp_path / "out.xlsx", sheet_name="Data")
    pd.testing.assert_frame_equal(result, df)


def test_save_to_xlsx_writes_multiple_dataframes(tmp_path):
    prices = pd.DataFrame({"price": [10, 20]})
    volumes = pd.DataFrame({"volume": [1, 2]}, index=pd.Index(["a", "b"], name="id"))

    save_to_xlsx(
        [prices, volumes],
        tmp_path,
        "out.xlsx",
        sheet_name=["Prices", "Volumes"],
        index=[False, True],
    )

    price_result = pd.read_excel(tmp_path / "out.xlsx", sheet_name="Prices")
    volume_result = pd.read_excel(tmp_path / "out.xlsx", sheet_name="Volumes")
    expected_volume = pd.DataFrame({"id": ["a", "b"], "volume": [1, 2]})

    pd.testing.assert_frame_equal(price_result, prices)
    pd.testing.assert_frame_equal(volume_result, expected_volume)


def test_save_to_xlsx_rejects_wrong_extension(tmp_path):
    df = pd.DataFrame({"value": [1]})

    with pytest.raises(ValueError, match="expected file_type"):
        save_to_xlsx(df, tmp_path, "out.csv", sheet_name="Data")


def test_save_to_xlsx_rejects_sheet_name_length_mismatch(tmp_path):
    df = [pd.DataFrame({"value": [1]}), pd.DataFrame({"value": [2]})]

    with pytest.raises(ValueError, match="same number"):
        save_to_xlsx(df, tmp_path, "out.xlsx", sheet_name=["Only One"])


def test_save_to_xlsx_rejects_index_length_mismatch(tmp_path):
    df = [pd.DataFrame({"value": [1]}), pd.DataFrame({"value": [2]})]

    with pytest.raises(ValueError, match="one value per dataframe"):
        save_to_xlsx(
            df,
            tmp_path,
            "out.xlsx",
            sheet_name=["One", "Two"],
            index=[False],
        )


def test_save_to_parquet_writes_without_index_by_default(tmp_path):
    df = pd.DataFrame({"value": [1, 2]})

    save_to_parquet(df, tmp_path, "out.parquet")

    result = pd.read_parquet(tmp_path / "out.parquet")
    pd.testing.assert_frame_equal(result, df)


def test_save_to_parquet_can_write_index(tmp_path):
    df = pd.DataFrame({"value": [1, 2]}, index=pd.Index(["a", "b"], name="id"))

    save_to_parquet(df, tmp_path, "out.parquet", index=True)

    result = pd.read_parquet(tmp_path / "out.parquet")
    expected = pd.DataFrame({"value": [1, 2]}, index=pd.Index(["a", "b"], name="id"))
    pd.testing.assert_frame_equal(result, expected)


def test_save_to_parquet_rejects_wrong_extension(tmp_path):
    df = pd.DataFrame({"value": [1]})

    with pytest.raises(ValueError, match="expected file_type"):
        save_to_parquet(df, tmp_path, "out.csv")
