#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compatibility exports for datetime helper functions.

The implementation has been split into focused modules. Importing from
``ebtools.general.datetime_funcs`` remains supported for existing code.
"""

import warnings

warnings.warn(
    "ebtools.general.datetime_funcs is deprecated and will be removed from "
    "ebtools in a future version. Import from the focused datetime modules "
    "or from ebtools.general instead.",
    FutureWarning,
    stacklevel=2,
)

from ebtools.general.datetime_calendar import (
    is_year_leap_year,
    get_daylight_savings_dates,
    bst_date_range,
)
from ebtools.general.datetime_conversion import (
    convert_single_datetime_to_sp_start,
    convert_single_datetime_to_sp_end,
    convert_date_to_standard_date_str,
    convert_date_to_datetime,
    convert_datetime_to_date,
    convert_date_to_datetime_str,
    convert_date_to_first_of_month,
    convert_date_to_last_of_month,
    move_date_to_start_of_month,
    move_date_to_end_of_month,
)
from ebtools.general.datetime_timezone import (
    convert_datetime_remove_tz_aware,
    convert_datetime_by_tz,
)
from ebtools.general.datetime_dataframe import (
    convert_datetime_sp_start,
    convert_datetime_sp_end,
    add_first_of_month_col_from_int_cols,
    add_first_of_month_col_from_date_col,
)
from ebtools.general.datetime_parsing import (
    check_datetime_formats,
    check_datetime_formats_tz,
    check_string_datetime_formats,
)
from ebtools.general.datetime_adjustments import (
    start_of_delivery_year,
    roll_back_by_month_str,
    roll_back_by_month_df,
)
