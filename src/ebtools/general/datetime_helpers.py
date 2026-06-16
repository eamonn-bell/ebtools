#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datetime helper functions.
"""

from typing import Literal

import pandas as pd

import ebtools.general.helper as helper


DayBoundary = Literal['start', 'end']
DatetimeParseSummary = dict[str, int | dict[str, int]]
MonthBoundary = Literal['start', 'end']
MonthBoundaryResult = pd.Timestamp | pd.Series | pd.DatetimeIndex


def _normalise_format_list(
        format_list: object,
        default: object
        ) -> list[str]:
    """
    Return a datetime format input as a list.

    If `format_list` is ``None``, `default` is used instead. The selected
    value is then passed through `helper.force_to_list`.

    Parameters
    ----------
    format_list : object
        Datetime format string, iterable of datetime format strings, or
        ``None``.
    default : object
        Default datetime format string or iterable of format strings used when
        `format_list` is ``None``.

    Returns
    -------
    list
        Datetime format values as a list.

    Examples
    --------
    Use the default formats when no explicit format is supplied:

    >>> _normalise_format_list(None, default="%Y-%m-%d")
    ['%Y-%m-%d']

    Preserve multiple explicit formats:

    >>> _normalise_format_list(["%Y-%m-%d", "%d/%m/%Y"], default="%Y-%m-%d")
    ['%Y-%m-%d', '%d/%m/%Y']

    """
    if format_list is None:
        format_list = default
    return helper.force_to_list(format_list)


def _validate_format_list(
        format_list: list[str],
        name: str
        ) -> None:
    """
    Validate that a datetime format list contains at least one value.

    Parameters
    ----------
    format_list : list
        List of datetime format strings to validate.
    name : str
        Name of the argument being validated. Used in the error message.

    Raises
    ------
    ValueError
        If `format_list` is empty.

    Examples
    --------
    Non-empty format lists pass validation:

    >>> _validate_format_list(["%Y-%m-%d"], name="format_list")

    Empty format lists raise a `ValueError`:

    >>> _validate_format_list([], name="format_list")
    Traceback (most recent call last):
    ...
    ValueError: format_list must contain at least one datetime format.

    """
    if len(format_list) == 0:
        raise ValueError(f"{name} must contain at least one datetime format.")


def _replace_column_with_temp(
        df: pd.DataFrame,
        colname: str,
        temp_colname: str
        ) -> pd.DataFrame:
    """
    Replace a dataframe column with a temporary column.

    The original column is dropped and `temp_colname` is renamed to `colname`.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing both the original and temporary columns.
    colname : str
        Name of the original column to replace.
    temp_colname : str
        Name of the temporary column to rename.

    Returns
    -------
    pandas.DataFrame
        Dataframe with `temp_colname` renamed to `colname`.

    Examples
    --------
    Replace an original column with a parsed temporary column:

    >>> df = pd.DataFrame({
    ...     "date": ["raw"],
    ...     "date_correct": [pd.Timestamp("2024-01-01")],
    ... })
    >>> _replace_column_with_temp(df, "date", "date_correct").columns.to_list()
    ['date']

    """
    return df.drop(colname, axis=1).rename(columns={temp_colname: colname})


def _restore_column_order(
        df: pd.DataFrame,
        column_order: list[str]
        ) -> pd.DataFrame:
    """
    Return a dataframe with columns in a specified order.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe whose columns should be reordered.
    column_order : list of str
        Column names in the desired order.

    Returns
    -------
    pandas.DataFrame
        Copy of `df` with columns reordered to match `column_order`.

    Examples
    --------
    Restore a dataframe to a known column order:

    >>> df = pd.DataFrame({"b": [2], "a": [1]})
    >>> _restore_column_order(df, ["a", "b"]).columns.to_list()
    ['a', 'b']

    """
    return df.loc[:, column_order].copy()


def _date_to_day_boundary(
        date: object,
        position: DayBoundary | str,
        date_format: str = '%Y-%m-%d',
        smallest_time_unit: str = '1s'
        ) -> pd.Timestamp:
    """
    Return the start or end boundary for a date's day.

    Parameters
    ----------
    date : object
        Date-like value accepted by `pandas.to_datetime`.
    position : {'start', 'end'}
        Boundary to return. Use ``'start'`` for midnight at the start of the
        day, or ``'end'`` for the final representable point in the day based
        on `smallest_time_unit`.
    date_format : str, default '%Y-%m-%d'
        Format string used when parsing `date`.
    smallest_time_unit : str, default '1s'
        Time interval subtracted from the next day when `position='end'`.

    Returns
    -------
    pandas.Timestamp
        Timestamp at the requested day boundary.

    Raises
    ------
    ValueError
        If `position` is not ``'start'`` or ``'end'``.

    Examples
    --------
    Return the start of a day:

    >>> _date_to_day_boundary("2024-03-14", position="start")
    Timestamp('2024-03-14 00:00:00')

    Return the end of a day:

    >>> _date_to_day_boundary("2024-03-14", position="end")
    Timestamp('2024-03-14 23:59:59')

    """
    date = pd.to_datetime(date, format=date_format)

    if position == 'start':
        return date

    if position == 'end':
        return date + pd.Timedelta('1D') - pd.Timedelta(smallest_time_unit)

    raise ValueError("position must be 'start' or 'end'.")


def _date_to_month_boundary(
        date: object,
        position: MonthBoundary | str
        ) -> MonthBoundaryResult:
    """
    Return the start or end boundary for date-like values' month.

    Parameters
    ----------
    date : object
        Scalar date-like value, pandas Series, or pandas DatetimeIndex
        accepted by `pandas.to_datetime`.
    position : {'start', 'end'}
        Month boundary to return. Use ``'start'`` for the first day of the
        month or ``'end'`` for the last day of the month.

    Returns
    -------
    pandas.Timestamp, pandas.Series, or pandas.DatetimeIndex
        Date value or values moved to the requested month boundary.

    Raises
    ------
    ValueError
        If `position` is not ``'start'`` or ``'end'``.

    Examples
    --------
    Move a scalar date to the start of its month:

    >>> _date_to_month_boundary("2024-02-15", position="start")
    Timestamp('2024-02-01 00:00:00')

    Move a scalar date to the end of its month:

    >>> _date_to_month_boundary("2024-02-15", position="end")
    Timestamp('2024-02-29 00:00:00')

    """
    # Convert the input to pandas datetime values before month handling.
    date_values = pd.to_datetime(date)

    # Move scalar or Series values to the start of their month.
    if isinstance(date_values, pd.core.series.Series):
        start_of_month = date_values.dt.to_period('M').dt.to_timestamp()
    else:
        start_of_month = date_values.to_period('M').to_timestamp()

    if position == 'start':
        return start_of_month

    if position == 'end':
        return (
            pd.to_datetime(start_of_month)
            + pd.DateOffset(months=1)
            - pd.Timedelta('1D')
            )

    raise ValueError("position must be 'start' or 'end'.")


def _datetime_parse_summary(
        total_rows: int,
        unparsed_rows: int,
        parsed_by_format: dict[str, int]
        ) -> DatetimeParseSummary:
    """
    Return a standard datetime parsing summary dictionary.

    Parameters
    ----------
    total_rows : int
        Number of rows attempted.
    unparsed_rows : int
        Number of rows that could not be parsed.
    parsed_by_format : dict of str to int
        Number of rows parsed by each datetime format.

    Returns
    -------
    dict
        Summary containing ``total_rows``, ``parsed_rows``, ``unparsed_rows``,
        and ``parsed_by_format``.

    Examples
    --------
    Return a standard parse summary:

    >>> _datetime_parse_summary(3, 1, {"%Y-%m-%d": 2})
    {'total_rows': 3, 'parsed_rows': 2, 'unparsed_rows': 1, ...}

    """
    return {
        'total_rows': total_rows,
        'parsed_rows': total_rows - unparsed_rows,
        'unparsed_rows': unparsed_rows,
        'parsed_by_format': parsed_by_format,
    }
