#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:12:28 2023

@author: eamonnbell
"""


from ebtools.general.helper import (
    
    # Dict Tools
    sort_dict_by_keys,
    make_dict_keys_from_list,
    
    # Force to Type
    force_to_list,
    force_to_np_array

    )


from ebtools.general.read_data import (
    
    # Reading different file_types into dataframes
    read_from_csv,
    read_from_xlsx,
    read_from_parquet,
    
    # Reading HH Data into a dataframe
    load_hh_data
    
    )


from ebtools.general.save_data import (
    
    save_to_csv,
    save_to_xlsx,
    save_to_parquet
    
    )


from ebtools.general.inspect_funcs import (
    
    get_call_func_name,
    get_function_arguments
    
    )


from ebtools.general.file_reading_tools import (
    
    does_file_exist,
    get_file_type,
    list_all_files_in_folder,
    zip_checker
    
    )


from ebtools.general.datetime_calendar import (
    
    # Helper funcs
    is_year_leap_year,
    get_daylight_savings_dates,
    bst_date_range,
    )

from ebtools.general.datetime_conversion import (

    # Helper funcs
    convert_single_datetime_to_sp_start,
    convert_single_datetime_to_sp_end,
    
    # Convert Datetime
    convert_date_to_standard_date_str,
    convert_date_to_datetime,
    convert_datetime_to_date,
    convert_date_to_datetime_str,
    convert_date_to_first_of_month,
    convert_date_to_last_of_month,
    
    # Month-start and Month-end
    move_date_to_start_of_month,
    move_date_to_end_of_month
    
    )

from ebtools.general.datetime_timezone import (

    # Convert timezone-aware datetime columns
    convert_datetime_remove_tz_aware,
    convert_datetime_by_tz,

    )

from ebtools.general.datetime_dataframe import (

    # Add dataframe datetime columns
    convert_datetime_sp_start,
    convert_datetime_sp_end,
    add_first_of_month_col_from_int_cols,
    add_first_of_month_col_from_date_col,

    )

from ebtools.general.datetime_parsing import (
    
    # Check Datetime
    check_datetime_formats,
    check_datetime_formats_tz,
    check_string_datetime_formats,

    )

from ebtools.general.datetime_adjustments import (
    
    # Adjust Dates
    start_of_delivery_year,
    roll_back_by_month_str,
    roll_back_by_month_df,
    
    )


from ebtools.general.sp_efa_conversion import (
    
    # General
    sp_to_efa,
    hour_to_efa,
    current_sp,
    current_efa,
    make_sp_efa_table,

    )

from ebtools.general.sp_efa_datetime import (
    
    # EFA date and datetime
    convert_date_to_efa_datetime,
    convert_datetime_to_date_and_efa,

    )

from ebtools.general.sp_efa_strings import (
    
    # SP and EFA from strings
    make_sp_from_string,
    make_efa_from_string,

    )

from ebtools.general.sp_efa_dataframe import (
    
    # Add cols to df
    add_sp_from_datetime_col,
    add_sp_start_end_datetimes,
    add_sp_to_efa_column,
    add_efa_datetime_col,
    add_date_efa_cols,
    add_sp_and_efa_from_datetime
    
    )


from ebtools.general.dataframe_dates import (
    
    # Dataframe - Augmentation
    add_buffer_days,
    add_columns,
    )

from ebtools.general.dataframe_selection import (

    # Dataframe - Date Range Selection
    select_year,
    select_weeks,
    select_days,
    )

from ebtools.general.dataframe_plotting import (

    # Dataframe - Analysis and Plotting
    make_full_year_pivot,
    make_full_plotting_df,
    make_pivot_calendar,
    )

from ebtools.general.dataframe_base import (

    # Dataframe - BASE
    adjust_for_clock_change,
    base_df,
    )

from ebtools.general.dataframe_filtering import (

    # Dataframe - Filtering
    df_filter,
    df_cutoff,
    drop_empty_df_cols,
    melt_df,
    )

from ebtools.general.dataframe_processing import (

    # Dataframe - Processing
    unique_element_count,
    non_numeric_pivot,
    df_round_to_decimal,
    )

from ebtools.general.dataframe_formatting import (

    # Dataframe - Formatting
    remove_df_index_name,
    remove_df_column_name,
    )

from ebtools.general.dataframe_conversion import (

    # Dataframe - Correct Strings
    correct_str_elements_float,
    correct_str_elements_int,

    # Dataframe - Create df from JSON
    create_df_from_json,
    create_df_from_json_from_file
    )


from ebtools.general.df_tools_string_dates import (
    
    # STRING date functions
    week_starting,
    week_number,
    weekday_number,
    day_of_the_year_number
    
    )

from ebtools.general.array_selection import (
    
    # General
    add_newaxis,
    
    # Select data from ROWS
    n_smallest_values_per_row,
    n_largest_values_per_row
    
    )


from ebtools.general.online import (

    is_online
    
    )
