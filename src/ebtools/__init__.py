# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:48:46 2021

@author: Eamonn.Bell
"""



from ebtools.general import (

    # HELPER functions
    get_file_type,
    force_to_list,
    force_to_np_array,
    sort_dict_by_keys,
    adjust_for_clock_change,
    base_df,
    df_filter,
    df_cutoff,
    drop_empty_df_cols,
    melt_df,
    unique_element_count,
    non_numeric_pivot,
    df_round_to_decimal,
    make_dict_keys_from_list,
    remove_df_index_name,
    remove_df_column_name,
    correct_str_elements_float,
    correct_str_elements_int,

    # DF TOOLS - Create df from JSON
    create_df_from_json,
    create_df_from_json_from_file,

    # READ data - general file_types
    read_from_csv,
    read_from_xlsx,
    read_from_parquet,
    
    # READ data - HH Data into a dataframe
    load_hh_data,

    # SAVE data
    save_to_csv,
    save_to_xlsx,
    save_to_parquet,
    
    # INSPECT functions
    get_call_func_name,
    get_function_arguments,
    
    # FILE READING tools
    does_file_exist,
    list_all_files_in_folder,
    zip_checker,
    
    # DATETIME - Helper funcs
    is_year_leap_year,
    get_daylight_savings_dates,
    bst_date_range,
    convert_single_datetime_to_sp_start,
    convert_single_datetime_to_sp_end,
    
    # DATETIME - Convert Datetime
    convert_date_to_standard_date_str,
    convert_date_to_datetime,
    convert_datetime_to_date,
    convert_date_to_datetime_str,
    convert_date_to_first_of_month,
    convert_date_to_last_of_month,
    convert_datetime_remove_tz_aware,
    convert_datetime_by_tz,
    convert_datetime_sp_start,
    convert_datetime_sp_end,
    
    # DATETIME - Check Datetime
    check_datetime_formats,
    check_datetime_formats_tz,
    check_string_datetime_formats,
    
    # DATETIME - Adjust Dates
    start_of_delivery_year,
    roll_back_by_month_str,
    roll_back_by_month_df,
    
    # DATETIME - Add first-of-month-col
    add_first_of_month_col_from_int_cols,
    add_first_of_month_col_from_date_col,

    # DATETIME - Month-start and Month-end
    move_date_to_start_of_month,
    move_date_to_end_of_month,
    
    # SP_EFA
    sp_to_efa,
    hour_to_efa,
    current_sp,
    current_efa,
    make_sp_efa_table,
    convert_date_to_efa_datetime,
    convert_datetime_to_date_and_efa,
    make_sp_from_string,
    make_efa_from_string,
    add_sp_from_datetime_col,
    add_sp_start_end_datetimes,
    add_sp_to_efa_column,
    add_efa_datetime_col,
    add_date_efa_cols,
    add_sp_and_efa_from_datetime,
    
    # DATAFRAME SELECTION - Dataframe Augmentation
    add_columns,
    add_buffer_days,
    
    # Dataframe Date Range Selection
    select_year,
    select_weeks,
    select_days,
    
    # Analysis and Plotting dataframes
    make_full_year_pivot,
    make_full_plotting_df,
    make_pivot_calendar,
    
    # DATAFRAME SELECTION - STRING date functions
    week_starting,
    week_number,
    weekday_number,
    day_of_the_year_number,
    
    # ARRAY GENERAL functions
    add_newaxis,
    
    # ARRAY SELECTION functions 
    n_smallest_values_per_row,
    n_largest_values_per_row,

    # ONLINE tools
    is_online

    )


from ebtools.data import (
    
    # Date lists for quick formatting
    format_list_standard,
    format_list_tz,
    
    )


import ebtools.data as data


from ebtools._version import __version__


# Module level doc_string
__doc__ = """

Write a docstring here which sets out what each high level component of the 
module does.

State the the docstrings of each high level component will suggest the best
ways to use that module, the most useful functions, and the right order in 
which to use them. 
"""
