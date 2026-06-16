#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datetime helper functions.
"""

import pandas as pd


def _roll_back_timestamp_by_month(
        date: object,
        n_months: int
        ) -> pd.Timestamp | pd.Series:
    """
    Return `date` shifted backward by `n_months` calendar months.
    """
    return pd.to_datetime(date) - pd.tseries.offsets.DateOffset(months=n_months)


def start_of_delivery_year(
        date: object
        ) -> pd.Timestamp:
    """
    Return the start date of the UK electricity delivery year containing a date.

    The delivery year starts on 1 April. Dates from April through December
    return 1 April of the same calendar year. Dates from January through March
    return 1 April of the previous calendar year.

    Parameters
    ----------
    date : object
        Date-like value accepted by `pandas.to_datetime`.

    Returns
    -------
    pandas.Timestamp
        Timestamp for 1 April at the start of the delivery year containing
        `date`.

    Examples
    --------
    Dates from January to March belong to the delivery year that started in
    the previous calendar year:

    >>> start_of_delivery_year("2024-03-31")
    Timestamp('2023-04-01 00:00:00')

    Dates from April onward belong to the delivery year starting in the same
    calendar year:

    >>> start_of_delivery_year("2024-04-01")
    Timestamp('2024-04-01 00:00:00')

    """
    date = pd.to_datetime(date)
    start_year = date.year if date.month >= 4 else date.year - 1

    return pd.Timestamp(start_year, 4, 1)


def roll_back_by_month_str(
        date: object, 
        n_months: int,
        as_string: bool = True
        ) -> str | pd.Timestamp:
    """
    Roll a date backward by a number of calendar months.

    Month-end dates are handled using pandas `DateOffset`, so invalid target
    dates are adjusted to the end of the target month.
    
    Parameters
    ----------
    date : object
        Date-like value accepted by `pandas.to_datetime`.
    n_months : int
        Number of calendar months to subtract from `date`.
    as_string : bool, default True
        If ``True``, return the result as ``'YYYY-MM-DD'``. If ``False``,
        return a `pandas.Timestamp`.

    Returns
    -------
    str or pandas.Timestamp
        Date shifted backward by `n_months` calendar months.

    Examples
    --------
    Roll a date back and return the default string output:

    >>> roll_back_by_month_str("2024-03-31", n_months=1)
    '2024-02-29'

    Return a `pandas.Timestamp` instead:

    >>> roll_back_by_month_str("2024-03-31", n_months=1, as_string=False)
    Timestamp('2024-02-29 00:00:00')

    """
    date = _roll_back_timestamp_by_month(date, n_months=n_months)
    
    # Convert to a Timestamp object if required
    if as_string:
        date = date.strftime('%Y-%m-%d')
    
    return date


def roll_back_by_month_df(
        df: pd.DataFrame,
        col_name: str,
        n_months: int,
        date_format: str = '%Y-%m-%d'
        ) -> pd.DataFrame:
    """
    Roll a dataframe date column backward by a number of calendar months.

    The column is parsed with `pandas.to_datetime` and shifted backward using
    pandas `DateOffset`.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the date column to update.
    col_name : str
        Name of the date column to shift.
    n_months : int
        Number of calendar months to subtract from each date.
    date_format : str, default '%Y-%m-%d'
        Format string used when parsing the date column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with `col_name` shifted backward by `n_months`
        calendar months.

    Examples
    --------
    Shift a date column backward while leaving the input dataframe unchanged:

    >>> df = pd.DataFrame({"date": ["2024-03-31"], "value": [1]})
    >>> result = roll_back_by_month_df(df, col_name="date", n_months=1)
    >>> result.loc[0, "date"]
    Timestamp('2024-02-29 00:00:00')

    """
    df = df.copy()

    # Parse the source column and shift each value backward by the requested
    # number of calendar months.
    df[col_name] = _roll_back_timestamp_by_month(
        pd.to_datetime(df[col_name], format=date_format),
        n_months=n_months,
        )
    
    return df


