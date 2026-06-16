#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datetime helper functions.
"""

import pandas as pd

def convert_datetime_remove_tz_aware(
        df: pd.DataFrame,
        colname: str
        ) -> pd.DataFrame:
    """
    Remove timezone awareness from a dataframe datetime column.

    The clock times are not shifted. For example, ``2023-04-14
    07:30:00+00:00`` becomes ``2023-04-14 07:30:00``.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime column to update.
    colname : str
        Name of the datetime column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with `colname` converted to timezone-naive datetimes.

    Examples
    --------
    Remove timezone awareness without changing the displayed clock time:

    >>> df = pd.DataFrame({
    ...     "Date": pd.to_datetime(["2024-01-01 12:00:00+00:00"], utc=True)
    ... })
    >>> convert_datetime_remove_tz_aware(df, colname="Date").loc[0, "Date"]
    Timestamp('2024-01-01 12:00:00')

    Already timezone-naive datetime columns are returned unchanged:

    >>> df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01 12:00:00"])})
    >>> convert_datetime_remove_tz_aware(df, colname="Date").loc[0, "Date"]
    Timestamp('2024-01-01 12:00:00')

    """
    df = df.copy()

    # Remove timezone awareness only when the column has a timezone-aware dtype.
    colname_tz = df[colname].dt.tz
    if colname_tz is not None:
        df[colname] = df[colname].dt.tz_localize(None)
    
    return df


def convert_datetime_by_tz(
        df: pd.DataFrame, 
        colname: str = 'Date',
        use_tz: str = 'Europe/London'
        ) -> pd.DataFrame:
    """
    Convert a UTC datetime column to a local timezone and remove timezone awareness.

    The input column is treated as UTC. It is localized to UTC, converted to
    `use_tz`, and then made timezone-naive while preserving the converted
    local clock time.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime column to update.
    colname : str, default 'Date'
        Name of the datetime column.
    use_tz : str, default 'Europe/London'
        Timezone to convert the UTC datetimes into.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with `colname` converted to timezone-naive local datetimes.

    Examples
    --------
    Convert UTC datetimes to Europe/London local clock time:

    >>> df = pd.DataFrame({"Date": pd.to_datetime(["2024-07-01 12:00:00"])})
    >>> convert_datetime_by_tz(df, colname="Date").loc[0, "Date"]
    Timestamp('2024-07-01 13:00:00')

    Winter dates remain aligned with UTC in Europe/London:

    >>> df = pd.DataFrame({"Date": pd.to_datetime(["2024-12-01 12:00:00"])})
    >>> convert_datetime_by_tz(df, colname="Date").loc[0, "Date"]
    Timestamp('2024-12-01 12:00:00')

    """
    df = df.copy()
    init_col_list = [x for x in df.columns]
    
    df[colname] = (
        df[colname]
        .dt.tz_localize('UTC')
        .dt.tz_convert(use_tz)
        )
    
    df[colname] = df[colname].dt.tz_localize(None)

    df = df.loc[:, init_col_list].copy()
    
    return df
