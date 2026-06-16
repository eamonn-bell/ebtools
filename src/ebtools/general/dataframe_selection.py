#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

from typing import Literal

import numpy as np
import pandas as pd

from ebtools.general.dataframe_dates import add_buffer_days, add_columns
from ebtools.general.dataframe_helpers import (
    _date_range_frequency,
    _full_week_index,
)



# ---- Dataframe - Date Range Selection


AverageType = Literal['int', 'float']
Period = Literal['day', 'efa', 'sp']
ReplaceZeroValue = int | float | str


def _replace_zero_values(
        df: pd.DataFrame,
        replace_zero: ReplaceZeroValue
        ) -> pd.DataFrame:
    """
    Return a copy of `df` with zero values replaced.
    """
    replacement = np.nan if replace_zero == 'nan' else replace_zero

    return df.replace(0, replacement)


def _add_average_column(
        df: pd.DataFrame,
        average_all: bool,
        average_type: AverageType
        ) -> pd.DataFrame:
    """
    Return a copy of `df` with an ``Average`` column.
    """
    df_update = df.copy()

    if average_all:
        average_values = df_update.mean(axis=1)
    else:
        past_years = df_update.columns[:-1]
        average_values = df_update.loc[:, past_years].mean(axis=1)

    if average_type == 'int':
        df_update['Average'] = average_values.astype('Int64')
    elif average_type == 'float':
        df_update['Average'] = average_values.astype(np.float64)
    else:
        raise ValueError("average_type must be 'int' or 'float'.")

    return df_update





def select_year(
        df: pd.DataFrame,
        year: int | None = None,
        full_year: bool = True,
        period: Period | str = 'day',
        add_buffer: bool = False,
        buffer_days: int = 1
        ) -> pd.DataFrame:
    """
    Select one year from a dataframe with a datetime index.

    Optionally reindex the result to a complete calendar year at daily, EFA,
    or settlement-period frequency. When `add_buffer` is ``True``, the
    reindexing range is extended by `buffer_days` at either side. The input
    rows are still selected from `year`.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe with a datetime-like index.
    year : int or None, default None
        Calendar year to select.
    full_year : bool, default True
        If ``True``, reindex the result to cover the full selected year.
    period : {'day', 'efa', 'sp'}, default 'day'
        Frequency represented by the dataframe index.
    add_buffer : bool, default False
        If ``True``, add buffer days before and after the selected range.
    buffer_days : int, default 1
        Number of buffer days to add when `add_buffer` is ``True``.

    Returns
    -------
    pandas.DataFrame
        Dataframe containing data for the selected year.

    Examples
    --------
    Select rows from one calendar year without filling missing dates:

    >>> index = pd.date_range("2023-12-31", "2025-01-01", freq="D")
    >>> df = pd.DataFrame({"value": range(len(index))}, index=index)
    >>> select_year(df, year=2024, full_year=False).index.year.unique().tolist()
    [2024]

    Reindex sparse data to a full year:

    >>> df = pd.DataFrame({"value": [1]}, index=pd.to_datetime(["2024-01-03"]))
    >>> result = select_year(df, year=2024, full_year=True)
    >>> result.index.min()
    Timestamp('2024-01-01 00:00:00')

    """
    period_use = period.lower()
    
    start_date = str(year)+'-01-01'
    end_date   = str(year)+'-12-31'

    if add_buffer:
        start_date = add_buffer_days(start_date, direction='start', days=buffer_days)
        end_date   = add_buffer_days(end_date, direction='end', days=buffer_days)
    
    df_update = df.loc[(df.index.year == year)].copy()
    
    if full_year: 
        new_df_index = pd.date_range(
            start=start_date,
            end=end_date, 
            freq=_date_range_frequency(period_use)
            )
        
        if period_use == 'efa': 
            new_df_index = new_df_index - pd.Timedelta('1h')
        
        df_update = df_update.reindex(new_df_index)
    
    return df_update





def select_weeks(
        df: pd.DataFrame, 
        week: int | None = None,
        date_col: str = 'Date',
        sp_col: str = 'SP',
        value_col: str = 'TD',
        average_col: bool = True,
        average_all: bool = False,
        average_type: AverageType = 'int',
        make_week_full: bool = True,
        replace_zero: ReplaceZeroValue = 'nan',
        periods_per_day: int = 48
        ) -> pd.DataFrame:
    """
    Select the same ISO week across years and pivot values by year.

    The result is indexed by week, weekday, and settlement period, with one
    column per year. It is intended for comparing the same week across
    multiple years.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Long-form dataframe containing date, settlement-period, and value
        columns.
    week : int or None, default None
        ISO week number to select.
    date_col : str, default 'Date'
        Name of the datetime-like date column.
    sp_col : str, default 'SP'
        Name of the settlement period column.
    value_col : str, default 'TD'
        Name of the value column to pivot.
    average_col : bool, default True
        If ``True``, add an `Average` column.
    average_all : bool, default False
        If ``True``, average over all year columns. If ``False``, exclude the
        most recent year column from the average.
    average_type : {'int', 'float'}, default 'int'
        Output dtype used for the `Average` column.
    make_week_full : bool, default True
        If ``True``, reindex the result to a complete seven-day week of 48
        settlement periods per day.
    replace_zero : int, float, or str, default 'nan'
        Value used to replace zeros. If ``'nan'``, zeros are replaced with
        `numpy.nan`.
    periods_per_day : int, default 48
        Number of periods per day used when filling an incomplete week.
        
    Returns
    -------
    pandas.DataFrame
        Pivoted dataframe containing the selected week across available years.

    Examples
    --------
    Compare the same ISO week across years:

    >>> df = pd.DataFrame({
    ...     "Date": pd.to_datetime(["2023-01-02", "2024-01-01"]),
    ...     "SP": [1, 1],
    ...     "TD": [10, 20],
    ... })
    >>> result = select_weeks(df, week=1, average_col=False, make_week_full=False)
    >>> result.loc[(1, 0, 1), 2023]
    10.0

    Add a floating-point average over all year columns:

    >>> result = select_weeks(
    ...     df, week=1, average_all=True, average_type="float",
    ...     make_week_full=False
    ... )
    >>> result.loc[(1, 0, 1), "Average"]
    15.0

    """
    select_cols = ['Week','Day',sp_col]
    df_select = df.reset_index(drop=True).copy()
    
    select_week = df_select[date_col].dt.isocalendar()['week'] == week
    df_pivot = df_select.loc[select_week].copy()

    df_pivot = (
        add_columns(df_pivot, col=date_col)
        .drop(['DayYear', 'Delivery_Year'], axis=1)
        )

    df_pivot = df_pivot.pivot_table(
        values=value_col, 
        index=select_cols, 
        columns='Year'
        )

    df_pivot = _replace_zero_values(df_pivot, replace_zero)

    if make_week_full:
        df_pivot = df_pivot.reset_index(drop=False)
        df_holder = _full_week_index(
            week=week,
            sp_col=sp_col,
            periods_per_day=periods_per_day
            )
        df_pivot = df_holder.merge(df_pivot, how='left', on=select_cols)
        df_pivot = df_pivot.set_index(select_cols)
    
    if average_col:
        df_pivot = _add_average_column(
            df_pivot,
            average_all=average_all,
            average_type=average_type,
            )
    
    return df_pivot





def select_days(
        df: pd.DataFrame, 
        date: object = None, 
        date_col: str = 'Date',
        sp_col: str = 'SP',
        value_col: str = 'TD',
        average_col: bool = True,
        average_all: bool = False,
        replace_zero: ReplaceZeroValue = 'nan'
        ) -> pd.DataFrame:
    """
    Select the same weekday and ISO week across years.

    The selected day is identified from `date`, then matching rows are
    selected from all years present in `df`.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Long-form dataframe containing date, settlement-period, and value
        columns.
    date : object, default None
        Date-like value used to identify the target ISO week and weekday.
    date_col : str, default 'Date'
        Name of the datetime-like date column.
    sp_col : str, default 'SP'
        Name of the settlement period column.
    value_col : str, default 'TD'
        Name of the value column to pivot.
    average_col : bool, default True
        If ``True``, add an `Average` column.
    average_all : bool, default False
        If ``True``, average over all year columns. If ``False``, exclude the
        most recent year column from the average.
    replace_zero : int, float, or str, default 'nan'
        Value used to replace zeros. If ``'nan'``, zeros are replaced with
        `numpy.nan`.
    
    Returns
    -------
    pandas.DataFrame
        Pivoted dataframe containing the matching day across available years.

    Examples
    --------
    Select matching Wednesdays from the same ISO week in all years:

    >>> df = pd.DataFrame({
    ...     "Date": pd.to_datetime(["2023-01-04", "2024-01-03"]),
    ...     "SP": [1, 1],
    ...     "TD": [10, 20],
    ... })
    >>> result = select_days(df, date="2024-01-03", average_col=False)
    >>> result.index.get_level_values("Day").unique().tolist()
    [2]

    """
    selected_date = pd.to_datetime(date)
    selected_week = selected_date.isocalendar()[1]
    
    selected_day = selected_date.dayofweek
    
    df_weeks = select_weeks(
        df, 
        week=selected_week,
        date_col=date_col,
        sp_col=sp_col,
        value_col=value_col,
        average_col=average_col,
        average_all=average_all,
        replace_zero=replace_zero
        )
    
    df_day = df_weeks.loc[df_weeks.index.get_level_values('Day')==selected_day]
    
    return df_day
