import zipfile

import pytest

from ebtools.general.file_reading_tools import (
    does_file_exist,
    get_file_type,
    list_all_files_in_folder,
    zip_checker,
)


def _make_zip(path, names):
    with zipfile.ZipFile(path, "w") as zf:
        for name in names:
            zf.writestr(name, "content")


def test_does_file_exist_returns_true_for_existing_file(tmp_path):
    file_path = tmp_path / "data.csv"
    file_path.write_text("value\n1\n")

    assert does_file_exist(file_path) is True


def test_does_file_exist_returns_false_for_directory_or_missing_path(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()

    assert does_file_exist(folder) is False
    assert does_file_exist(tmp_path / "missing.csv") is False


def test_get_file_type_returns_extension_without_dot():
    assert get_file_type("data/example.csv") == "csv"


def test_get_file_type_returns_empty_string_when_no_extension():
    assert get_file_type("README") == ""


def test_get_file_type_returns_final_extension_for_multi_extension_path():
    assert get_file_type("archive.tar.gz") == "gz"


def test_list_all_files_in_folder_returns_sorted_filenames_without_ds_store(tmp_path):
    (tmp_path / "b.csv").write_text("b")
    (tmp_path / "a.csv").write_text("a")
    (tmp_path / ".DS_Store").write_text("metadata")
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "c.csv").write_text("c")

    result = list_all_files_in_folder(tmp_path)

    assert result == ["a.csv", "b.csv", "c.csv"]


def test_list_all_files_in_folder_preserves_duplicate_filenames(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    (first / "data.csv").write_text("1")
    (second / "data.csv").write_text("2")

    result = list_all_files_in_folder(tmp_path)

    assert result == ["data.csv", "data.csv"]


def test_zip_checker_single_zip_returns_list_of_names(tmp_path):
    _make_zip(tmp_path / "archive.zip", ["a.csv", "b.csv"])

    result = zip_checker(
        tmp_path,
        assess_folder=False,
        file_name="archive.zip",
    )

    assert result == [["a.csv", "b.csv"]]


def test_zip_checker_single_zip_can_return_dict(tmp_path):
    _make_zip(tmp_path / "archive.zip", ["a.csv"])

    result = zip_checker(
        tmp_path,
        assess_folder=False,
        file_name="archive.zip",
        output="dict",
    )

    assert result == {"archive.zip": ["a.csv"]}


def test_zip_checker_value_type_str_returns_first_name(tmp_path):
    _make_zip(tmp_path / "archive.zip", ["a.csv", "b.csv"])

    result = zip_checker(
        tmp_path,
        assess_folder=False,
        file_name="archive.zip",
        value_type="str",
    )

    assert result == ["a.csv"]


def test_zip_checker_folder_mode_reads_all_zipfiles(tmp_path):
    _make_zip(tmp_path / "b.zip", ["b.csv"])
    _make_zip(tmp_path / "a.zip", ["a.csv"])

    result = zip_checker(tmp_path, assess_folder=True, output="dict")

    assert result == {
        "a.zip": ["a.csv"],
        "b.zip": ["b.csv"],
    }


def test_zip_checker_rejects_invalid_output(tmp_path):
    with pytest.raises(ValueError, match="output must be"):
        zip_checker(tmp_path, output="tuple")


def test_zip_checker_rejects_invalid_value_type(tmp_path):
    with pytest.raises(ValueError, match="value_type must be"):
        zip_checker(tmp_path, value_type="first")


def test_zip_checker_requires_file_name_when_not_assessing_folder(tmp_path):
    with pytest.raises(ValueError, match="file_name must be provided"):
        zip_checker(tmp_path, assess_folder=False)
