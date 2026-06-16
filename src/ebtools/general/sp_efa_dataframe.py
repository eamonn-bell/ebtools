#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DataFrame helpers for Settlement Period and EFA columns."""

import pandas as pd
import numpy as np

from ebtools.general._sp_efa_helpers import require_columns, validate_sp_values
from ebtools.general.datetime_dataframe import convert_datetime_sp_start
from ebtools.general.sp_efa_conversion import sp_to_efa
from ebtools.general.sp_efa_datetime import (
    convert_date_to_efa_datetime,
    convert_datetime_to_date_and_efa,
)


def add_sp_from_datetime_col(
        df: pd.DataFrame,
        datetime_col: str = 'Date'
        ) -> pd.DataFrame:
    """
    Add a Settlement Period column from a datetime column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime column.
    datetime_col : str, default 'Date'
        Name of the datetime column. Values must fall on half-hour boundaries.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with an added ``'SP'`` column.

    Raises
    ------
    KeyError
        If `datetime_col` is not present in `df`.
    ValueError
        If any datetime value is not on a half-hour boundary.

    Examples
    --------
    >>> df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01 00:00:00"])})
    >>> add_sp_from_datetime_col(df)
                     Date  SP
    0 2024-01-01 00:00:00   1

    """
    require_columns(df, [datetime_col])

    df = df.copy()
    values = pd.to_datetime(df[datetime_col])

    if np.any(~values.dt.minute.isin([0, 30])):
        raise ValueError("datetime values must be on a half-hour boundary.")

    df['SP'] = ((values.dt.hour * 2) + (values.dt.minute // 30) + 1).astype(int)

    return df


def add_sp_start_end_datetimes(
        df: pd.DataFrame,
        date_col: str = 'Date',
        sp_col: str = 'SP',
        position: str = 'both'
        ) -> pd.DataFrame:
    """
    Add Settlement Period start and/or end datetime columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing date and Settlement Period columns.
    date_col : str, default 'Date'
        Name of the date column.
    sp_col : str, default 'SP'
        Name of the Settlement Period column.
    position : {'start', 'end', 'both'}, default 'both'
        Which datetime columns to add.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with ``'SP_start'``, ``'SP_end'``, or both columns
        added.

    Raises
    ------
    KeyError
        If `date_col` or `sp_col` is not present in `df`.
    ValueError
        If `position` is not one of ``'start'``, ``'end'``, or ``'both'``.
    ValueError
        If any SP value is outside the range 1 to 48.

    Examples
    --------
    >>> df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01"]), "SP": [1]})
    >>> add_sp_start_end_datetimes(df)
            Date  SP   SP_start              SP_end
    0 2024-01-01   1 2024-01-01 2024-01-01 00:30:00

    """
    if position not in {'start', 'end', 'both'}:
        raise ValueError("position must be one of 'start', 'end', or 'both'.")

    require_columns(df, [date_col, sp_col])

    df = df.copy()
    dates = pd.to_datetime(df[date_col])
    sp_values = df[sp_col].astype(int)
    validate_sp_values(sp_values)

    if position in {'start', 'both'}:
        df['SP_start'] = dates + pd.to_timedelta((sp_values - 1) * 30, unit='m')

    if position in {'end', 'both'}:
        df['SP_end'] = dates + pd.to_timedelta(sp_values * 30, unit='m')

    return df


def add_sp_to_efa_column(
        df: pd.DataFrame,
        sp_col: str = 'SP'
        ) -> pd.DataFrame:
    """
    Add an EFA block column from a Settlement Period column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing a Settlement Period column.
    sp_col : str, default 'SP'
        Name of the Settlement Period column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with an added ``'EFA'`` column.

    Raises
    ------
    KeyError
        If `sp_col` is not present in `df`.
    ValueError
        If any SP value is invalid.

    Examples
    --------
    >>> df = pd.DataFrame({"SP": [1, 23, 47]})
    >>> add_sp_to_efa_column(df)
       SP  EFA
    0   1    1
    1  23    4
    2  47    1

    """
    require_columns(df, [sp_col])

    df = df.copy()
    df['EFA'] = sp_to_efa(df[sp_col].to_numpy())

    return df


def add_efa_datetime_col(
        df: pd.DataFrame,
        date_col: str = 'Date',
        efa_col: str = 'EFA'
        ) -> pd.DataFrame:
    """
    Add EFA start datetime strings from date and EFA columns.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing date and EFA block columns.
    date_col : str, default 'Date'
        Name of the date column.
    efa_col : str, default 'EFA'
        Name of the EFA block column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with an added ``'EFA_Datetime'`` column.

    Raises
    ------
    KeyError
        If `date_col` or `efa_col` is not present in `df`.
    ValueError
        If any EFA value is invalid.

    Examples
    --------
    >>> df = pd.DataFrame({"Date": ["2023-03-14"], "EFA": [1]})
    >>> add_efa_datetime_col(df)
             Date  EFA         EFA_Datetime
    0  2023-03-14    1  2023-03-13T23:00:00

    """
    require_columns(df, [date_col, efa_col])

    df = df.copy()

    df['EFA_Datetime'] = [
        convert_date_to_efa_datetime(date, efa=int(efa))
        for date, efa in zip(df[date_col], df[efa_col])
    ]

    return df


def add_date_efa_cols(
        df: pd.DataFrame,
        datetime_col: str
        ) -> pd.DataFrame:
    """
    Add delivery date and EFA block columns from EFA start datetimes.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing an EFA start datetime column.
    datetime_col : str
        Name of the datetime column. Values must start at valid EFA block
        times.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with added ``'Date'`` and ``'EFA'`` columns.

    Raises
    ------
    KeyError
        If `datetime_col` is not present in `df`.
    ValueError
        If any datetime value does not start at a valid EFA block time.

    Examples
    --------
    >>> df = pd.DataFrame({"Datetime": ["2023-03-13T23:00:00"]})
    >>> add_date_efa_cols(df, datetime_col="Datetime")
                  Datetime        Date  EFA
    0  2023-03-13T23:00:00  2023-03-14    1

    """
    require_columns(df, [datetime_col])

    df = df.copy()

    date_efa_values = [
        convert_datetime_to_date_and_efa(date_time)
        for date_time in df[datetime_col]
    ]

    df[['Date', 'EFA']] = pd.DataFrame(date_efa_values, index=df.index)

    return df


def add_sp_and_efa_from_datetime(
        df: pd.DataFrame,
        colname: str
        ) -> pd.DataFrame:
    """
    Add Settlement Period and EFA columns from a datetime column.

    The datetime values are first floored to the start of their containing
    half-hour Settlement Period.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime column.
    colname : str
        Name of the datetime column.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with added ``'SP'`` and ``'EFA'`` columns.

    Raises
    ------
    KeyError
        If `colname` is not present in `df`.
    ValueError
        If generated SP values are invalid.

    Examples
    --------
    >>> df = pd.DataFrame({"Datetime": pd.to_datetime(["2023-03-14 11:15:00"])})
    >>> add_sp_and_efa_from_datetime(df, colname="Datetime")
                 Datetime  SP  EFA
    0 2023-03-14 11:15:00  23    4

    """
    require_columns(df, [colname])

    # Create a temporary column with the start of the containing SP.
    df = convert_datetime_sp_start(df, colname=colname)

    # Add SP and EFA columns, then remove the temporary datetime column.
    df = add_sp_from_datetime_col(df, datetime_col='SP_start_datetime')
    df = add_sp_to_efa_column(df, sp_col='SP')
    df = df.drop('SP_start_datetime', axis=1)

    return df
