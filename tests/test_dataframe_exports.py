import pytest

import ebtools as ebt
import ebtools.general as general

from ebtools.general.dataframe_base import base_df as direct_base_df


def test_dataframe_helpers_are_exported_from_expected_paths():
    with pytest.warns(FutureWarning, match="ebtools.general.df_tools is deprecated"):
        from ebtools.general.df_tools import base_df as facade_base_df

    assert facade_base_df is direct_base_df
    assert general.base_df is direct_base_df
    assert ebt.base_df is direct_base_df
