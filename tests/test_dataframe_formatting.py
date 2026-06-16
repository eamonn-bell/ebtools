import pandas as pd

from ebtools.general.dataframe_formatting import (
    remove_df_column_name,
    remove_df_index_name,
)


def test_remove_df_index_name_removes_index_axis_name():
    df = pd.DataFrame({"value": [1]})
    df.index.name = "idx"

    result = remove_df_index_name(df)

    assert result.index.name is None
    assert df.index.name == "idx"


def test_remove_df_column_name_removes_column_axis_name():
    df = pd.DataFrame({"value": [1]})
    df.columns.name = "cols"

    result = remove_df_column_name(df)

    assert result.columns.name is None
    assert df.columns.name == "cols"
