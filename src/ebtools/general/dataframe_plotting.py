#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

import pandas as pd
import numpy as np

import ebtools.data as data
from ebtools.general.dataframe_dates import add_buffer_days
from ebtools.general.dataframe_helpers import _date_range_frequency
from ebtools.general.dataframe_selection import select_year



# ---- Dataframe - Analysis and Plotting





def _efa_start_date(
        df: pd.DataFrame,
        start_date: pd.Timestamp,
        start_fill: bool
        ) -> str:
    """
    Return the delivery date used to start an EFA-frequency range.
    """
    start_year = start_date.year

    if start_fill:
        check_date = pd.to_datetime(f'{start_year}-12-31 23:00:00')
        if df.index[0] == check_date:
            start_year += 1

        return f'{start_year}-01-01'

    if df.index[0].hour == 23:
        return (
            df.index[0].date() + pd.Timedelta('1D')
            ).strftime('%Y-%m-%d')

    return df.index[0].date().strftime('%Y-%m-%d')





def _full_year_date_bounds(
        df: pd.DataFrame,
        start_fill: bool,
        end_fill: bool,
        period: str
        ) -> tuple[str, str]:
    """
    Return start and end date strings for a complete plotting index.
    """
    start_date = df.index.min()
    end_date = df.index.max()

    if period == 'efa':
        start_date_use = _efa_start_date(
            df=df,
            start_date=start_date,
            start_fill=start_fill,
            )
    elif start_fill:
        start_date_use = f'{start_date.year}-01-01'
    else:
        start_date_use = start_date.strftime('%Y-%m-%d')

    if end_fill:
        end_date_use = f'{end_date.year}-12-31'
    else:
        end_date_use = end_date.strftime('%Y-%m-%d')

    # For periods smaller than a whole day, pd.date_range() stops at the start
    # of end_date_use, so add one day to include periods during that date.
    if period in ['efa', 'sp']:
        end_date_use = (
            pd.to_datetime(end_date_use) + pd.Timedelta('1D')
            ).strftime('%Y-%m-%d')

    return start_date_use, end_date_use





def make_full_year_pivot(
        df: pd.DataFrame,
        start_fill: bool = True,
        end_fill: bool = True,
        period: str = 'day',
        add_buffer: bool = False,
        buffer_days: int = 1
        ) -> pd.DataFrame:
    """
    Reindex a pivot dataframe to cover complete calendar-year ranges.

    The dataframe must have a datetime-like index. Missing rows introduced by
    reindexing are filled with `numpy.nan`.

    Parameters
    ----------
    df : pandas.DataFrame
        Pivot-style dataframe with a datetime-like index.
    start_fill : bool, default True
        If ``True``, extend the index to the start of the first calendar year.
    end_fill : bool, default True
        If ``True``, extend the index to the end of the last calendar year.
    period : {'day', 'efa', 'sp'}, default 'day'
        Frequency represented by the dataframe index.
    add_buffer : bool, default False
        If ``True``, add buffer days before and after the generated range.
    buffer_days : int, default 1
        Number of buffer days to add when `add_buffer` is ``True``.

    Returns
    -------
    pandas.DataFrame
        Reindexed dataframe covering the requested date range.

    Raises
    ------
    ValueError
        If `period` is not one of ``'day'``, ``'efa'``, or ``'sp'``.

    Examples
    --------
    >>> df = pd.DataFrame({"value": [1]}, index=pd.to_datetime(["2024-01-03"]))
    >>> make_full_year_pivot(df).index.min()
    Timestamp('2024-01-01 00:00:00')

    """
    period_use = period.lower()
    start_date_use, end_date_use = _full_year_date_bounds(
        df=df,
        start_fill=start_fill,
        end_fill=end_fill,
        period=period_use,
        )

    if add_buffer:
        start_date_use = add_buffer_days(
            start_date_use,
            direction='start',
            days=buffer_days,
            )
        end_date_use = add_buffer_days(
            end_date_use,
            direction='end',
            days=buffer_days,
            )

    # Create a full date range covering all days in all available years.
    new_df_index = pd.date_range(
        start=start_date_use,
        end=end_date_use,
        freq=_date_range_frequency(period_use),
        )

    if period_use == 'efa':
        new_df_index = new_df_index - pd.Timedelta('1H')

    return df.reindex(new_df_index)





def make_full_plotting_df(
        df: pd.DataFrame,
        year: int | None = None,
        month: int | None = None,
        calendar_year: bool | None = None,
        period: str = 'day',
        add_buffer: bool = False,
        buffer_days: int = 1
        ) -> pd.DataFrame:
    """
    Build a date-complete dataframe for plotting.

    The input should be a pivot-style dataframe with a datetime-like index.
    The output can cover all available data, a selected calendar year, or one
    selected month within a year.

    Parameters
    ----------
    df : pandas.DataFrame
        Pivot-style dataframe with a datetime-like index.
    year : int or None, default None
        Calendar year to select. If ``None``, all available data is used.
    month : int or None, default None
        Month to select when `year` is provided.
    calendar_year : bool or None, default None
        If ``True``, fill to calendar-year boundaries. If ``None``, treated as
        ``False``.
    period : {'day', 'efa', 'sp'}, default 'day'
        Frequency represented by the dataframe index.
    add_buffer : bool, default False
        If ``True``, add buffer days before and after the generated range.
    buffer_days : int, default 1
        Number of buffer days to add when `add_buffer` is ``True``.

    Returns
    -------
    pandas.DataFrame
        Plotting-ready dataframe with missing periods represented as `NaN`.

    Examples
    --------
    >>> index = pd.date_range("2024-01-01", "2024-01-31", freq="D")
    >>> df = pd.DataFrame({"value": range(len(index))}, index=index)
    >>> make_full_plotting_df(df, year=2024, month=1).index.min()
    Timestamp('2024-01-01 00:00:00')

    """
    period_use = period.lower()
    calendar_year_use = bool(calendar_year)

    if year is None:
        df_plot = make_full_year_pivot(
            df,
            start_fill=calendar_year_use,
            end_fill=calendar_year_use,
            period=period_use,
            add_buffer=add_buffer,
            buffer_days=buffer_days,
            )
    else:
        df_plot = select_year(
            df,
            year=year,
            full_year=calendar_year_use,
            period=period_use,
            add_buffer=add_buffer,
            buffer_days=buffer_days,
            )

        if month is not None:
            df_plot = df_plot.loc[(df_plot.index.month == month)].copy()

    return df_plot





def _calendar_month_holder(
        unit_value: int
        ) -> pd.DataFrame:
    """
    Return an empty six-week month layout for calendar plotting.

    Parameters
    ----------
    unit_value : int
        Number of intervals in each day.

    Returns
    -------
    pandas.DataFrame
        Holder dataframe with ``SP``, ``Weekday``, and ``Week`` columns.

    Examples
    --------
    >>> _calendar_month_holder(unit_value=2).head()
       SP  Weekday  Week
    0   1        0     0
    1   2        0     0
    2   1        1     0
    3   2        1     0
    4   1        2     0

    """
    weeks_per_month = 6
    days_per_week = 7

    return pd.DataFrame(
        {
            'SP': np.tile(
                np.arange(1, unit_value + 1),
                days_per_week * weeks_per_month,
                ),
            'Weekday': np.tile(
                np.repeat(np.arange(days_per_week), unit_value),
                weeks_per_month,
                ),
            'Week': np.repeat(
                np.arange(weeks_per_month),
                days_per_week * unit_value,
                ),
        }
    )





def _calendar_week_holder(
        unit_value: int
        ) -> pd.DataFrame:
    """
    Return an empty one-week layout for calendar plotting.

    Parameters
    ----------
    unit_value : int
        Number of intervals in each day.

    Returns
    -------
    pandas.DataFrame
        Holder dataframe with ``SP`` and ``Weekday`` columns.

    Examples
    --------
    >>> _calendar_week_holder(unit_value=2).head()
       SP  Weekday
    0   1        0
    1   2        0
    2   1        1
    3   2        1
    4   1        2

    """
    days_per_week = 7

    return pd.DataFrame(
        {
            'SP': np.tile(np.arange(1, unit_value + 1), days_per_week),
            'Weekday': np.repeat(np.arange(days_per_week), unit_value),
        }
    )





def _prepare_calendar_data(
        df: pd.DataFrame,
        year: int | None,
        full_year: bool
        ) -> pd.DataFrame:
    """
    Return melted calendar data with weekday and ISO week columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Pivot-style dataframe with a datetime-like index.
    year : int or None
        Calendar year to select. A year should be supplied by callers.
    full_year : bool
        If ``True``, reindex the selected year to a complete calendar year.

    Returns
    -------
    pandas.DataFrame
        Melted dataframe indexed by date, with ``SP``, ``value``,
        ``Weekday``, and ``Week`` columns.

    Examples
    --------
    >>> df = pd.DataFrame({1: [10]}, index=pd.to_datetime(["2024-01-01"]))
    >>> _prepare_calendar_data(df, year=2024, full_year=False).columns.to_list()
    ['SP', 'value', 'Weekday', 'Week']

    """
    df_cal = df.loc[(df.index.year == year)].copy()

    if full_year:
        df_cal = select_year(
            df_cal,
            year=year,
            full_year=full_year,
            )

    # Make sure the input data is labelled consistently before melting.
    df_cal = df_cal.rename_axis('Date', axis=0).rename_axis(None, axis=1)

    # Create a melted version of input df for processing.
    df_cal = df_cal.melt(ignore_index=False)
    df_cal = df_cal.rename(columns={'variable': 'SP'})
    df_cal = df_cal.sort_values(by=['Date', 'SP'])

    # Add weekday and ISO week labels for calendar alignment.
    df_cal['Weekday'] = df_cal.index.dayofweek
    df_cal['Week'] = df_cal.index.isocalendar().week

    return df_cal





def _normalise_month_weeks(
        df_month: pd.DataFrame,
        month: int
        ) -> pd.DataFrame:
    """
    Return month data with weeks numbered from zero within that month.

    Parameters
    ----------
    df_month : pandas.DataFrame
        Melted calendar data for one month, containing a ``Week`` column.
    month : int
        Calendar month number.

    Returns
    -------
    pandas.DataFrame
        Copy of `df_month` with normalized ``Week`` values.

    Examples
    --------
    >>> df = pd.DataFrame({"Week": [1, 1, 2]})
    >>> _normalise_month_weeks(df, month=2)["Week"].to_list()
    [0, 0, 1]

    """
    df_month = df_month.copy()

    # Correct January dates that belong to the final ISO week of the prior year.
    if (month == 1) and (df_month['Week'].iloc[0] >= 7):
        df_month['Week'] = np.where(
            df_month['Week'].to_numpy() >= 7,
            0,
            df_month['Week'].to_numpy(),
            )

    # Rebase the month so its first visible week is week zero.
    first_week = df_month['Week'].iloc[0]
    df_month['Week'] = df_month['Week'].to_numpy() - first_week
    week_values = set(df_month['Week'])

    # Correct dates in the final calendar week that roll into next ISO year.
    if min(week_values) < 0:
        df_month['Week'] = np.where(
            df_month['Week'].to_numpy() < 0,
            first_week + max(week_values) + min(week_values),
            df_month['Week'].to_numpy(),
            )

    return df_month





def _normalise_year_weeks(
        df_cal: pd.DataFrame
        ) -> pd.DataFrame:
    """
    Return year data with boundary ISO weeks adjusted for calendar plotting.

    Parameters
    ----------
    df_cal : pandas.DataFrame
        Melted calendar data with a datetime-like index and ``Week`` column.

    Returns
    -------
    pandas.DataFrame
        Copy of `df_cal` with January and December boundary ISO weeks adjusted.

    Examples
    --------
    >>> df = pd.DataFrame(
    ...     {"Week": [52, 1]},
    ...     index=pd.to_datetime(["2024-01-01", "2024-12-31"]),
    ... )
    >>> _normalise_year_weeks(df)["Week"].to_list()
    [0, 1]

    """
    df_cal = df_cal.copy()

    # Correct January dates that belong to the final ISO week of the prior year.
    df_cal['Week'] = np.where(
        (df_cal['Week'].to_numpy() >= 7) & (df_cal.index.month == 1),
        0,
        df_cal['Week'].to_numpy(),
        )

    # Correct December dates that belong to the first ISO week of the next year.
    if df_cal['Week'].iloc[-1] == 1:
        max_week_number = max(set(df_cal['Week']))
        df_cal['Week'] = np.where(
            (df_cal['Week'].to_numpy() == 1) & (df_cal.index.month == 12),
            max_week_number + 1,
            df_cal['Week'].to_numpy(),
            )

    return df_cal





def _month_calendar_pivot(
        df_cal: pd.DataFrame,
        unit_value: int
        ) -> pd.DataFrame:
    """
    Return a month-column calendar pivot from prepared calendar data.
    """
    df_cal_pivot = _calendar_month_holder(unit_value)
    months_in_data = set(df_cal.index.month)

    for month in range(1, 13):
        if month in months_in_data:
            df_month = df_cal.loc[(df_cal.index.month == month)].copy()
            df_month = _normalise_month_weeks(df_month, month=month)

            df_cal_pivot = pd.merge(
                df_cal_pivot,
                df_month,
                on=['SP', 'Weekday', 'Week'],
                how='left',
                )
            df_cal_pivot = df_cal_pivot.rename(columns={'value': month})
        else:
            df_cal_pivot[month] = np.nan

    return df_cal_pivot.drop(['SP', 'Weekday', 'Week'], axis=1)





def _week_calendar_pivot(
        df_cal: pd.DataFrame,
        unit_value: int
        ) -> pd.DataFrame:
    """
    Return a week-column calendar pivot from prepared calendar data.
    """
    df_cal_pivot = _calendar_week_holder(unit_value)
    df_cal = _normalise_year_weeks(df_cal)
    weeks_in_data = set(df_cal['Week'])

    for week in range(0, max(weeks_in_data) + 1):
        if week in weeks_in_data:
            df_week = (
                df_cal
                .loc[(df_cal['Week'] == week)]
                .copy()
                .drop('Week', axis=1)
                )

            df_cal_pivot = pd.merge(
                df_cal_pivot,
                df_week,
                on=['SP', 'Weekday'],
                how='left',
                )
            df_cal_pivot = df_cal_pivot.rename(columns={'value': week})
        else:
            df_cal_pivot[week] = np.nan

    return df_cal_pivot.drop(['SP', 'Weekday'], axis=1)





def make_pivot_calendar(
        df: pd.DataFrame,
        year: int | None = None,
        form: str = 'month',
        unit: str = 'hh',
        full_year: bool = True
        ) -> pd.DataFrame:
    """
    Reformat one year of pivot data for calendar-style plotting.

    The output aligns weekdays so monthly or weekly data can be compared in
    columns. Monday is treated as weekday 0 and Sunday as weekday 6.

    Parameters
    ----------
    df : pandas.DataFrame
        Pivot-style dataframe with a datetime-like index and interval columns.
    year : int or None, default None
        Calendar year to select.
    form : {'month', 'week'}, default 'month'
        Calendar layout to return.
    unit : {'hh', 'hour', 'efa'}, default 'hh'
        Interval unit represented by the input columns.
    full_year : bool, default True
        If ``True``, reindex the selected year to a complete calendar year.

    Returns
    -------
    pandas.DataFrame
        Calendar-aligned dataframe arranged by month or week.

    Raises
    ------
    KeyError
        If `unit` is not present in `ebtools.data.unit_dict`.
    ValueError
        If `form` is not ``'month'`` or ``'week'``.

    Examples
    --------
    >>> index = pd.date_range("2024-01-01", "2024-01-07", freq="D")
    >>> df = pd.DataFrame(np.ones((len(index), 48)), index=index, columns=range(1, 49))
    >>> make_pivot_calendar(df, year=2024, form="week", unit="hh").shape[0]
    336

    """
    unit_value = data.unit_dict[unit]

    # Melt the requested year and add calendar alignment columns.
    df_cal = _prepare_calendar_data(
        df=df,
        year=year,
        full_year=full_year,
        )

    if form == 'month':
        return _month_calendar_pivot(
            df_cal=df_cal,
            unit_value=unit_value,
            )

    if form == 'week':
        return _week_calendar_pivot(
            df_cal=df_cal,
            unit_value=unit_value,
            )

    raise ValueError("form must be 'month' or 'week'.")
