#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EFA date and datetime conversion functions."""

import pandas as pd

from ebtools.general._sp_efa_helpers import EFA_START_HOURS, TIME_TO_EFA


def convert_date_to_efa_datetime(
        date: object,
        efa: int = 1
        ) -> str:
    """
    Convert a delivery date and EFA block to an EFA start datetime string.

    EFA block 1 starts at 23:00 on the previous calendar day. EFA blocks 2 to
    6 start at 03:00, 07:00, 11:00, 15:00, and 19:00 on the delivery date.

    Parameters
    ----------
    date : object
        Delivery date accepted by `pandas.to_datetime`.
    efa : int, default 1
        EFA block number. Must be in the range 1 to 6.

    Returns
    -------
    str
        EFA block start datetime formatted as ``'%Y-%m-%dT%H:%M:%S'``.

    Raises
    ------
    ValueError
        If `efa` is outside the range 1 to 6.

    Examples
    --------
    >>> convert_date_to_efa_datetime("2023-03-14", efa=1)
    '2023-03-13T23:00:00'

    >>> convert_date_to_efa_datetime("2023-03-14", efa=4)
    '2023-03-14T11:00:00'

    """
    if efa not in EFA_START_HOURS:
        raise ValueError("efa must be in the range 1 to 6.")

    updated_date = pd.to_datetime(date) + pd.Timedelta(hours=EFA_START_HOURS[efa])

    return updated_date.strftime(format='%Y-%m-%dT%H:%M:%S')


def convert_datetime_to_date_and_efa(
        date_time: object
        ) -> tuple[str, int]:
    """
    Convert an EFA start datetime to a delivery date and EFA block.

    Parameters
    ----------
    date_time : object
        Datetime-like value accepted by `pandas.to_datetime`. The time
        component must be one of the valid EFA start times: 23:00, 03:00,
        07:00, 11:00, 15:00, or 19:00.

    Returns
    -------
    tuple of str and int
        Delivery date formatted as ``'%Y-%m-%d'`` and EFA block number.

    Raises
    ------
    ValueError
        If the time component is not a valid EFA start time.

    Examples
    --------
    >>> convert_datetime_to_date_and_efa("2023-03-13T23:00:00")
    ('2023-03-14', 1)

    >>> convert_datetime_to_date_and_efa("2023-03-14T11:00:00")
    ('2023-03-14', 4)

    """
    datetime_convert = pd.to_datetime(date_time, format='%Y-%m-%dT%H:%M:%S')
    time_part = datetime_convert.time()

    if time_part not in TIME_TO_EFA:
        raise ValueError("date_time must start at a valid EFA block time.")

    efa_part = TIME_TO_EFA[time_part]

    if efa_part == 1:
        datetime_convert = datetime_convert + pd.Timedelta(hours=1)

    date_part = datetime_convert.date().strftime('%Y-%m-%d')

    return (date_part, efa_part)
