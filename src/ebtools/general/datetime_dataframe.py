#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datetime helper functions.
"""

import pandas as pd

from ebtools.general.datetime_conversion import move_date_to_start_of_month


def _settlement_period_start_values(
        values: object
        ) -> pd.Series:
    """
    Return datetime values floored to 30-minute settlement-period starts.
    """
    return pd.to_datetime(values).dt.floor('30min')


def _date_parts_from_columns(
        df: pd.DataFrame,
        year_col: str,
        month_col: str,
        day_col: str | None
        ) -> pd.DataFrame:
    """
    Return year, month, and day columns suitable for `pandas.to_datetime`.
    """
    return pd.DataFrame(
        {
            'year': df[year_col],
            'month': df[month_col],
            'day': 1 if day_col is None else df[day_col],
        },
        index=df.index,
        )


def convert_datetime_sp_start(
        df: pd.DataFrame,
        colname: str
        ) -> pd.DataFrame:
    """
    Add settlement-period start datetimes from a dataframe datetime column.

    Settlement periods are treated as 30-minute intervals. The new
    ``'SP_start_datetime'`` column contains each value in `colname` rounded
    down to the start of its containing settlement period.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime column.
    colname : str
        Name of the datetime column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with an added ``'SP_start_datetime'`` column.

    Examples
    --------
    Add the start of each containing settlement period:

    >>> df = pd.DataFrame({"Date": ["2024-03-14 14:35:00"]})
    >>> convert_datetime_sp_start(df, colname="Date")["SP_start_datetime"].iloc[0]
    Timestamp('2024-03-14 14:30:00')

    """
    df = df.copy()
    df['SP_start_datetime'] = _settlement_period_start_values(df[colname])

    return df


def convert_datetime_sp_end(
        df: pd.DataFrame,
        colname: str
        ) -> pd.DataFrame:
    """
    Add settlement-period end datetimes from a dataframe datetime column.

    Settlement periods are treated as 30-minute intervals. The new
    ``'SP_end_datetime'`` column contains the end of the settlement period
    containing each value in `colname`.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime column.
    colname : str
        Name of the datetime column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with an added ``'SP_end_datetime'`` column.

    Examples
    --------
    Add the end of each containing settlement period:

    >>> df = pd.DataFrame({"Date": ["2024-03-14 14:35:00"]})
    >>> convert_datetime_sp_end(df, colname="Date")["SP_end_datetime"].iloc[0]
    Timestamp('2024-03-14 15:00:00')

    The final settlement period in a day ends at midnight on the next day:

    >>> df = pd.DataFrame({"Date": ["2024-03-14 23:59:00"]})
    >>> convert_datetime_sp_end(df, colname="Date")["SP_end_datetime"].iloc[0]
    Timestamp('2024-03-15 00:00:00')

    """
    df = df.copy()
    df['SP_end_datetime'] = (
        _settlement_period_start_values(df[colname]) + pd.Timedelta(minutes=30)
        )

    return df





# ---- Check Datetime


def add_first_of_month_col_from_int_cols(
        df: pd.DataFrame,
        year_col: str,
        month_col: str,
        day_col: str | None = None,
        date_month_col_name: str = 'Date_Month'
        ) -> pd.DataFrame:
    """
    Add a datetime column from integer year, month, and optional day columns.

    If `day_col` is ``None``, the day is set to 1 for every row.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the integer date-part columns.
    year_col : str
        Name of the year column.
    month_col : str
        Name of the month column.
    day_col : str or None, default None
        Name of the day column. If ``None``, day 1 is used.
    date_month_col_name : str, default 'Date_Month'
        Name of the output datetime column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with an added datetime column.

    Examples
    --------
    Build a first-of-month column from year and month columns:

    >>> df = pd.DataFrame({"Year": [2024], "Month": [2]})
    >>> add_first_of_month_col_from_int_cols(
    ...     df, year_col="Year", month_col="Month"
    ... )["Date_Month"].iloc[0]
    Timestamp('2024-02-01 00:00:00')

    Include a day column when the exact day should be preserved:

    >>> df = pd.DataFrame({"Year": [2024], "Month": [2], "Day": [15]})
    >>> add_first_of_month_col_from_int_cols(
    ...     df, year_col="Year", month_col="Month", day_col="Day"
    ... )["Date_Month"].iloc[0]
    Timestamp('2024-02-15 00:00:00')

    """
    df = df.copy()

    date_parts = _date_parts_from_columns(
        df,
        year_col=year_col,
        month_col=month_col,
        day_col=day_col,
        )

    df[date_month_col_name] = pd.to_datetime(date_parts)

    return df


def add_first_of_month_col_from_date_col(
        df: pd.DataFrame,
        date_col: str,
        date_month_col_name: str = 'Date_Month'
        ) -> pd.DataFrame:
    """
    Add a first-of-month datetime column from an existing date column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the source date column.
    date_col : str
        Name of the source date column.
    date_month_col_name : str, default 'Date_Month'
        Name of the output first-of-month column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with an added first-of-month datetime column.

    Examples
    --------
    Add a first-of-month column from an existing date column:

    >>> df = pd.DataFrame({"Date": ["2024-02-15"]})
    >>> add_first_of_month_col_from_date_col(df, date_col="Date")["Date_Month"].iloc[0]
    Timestamp('2024-02-01 00:00:00')

    """
    df = df.copy()

    df[date_month_col_name] = move_date_to_start_of_month(df[date_col])

    return df
