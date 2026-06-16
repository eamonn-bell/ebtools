#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datetime helper functions.
"""

import calendar
import datetime

import pandas as pd
import pytz

import ebtools.data as data


def _clock_change_date_for_year(
        clock_change_dates: pd.DatetimeIndex,
        year: int
        ) -> pd.Timestamp:
    """
    Return the configured clock-change date for `year`.
    """
    matching_dates = clock_change_dates[clock_change_dates.year == year]

    if matching_dates.empty:
        raise ValueError(f"No UK clock-change dates found for year {year}.")

    return matching_dates[0]


def is_year_leap_year(
        year: int
        ) -> bool:
    """
    Return whether a year is a leap year.

    Parameters
    ----------
    year : int
        Calendar year.

    Returns
    -------
    bool
        ``True`` if `year` is a leap year, otherwise ``False``.

    Examples
    --------
    Leap years occur every four years, except most century years:

    >>> is_year_leap_year(2024)
    True
    >>> is_year_leap_year(1900)
    False
    >>> is_year_leap_year(2000)
    True

    """
    return calendar.isleap(year)


def get_daylight_savings_dates(
        region: str = 'Europe/London',
        as_pandas_timestamp: bool = True
        ) -> list[datetime.datetime] | pd.DatetimeIndex:
    """
    Return timezone transition dates for a pytz region.

    Parameters
    ----------
    region : str, default 'Europe/London'
        Timezone name understood by `pytz.timezone`.
    as_pandas_timestamp : bool, default True
        If ``True``, return the transition dates as a `pandas.DatetimeIndex`.
        If ``False``, return `datetime.datetime` values.

    Returns
    -------
    list of datetime.datetime or pandas.DatetimeIndex
        Timezone transition dates for `region`.

    Notes
    -----
    The transition list comes from the private pytz attribute
    ``_utc_transition_times``. The sentinel value
    ``datetime.datetime(1, 1, 1, 0, 0)`` is removed when present.

    Examples
    --------
    Return transition dates as a `pandas.DatetimeIndex`:

    >>> dates = get_daylight_savings_dates()
    >>> isinstance(dates, pd.DatetimeIndex)
    True

    Return raw `datetime.datetime` values instead:

    >>> dates = get_daylight_savings_dates(as_pandas_timestamp=False)
    >>> isinstance(dates[0], datetime.datetime)
    True

    """
    tz_list = list(pytz.timezone(region)._utc_transition_times)

    if tz_list[0]==datetime.datetime(1, 1, 1, 0, 0):
        tz_list.pop(0)

    if as_pandas_timestamp:
        tz_list = pd.to_datetime(tz_list)
    
    return tz_list


def bst_date_range(
        year: int
        ) -> pd.DatetimeIndex:
    """
    Return the date range covering British Summer Time for a year.

    The returned range starts on the UK spring clock-change date and ends on
    the UK autumn clock-change date for `year`.

    Parameters
    ----------
    year : int
        Calendar year for which to return the British Summer Time date range.

    Returns
    -------
    pandas.DatetimeIndex
        Daily date range from the spring clock-change date through the autumn
        clock-change date, inclusive.

    Raises
    ------
    ValueError
        If `year` is not present in the configured UK clock-change date lists.

    Examples
    --------
    Return the inclusive British Summer Time date range for a known year:

    >>> bst_range = bst_date_range(2024)
    >>> bst_range[0]
    Timestamp('2024-03-31 00:00:00')
    >>> bst_range[-1]
    Timestamp('2024-10-27 00:00:00')

    """
    clock_change_spring = pd.to_datetime(data.uk_clock_change_forward, format='%Y-%m-%d')
    clock_change_autumn = pd.to_datetime(data.uk_clock_change_backward, format='%Y-%m-%d')
    
    start_date = _clock_change_date_for_year(clock_change_spring, year=year)
    end_date = _clock_change_date_for_year(clock_change_autumn, year=year)
    
    bst_range = pd.date_range(start=start_date, end=end_date)
    
    return bst_range
