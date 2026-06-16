#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

import pandas as pd

from ebtools.general.dataframe_helpers import _delivery_year_from_dates



# ---- Dataframe - Augmentation





def add_buffer_days(
        date: object,
        direction: str = 'start',
        days: int = 1
        ) -> str:
    """
    Add buffer days before or after a date.

    Parameters
    ----------
    date : object
        Date-like value accepted by `pandas.to_datetime`.
    direction : {'start', 'end'}, default 'start'
        Direction of the buffer. Use ``'start'`` to subtract days or ``'end'``
        to add days.
    days : int, default 1
        Number of days to add or subtract.

    Returns
    -------
    str
        Adjusted date formatted as ``'YYYY-MM-DD'``.

    Raises
    ------
    ValueError
        If `direction` is not ``'start'`` or ``'end'``.

    Examples
    --------
    >>> add_buffer_days("2024-01-10", direction="start", days=2)
    '2024-01-08'

    >>> add_buffer_days("2024-01-10", direction="end", days=3)
    '2024-01-13'

    """
    if direction not in ['start', 'end']:
        raise ValueError("direction must be 'start' or 'end'.")

    day_offset = -days if direction == 'start' else days
    
    return (
        pd.to_datetime(date) + pd.Timedelta(days=day_offset)
        ).strftime('%Y-%m-%d')
    




def add_columns(
        df: pd.DataFrame,
        col: str = 'Date'
        ) -> pd.DataFrame:
    """
    Add common date-derived columns to a dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe.
    col : str, default 'Date'
        Name of the datetime-like column used to derive the new columns.

    Returns
    -------
    pandas.DataFrame
        Copy of `df` with the following columns added:

        - ``Year``: calendar year.
        - ``Week``: ISO week number.
        - ``Day``: day of week, where Monday is 0 and Sunday is 6.
        - ``DayYear``: day of year.
        - ``Delivery_Year``: April-to-March delivery year.
        - ``Month_start``: first day of the calendar month.

    Raises
    ------
    KeyError
        If `col` is not present in `df`.

    Examples
    --------
    >>> df = pd.DataFrame({"Date": pd.to_datetime(["2024-04-01"])})
    >>> add_columns(df, col="Date")[["Year", "Delivery_Year"]].iloc[0].to_dict()
    {'Year': 2024, 'Delivery_Year': '2024_25'}

    """
    df = df.copy()
    date_values = pd.to_datetime(df[col])

    # Year column.
    df['Year'] = date_values.dt.year
    
    # ISO week number column.
    df['Week'] = date_values.dt.isocalendar().week

    # Day of week column, where Monday=0 and Sunday=6.
    df['Day'] = date_values.dt.dayofweek
        
    # Day of year column.
    df['DayYear'] = date_values.dt.dayofyear
    
    # April-to-March delivery year column.
    df['Delivery_Year'] = _delivery_year_from_dates(date_values)
    
    # First day of the calendar month.
    df['Month_start'] = date_values.dt.to_period('M').dt.to_timestamp()
    
    return df
