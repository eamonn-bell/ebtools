import json

import numpy as np
import pandas as pd
import pytest

from ebtools.general.dataframe_conversion import (
    correct_str_elements_float,
    correct_str_elements_int,
    create_df_from_json,
    create_df_from_json_from_file,
)


def test_correct_str_elements_float_converts_comma_strings():
    df = pd.DataFrame({"value": ["1,234.50", "2.50"]})
    original = df.copy(deep=True)

    result = correct_str_elements_float(df, colname="value")

    assert result["value"].dtype == np.float64
    assert result["value"].to_list() == [1234.5, 2.5]
    pd.testing.assert_frame_equal(df, original)


def test_correct_str_elements_float_rejects_invalid_numeric_string():
    df = pd.DataFrame({"value": ["bad"]})

    with pytest.raises(ValueError):
        correct_str_elements_float(df, colname="value")


def test_correct_str_elements_int_converts_comma_strings():
    df = pd.DataFrame({"value": ["1,234", "2"]})
    original = df.copy(deep=True)

    result = correct_str_elements_int(df, colname="value")

    assert result["value"].dtype == np.int64
    assert result["value"].to_list() == [1234, 2]
    pd.testing.assert_frame_equal(df, original)


def test_correct_str_elements_int_rejects_invalid_numeric_string():
    df = pd.DataFrame({"value": ["bad"]})

    with pytest.raises(ValueError):
        correct_str_elements_int(df, colname="value")


def test_create_df_from_json_normalises_response():
    response = [{"a": 1, "nested": {"b": 2}}]

    result = create_df_from_json(response)

    assert result.columns.to_list() == ["a", "nested.b"]
    assert result.loc[0, "nested.b"] == 2


def test_create_df_from_json_from_file_reads_data_key(tmp_path):
    path = tmp_path / "response.json"
    path.write_text(json.dumps({"data": [{"a": 1}, {"a": 2}]}))

    result = create_df_from_json_from_file(str(path))

    assert result["a"].to_list() == [1, 2]


def test_create_df_from_json_from_file_accepts_path_object(tmp_path):
    path = tmp_path / "response.json"
    path.write_text(json.dumps({"data": [{"a": 1}]}))

    result = create_df_from_json_from_file(path)

    assert result["a"].to_list() == [1]
