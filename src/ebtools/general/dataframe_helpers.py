#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Private helpers shared by dataframe utility modules.
"""

import pandas as pd
import numpy as np


_DATE_RANGE_FREQUENCIES = {
    'day': 'D',
    'efa': '4h',
    'sp': '30min',
}


def _date_range_frequency(
        period: str
        ) -> str:
    """
    Return the pandas frequency string for a supported dataframe period.

    Parameters
    ----------
    period : str
        Period label. Supported values are ``'day'``, ``'efa'``, and ``'sp'``.
        Matching is case-insensitive.

    Returns
    -------
    str
        Pandas frequency string for `period`.

    Raises
    ------
    ValueError
        If `period` is not one of ``'day'``, ``'efa'``, or ``'sp'``.

    Examples
    --------
    >>> _date_range_frequency("day")
    'D'

    >>> _date_range_frequency("SP")
    '30min'

    """
    period_use = period.lower()

    if period_use not in _DATE_RANGE_FREQUENCIES:
        raise ValueError("period must be one of 'day', 'efa', or 'sp'.")

    return _DATE_RANGE_FREQUENCIES[period_use]


def _delivery_year_from_dates(
        date_values: object
        ) -> list[str]:
    """
    Return delivery-year labels for date-like values.

    Delivery years run from April to March. Dates from January to March are
    assigned to the previous start year.

    Parameters
    ----------
    date_values : object
        Date-like values accepted by `pandas.to_datetime`.

    Returns
    -------
    list of str
        Delivery-year labels in ``YYYY_YY`` format.

    Examples
    --------
    >>> _delivery_year_from_dates(pd.Series(["2024-01-01", "2024-04-01"]))
    ['2023_24', '2024_25']

    """
    date_values = pd.Series(pd.to_datetime(date_values))

    # Create the start and end years based on the April delivery-year boundary.
    delivery_start_year = np.where(
        date_values.dt.month.to_numpy() < 4,
        date_values.dt.year.to_numpy() - 1,
        date_values.dt.year.to_numpy()
        )
    delivery_end_year = np.where(
        date_values.dt.month.to_numpy() < 4,
        date_values.dt.year.to_numpy() % 100,
        (date_values.dt.year.to_numpy() + 1) % 100
        )

    # Format the delivery-year labels with two-digit end years.
    return [
        f'{start_year}_{end_year:02d}'
        for start_year, end_year in zip(
            delivery_start_year,
            delivery_end_year,
            strict=True
            )
        ]


def _full_week_index(
        week: int,
        sp_col: str,
        periods_per_day: int
        ) -> pd.DataFrame:
    """
    Return a complete week index dataframe for period data.

    Parameters
    ----------
    week : int
        ISO week number to assign to every row.
    sp_col : str
        Name of the period column to create.
    periods_per_day : int
        Number of periods in each day.

    Returns
    -------
    pandas.DataFrame
        Dataframe with ``Week``, ``Day``, and `sp_col` columns. The dataframe
        contains seven days of period rows.

    Examples
    --------
    >>> _full_week_index(week=1, sp_col="SP", periods_per_day=2)
       Week  Day  SP
    0     1    0   1
    1     1    0   2
    2     1    1   1
    3     1    1   2

    """
    no_of_days = 7

    # Create a complete seven-day holder for the requested period resolution.
    arr_week = np.full(periods_per_day * no_of_days, week, dtype=np.int64)
    arr_day = np.repeat(np.arange(no_of_days), periods_per_day)
    arr_period = np.tile(np.arange(1, periods_per_day + 1), no_of_days)

    # Build the holder dataframe used to left-join incomplete week data.
    return pd.DataFrame(
        data={
            'Week': arr_week,
            'Day': arr_day,
            sp_col: arr_period
            }
        )
