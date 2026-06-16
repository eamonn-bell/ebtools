#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datetime helper functions.
"""

import datetime
from typing import Literal

import numpy as np
import pandas as pd

from ebtools.general.datetime_helpers import (
    _date_to_day_boundary,
    _date_to_month_boundary,
)


DayBoundary = Literal['start', 'end']
DateOnlyResult = datetime.date | pd.Timestamp | pd.Series | pd.DatetimeIndex | np.ndarray
MonthBoundaryResult = pd.Timestamp | pd.Series | pd.DatetimeIndex


def convert_single_datetime_to_sp_start(
        date: datetime.datetime
        ) -> datetime.datetime:
    """
    Return the start time of the settlement period containing a datetime.

    Settlement periods are treated as 30-minute intervals. Seconds and
    microseconds are discarded.

    Parameters
    ----------
    date : datetime.datetime
        Datetime to convert.

    Returns
    -------
    datetime.datetime
        Datetime rounded down to the start of the containing 30-minute
        settlement period.

    Examples
    --------
    Round a datetime down to the start of its settlement period:

    >>> convert_single_datetime_to_sp_start(datetime.datetime(2024, 3, 14, 14, 35))
    datetime.datetime(2024, 3, 14, 14, 30)

    Datetimes already on a half-hour boundary are unchanged:

    >>> convert_single_datetime_to_sp_start(datetime.datetime(2024, 3, 14, 20, 0))
    datetime.datetime(2024, 3, 14, 20, 0)

    """
    return datetime.datetime(
        date.year, 
        date.month, 
        date.day, 
        date.hour, 
        (date.minute//30)*30, 
        0
        )


def convert_single_datetime_to_sp_end(
        date: datetime.datetime
        ) -> datetime.datetime:
    """
    Return the end time of the settlement period containing a datetime.

    Settlement periods are treated as 30-minute intervals. The returned value
    is the start of the containing settlement period plus 30 minutes.

    Parameters
    ----------
    date : datetime.datetime
        Datetime to convert.

    Returns
    -------
    datetime.datetime
        Datetime at the end of the containing 30-minute settlement period.

    Examples
    --------
    Return the end of the containing settlement period:

    >>> convert_single_datetime_to_sp_end(datetime.datetime(2024, 3, 14, 14, 35))
    datetime.datetime(2024, 3, 14, 15, 0)

    The final settlement period in a day ends at midnight on the next day:

    >>> convert_single_datetime_to_sp_end(datetime.datetime(2024, 3, 14, 23, 59))
    datetime.datetime(2024, 3, 15, 0, 0)

    """
    return convert_single_datetime_to_sp_start(date) + datetime.timedelta(minutes=30)





# ---- Convert Datetime


def convert_date_to_standard_date_str(
        date: object = None
        ) -> str:
    """
    Convert a date-like value to a standard date string.

    Parameters
    ----------
    date : object, default None
        Date-like value accepted by `pandas.to_datetime`.

    Returns
    -------
    str
        Date formatted as ``'YYYY-MM-DD'``.

    Examples
    --------
    Convert datetime-like input to a date string:

    >>> convert_date_to_standard_date_str("2024-03-14 15:30:00")
    '2024-03-14'

    """
    return pd.to_datetime(date).strftime('%Y-%m-%d')


def convert_date_to_datetime(
        date: object = None,
        position: DayBoundary | str = 'start',
        date_format: str = '%Y-%m-%d',
        return_format: str = '%Y-%m-%d %H:%M:%S',
        smallest_time_unit: str = '1s'
        ) -> str:
    """
    Convert a date-like value to a start- or end-of-day datetime string.

    Parameters
    ----------
    date : object, default None
        Date-like value accepted by `pandas.to_datetime`.
    position : {'start', 'end'}, default 'start'
        Day boundary to return. Use ``'start'`` for midnight at the start of
        the day, or ``'end'`` for the final representable point in the day
        based on `smallest_time_unit`.
    date_format : str, default '%Y-%m-%d'
        Format string used when parsing `date`.
    return_format : str, default '%Y-%m-%d %H:%M:%S'
        Format string used for the returned datetime string.
    smallest_time_unit : str, default '1s'
        Time interval subtracted from the next day when `position='end'`.
        
    Returns
    -------
    str
        Datetime string formatted according to `return_format`.

    Raises
    ------
    ValueError
        If `position` is not ``'start'`` or ``'end'``.

    Examples
    --------
    Return the start of a day:

    >>> convert_date_to_datetime("2024-03-14", position="start")
    '2024-03-14 00:00:00'

    Return the end of a day:

    >>> convert_date_to_datetime("2024-03-14", position="end")
    '2024-03-14 23:59:59'

    """
    date_return = _date_to_day_boundary(
        date=date,
        position=position,
        date_format=date_format,
        smallest_time_unit=smallest_time_unit,
        )

    return date_return.strftime(return_format)


def convert_datetime_to_date(
        datetime_value: object = None,
        as_python_date: bool = False
        ) -> DateOnlyResult:
    """
    Convert datetime-like values to date-only values.

    Parameters
    ----------
    datetime_value : object, default None
        Datetime-like scalar, pandas Series, or dataframe column accepted by
        `pandas.to_datetime`.
    as_python_date : bool, default False
        If ``True``, return Python `datetime.date` values. If ``False``,
        return pandas datetime values normalised to midnight.

    Returns
    -------
    object
        Date-only value or values. Scalars return a scalar value. Series-like
        inputs return a pandas Series.

    Examples
    --------
    Normalise a scalar datetime to midnight:

    >>> convert_datetime_to_date("2024-03-14 15:30:00")
    Timestamp('2024-03-14 00:00:00')

    Return Python `datetime.date` values when requested:

    >>> convert_datetime_to_date("2024-03-14 15:30:00", as_python_date=True)
    datetime.date(2024, 3, 14)

    """
    datetime_values = pd.to_datetime(datetime_value)

    if isinstance(datetime_values, pd.Series):
        if as_python_date:
            return datetime_values.dt.date
        return datetime_values.dt.normalize()

    if as_python_date:
        return datetime_values.date()

    return datetime_values.normalize()


def convert_date_to_datetime_str(
        date: object = None,
        position: DayBoundary | str = 'start',
        date_format: str = '%Y-%m-%d',
        return_format: str = '%Y-%m-%dT%H:%M:%SZ',
        smallest_time_unit: str = '1s'
        ) -> str:
    """
    Convert a date-like value to an API-style datetime string.

    Parameters
    ----------
    date : object, default None
        Date-like value accepted by `pandas.to_datetime`.
    position : {'start', 'end'}, default 'start'
        Day boundary to return. Use ``'start'`` for midnight at the start of
        the day, or ``'end'`` for the final representable point in the day
        based on `smallest_time_unit`.
    date_format : str, default '%Y-%m-%d'
        Format string used when parsing `date`.
    return_format : str, default '%Y-%m-%dT%H:%M:%SZ'
        Format string used for the returned datetime string.
    smallest_time_unit : str, default '1s'
        Time interval subtracted from the next day when `position='end'`.

    Returns
    -------
    str
        Datetime string formatted according to `return_format`.

    Raises
    ------
    ValueError
        If `position` is not ``'start'`` or ``'end'``.

    Examples
    --------
    Format the start of a day for API-style datetime strings:

    >>> convert_date_to_datetime_str("2024-03-14", position="start")
    '2024-03-14T00:00:00Z'

    Format the end of a day:

    >>> convert_date_to_datetime_str("2024-03-14", position="end")
    '2024-03-14T23:59:59Z'

    """
    date = _date_to_day_boundary(
        date=date,
        position=position,
        date_format=date_format,
        smallest_time_unit=smallest_time_unit,
        ).strftime(return_format)
    
    return date


def convert_date_to_first_of_month(
        date: object,
        as_string: bool = True
        ) -> str | pd.Timestamp:
    """
    Return the first day of the month containing a date.

    Parameters
    ----------
    date : object
        Date-like value accepted by `pandas.to_datetime`.
    as_string : bool, default True
        If ``True``, return the result as ``'YYYY-MM-DD'``. If ``False``,
        return a `pandas.Timestamp`.

    Returns
    -------
    str or pandas.Timestamp
        First day of the month containing `date`.

    Examples
    --------
    Return the first of the month as a string:

    >>> convert_date_to_first_of_month("2024-02-15")
    '2024-02-01'

    Return a `pandas.Timestamp` instead:

    >>> convert_date_to_first_of_month("2024-02-15", as_string=False)
    Timestamp('2024-02-01 00:00:00')

    """
    
    new_date = move_date_to_start_of_month(date)

    if as_string:
        return new_date.strftime('%Y-%m-%d')

    return new_date


def convert_date_to_last_of_month(
        date: object,
        as_string: bool = True
        ) -> str | pd.Timestamp:
    """
    Return the last day of the month containing a date.

    Parameters
    ----------
    date : object
        Date-like value accepted by `pandas.to_datetime`.
    as_string : bool, default True
        If ``True``, return the result as ``'YYYY-MM-DD'``. If ``False``,
        return a `pandas.Timestamp`.

    Returns
    -------
    str or pandas.Timestamp
        Last day of the month containing `date`.

    Examples
    --------
    Return the last of the month as a string:

    >>> convert_date_to_last_of_month("2024-02-15")
    '2024-02-29'

    Return a `pandas.Timestamp` instead:

    >>> convert_date_to_last_of_month("2024-02-15", as_string=False)
    Timestamp('2024-02-29 00:00:00')

    """    
    new_date = move_date_to_end_of_month(date)

    if as_string:
        return new_date.strftime('%Y-%m-%d')

    return new_date


def move_date_to_start_of_month(
        date: object
        ) -> MonthBoundaryResult:
    """
    Move date-like values to the first day of their month.

    Parameters
    ----------
    date : object
        Scalar date-like value or pandas Series accepted by
        `pandas.to_datetime`.

    Returns
    -------
    pandas.Timestamp or pandas.Series
        Date value or values moved to the first day of their month.

    Examples
    --------
    Move a scalar date to the first day of its month:

    >>> move_date_to_start_of_month("2024-02-15")
    Timestamp('2024-02-01 00:00:00')

    """
    return _date_to_month_boundary(date, position='start')


def move_date_to_end_of_month(
        date: object
        ) -> MonthBoundaryResult:
    """
    Move date-like values to the last day of their month.

    Parameters
    ----------
    date : object
        Scalar date-like value or pandas Series accepted by
        `pandas.to_datetime`.

    Returns
    -------
    pandas.Timestamp or pandas.Series
        Date value or values moved to the last day of their month.

    Examples
    --------
    Move a scalar date to the last day of its month:

    >>> move_date_to_end_of_month("2024-02-15")
    Timestamp('2024-02-29 00:00:00')

    """
    return _date_to_month_boundary(date, position='end')
