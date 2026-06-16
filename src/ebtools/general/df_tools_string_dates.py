#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 12:31:01 2024

@author: eamonnbell
"""



from typing import Literal

import pandas as pd
import numpy as np





# ---- STRING date functions


Weekday = Literal['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']



def _to_timestamp(
        date: object = 'today'
        ) -> pd.Timestamp:
    """
    Convert a date-like value to a pandas timestamp.

    Parameters
    ----------
    date : object, default 'today'
        Date-like value accepted by `pandas.to_datetime`.

    Returns
    -------
    pandas.Timestamp
        Parsed timestamp.

    Examples
    --------
    Convert a date string to a timestamp:

    >>> _to_timestamp("2024-01-01")
    Timestamp('2024-01-01 00:00:00')

    Existing timestamp-like inputs are accepted:

    >>> _to_timestamp(pd.Timestamp("2024-06-15"))
    Timestamp('2024-06-15 00:00:00')

    """
    return pd.to_datetime(date)





def week_starting(
        df: pd.DataFrame, 
        week: int | None = None,
        year: int | None = None,
        date_col: str = 'Date',
        weekday: Weekday | str = 'Mon',
        return_format: str = '%d %B %Y'
        ) -> str:
    """
    Return the date for a selected weekday in an ISO week.

    The function searches `df[date_col]` for a row matching `year`, ISO
    `week`, and `weekday`, then returns that date as a formatted string.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing a datetime-like column.
    week : int or None, default None
        ISO week number to select.
    year : int or None, default None
        Calendar year to select.
    date_col : str, default 'Date'
        Name of the datetime column in `df`.
    weekday : {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}, default 'Mon'
        Weekday to return from the selected week.
    return_format : str, default '%d %B %Y'
        `strftime` format used for the returned date string.
    
    Returns
    -------
    str
        Selected date formatted according to `return_format`.

    Examples
    --------
    Return the Monday for a selected ISO week:

    >>> df = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=7)})
    >>> week_starting(df, week=1, year=2024)
    '01 January 2024'

    Select another weekday and return a custom format:

    >>> week_starting(df, week=1, year=2024, weekday="Wed", return_format="%Y-%m-%d")
    '2024-01-03'

    """
    
    df_use = df.copy().reset_index(drop=True)
    
    weekday_num = {
        'Mon' : 0,
        'Tue' : 1,
        'Wed' : 2,
        'Thu' : 3,
        'Fri' : 4,
        'Sat' : 5,
        'Sun' : 6        
        }
    
    date_index = np.flatnonzero(
        (df_use[date_col].dt.year==year) & 
        (df_use[date_col].dt.isocalendar()['week']==week) & 
        (df_use[date_col].dt.weekday==weekday_num[weekday])
        )[0]
    
    return df_use.at[date_index, date_col].strftime(return_format)





def week_number(
        date: object = 'today'
        ) -> int:
    """
    Return the ISO week number for a date.

    Parameters
    ----------
    date : object, default 'today'
        Date-like value accepted by `pandas.to_datetime`.

    Returns
    -------
    int
        ISO week number, from 1 to 53.

    Examples
    --------
    Return the ISO week number for a date:

    >>> week_number("2024-01-01")
    1

    ISO week years can cross calendar-year boundaries:

    >>> week_number("2024-12-31")
    1

    """
    return _to_timestamp(date).isocalendar().week





def weekday_number(
        date: object = 'today'
        ) -> int:
    """
    Return the weekday number for a date.

    Parameters
    ----------
    date : object, default 'today'
        Date-like value accepted by `pandas.to_datetime`.

    Returns
    -------
    int
        Weekday number, where Monday is 0 and Sunday is 6.

    Examples
    --------
    Monday is represented as 0:

    >>> weekday_number("2024-01-01")
    0

    Sunday is represented as 6:

    >>> weekday_number("2024-01-07")
    6

    """
    return _to_timestamp(date).dayofweek





def day_of_the_year_number(
        date: object = 'today'
        ) -> int:
    """
    Return the day-of-year number for a date.

    Parameters
    ----------
    date : object, default 'today'
        Date-like value accepted by `pandas.to_datetime`.

    Returns
    -------
    int
        Day-of-year number, from 1 to 365 or 366.

    Examples
    --------
    The first day of a year is 1:

    >>> day_of_the_year_number("2024-01-01")
    1

    Leap years can have day 366:

    >>> day_of_the_year_number("2024-12-31")
    366

    """
    return _to_timestamp(date).dayofyear
