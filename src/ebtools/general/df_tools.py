#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compatibility exports for dataframe helper functions.

The implementation has been split into focused modules. Importing from
``ebtools.general.df_tools`` remains supported for existing code.
"""

import warnings

warnings.warn(
    "ebtools.general.df_tools is deprecated and will be removed from ebtools "
    "in a future version. Import from the focused dataframe modules or from "
    "ebtools.general instead.",
    FutureWarning,
    stacklevel=2,
)

from ebtools.general.dataframe_dates import (
    add_buffer_days,
    add_columns,
)
from ebtools.general.dataframe_selection import (
    select_year,
    select_weeks,
    select_days,
)
from ebtools.general.dataframe_plotting import (
    make_full_year_pivot,
    make_full_plotting_df,
    make_pivot_calendar,
)
from ebtools.general.dataframe_base import (
    adjust_for_clock_change,
    base_df,
)
from ebtools.general.dataframe_filtering import (
    df_filter,
    df_cutoff,
    drop_empty_df_cols,
    melt_df,
)
from ebtools.general.dataframe_processing import (
    unique_element_count,
    non_numeric_pivot,
    df_round_to_decimal,
)
from ebtools.general.dataframe_formatting import (
    remove_df_index_name,
    remove_df_column_name,
)
from ebtools.general.dataframe_conversion import (
    correct_str_elements_float,
    correct_str_elements_int,
    create_df_from_json,
    create_df_from_json_from_file,
)
