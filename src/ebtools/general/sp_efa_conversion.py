#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Settlement Period and EFA conversion functions."""

import pandas as pd
import numpy as np

from ebtools.general.datetime_conversion import convert_single_datetime_to_sp_start
from ebtools.general._sp_efa_helpers import (
    as_integer_array,
    return_scalar_or_array,
    validate_range,
    validate_sp_values,
)


def sp_to_efa(
        sp: int | list[int] | np.ndarray
        ) -> int | np.ndarray:
    """
    Convert Settlement Period values to EFA block values.

    Settlement Periods are half-hour periods numbered 1 to 48. EFA blocks are
    four-hour blocks numbered 1 to 6. SP 47 and SP 48 are mapped to EFA 1,
    reflecting the EFA day convention.

    Parameters
    ----------
    sp : int, list of int, or numpy.ndarray
        Settlement Period value or values. Each value must be in the range
        1 to 48.

    Returns
    -------
    int or numpy.ndarray
        EFA block value or values. A scalar integer is returned when `sp` is
        passed as an integer. A NumPy array is returned for list or array
        inputs.

    Raises
    ------
    ValueError
        If any Settlement Period value is outside the range 1 to 48.
    ValueError
        If any Settlement Period value is not integer-like.

    Examples
    --------
    >>> sp_to_efa(1)
    1

    >>> sp_to_efa(47)
    1

    >>> sp_to_efa([1, 8, 23, 47])
    array([1, 2, 4, 1])

    """
    sp_is_int = isinstance(sp, int)
    sp_int = as_integer_array(sp, "sp")
    validate_range(sp_int, "sp", 1, 48)

    # Convert SPs into EFA blocks, then wrap SP 47 and 48 from block 7 to 1.
    arr_sp = ((sp_int + 1) // 8) + 1
    arr_efa = np.where(arr_sp == 7, 1, arr_sp).astype(int)

    return return_scalar_or_array(arr_efa, sp_is_int)


def hour_to_efa(
        hour: int | list[int] | np.ndarray,
        first_hour: int = 0
        ) -> int | np.ndarray:
    """
    Convert hour values to EFA block values.

    EFA blocks are four-hour blocks numbered 1 to 6. The final hour block of
    the calendar day wraps to EFA 1 under the EFA day convention.

    Parameters
    ----------
    hour : int, list of int, or numpy.ndarray
        Hour value or values to convert.
    first_hour : {0, 1}, default 0
        Hour numbering convention. Use ``0`` when hours are represented as
        ``0`` to ``23``. Use ``1`` when hours are represented as ``1`` to
        ``24``.

    Returns
    -------
    int or numpy.ndarray
        EFA block value or values. A scalar integer is returned when `hour` is
        passed as an integer. A NumPy array is returned for list or array
        inputs.

    Raises
    ------
    ValueError
        If `first_hour` is not ``0`` or ``1``.
    ValueError
        If any hour value is not integer-like.
    ValueError
        If any hour value is outside the valid range for `first_hour`.

    Examples
    --------
    >>> hour_to_efa(0)
    1

    >>> hour_to_efa(23)
    1

    >>> hour_to_efa([0, 4, 12, 23])
    array([1, 2, 4, 1])

    >>> hour_to_efa(24, first_hour=1)
    1

    """
    if first_hour not in {0, 1}:
        raise ValueError("first_hour must be 0 or 1.")

    hour_is_int = isinstance(hour, int)
    hour_int = as_integer_array(hour, "hour")

    min_hour = first_hour
    max_hour = 23 + first_hour
    validate_range(hour_int, "hour", min_hour, max_hour)

    factor = {
        0: 1,
        1: 0,
        }

    # Convert hours into EFA blocks, then wrap block 7 to EFA 1.
    arr_hour = ((hour_int + factor[first_hour]) // 4) + 1
    arr_efa = np.where(arr_hour == 7, 1, arr_hour).astype(int)

    return return_scalar_or_array(arr_efa, hour_is_int)


def current_sp(
        date_time: object | None = None
        ) -> int:
    """
    Return the Settlement Period containing a datetime.

    Settlement Periods are half-hour periods numbered 1 to 48.

    Parameters
    ----------
    date_time : object or None, default None
        Datetime-like value accepted by `pandas.to_datetime`. If ``None``,
        use the current local datetime.

    Returns
    -------
    int
        Settlement Period containing `date_time`.

    Examples
    --------
    >>> current_sp("2024-03-14 06:12:26")
    13

    >>> current_sp("2024-03-14 06:30:00")
    14

    """
    if date_time is None:
        date_use = pd.to_datetime('today')
    else:
        date_use = pd.to_datetime(date_time)

    # Floor to the start of the containing half-hour Settlement Period.
    sp_start = convert_single_datetime_to_sp_start(date_use)

    return int((sp_start.hour * 2) + (sp_start.minute // 30) + 1)


def current_efa(
        date_time: object | None = None
        ) -> int:
    """
    Return the EFA block containing a datetime.

    EFA blocks are four-hour blocks numbered 1 to 6.

    Parameters
    ----------
    date_time : object or None, default None
        Datetime-like value accepted by `pandas.to_datetime`. If ``None``,
        use the current local datetime.

    Returns
    -------
    int
        EFA block containing `date_time`.

    Examples
    --------
    >>> current_efa("2024-03-14 06:12:26")
    2

    >>> current_efa("2024-03-14 23:15:00")
    1

    """
    return int(sp_to_efa(current_sp(date_time)))


def make_sp_efa_table(
        date: object | None = None
        ) -> pd.DataFrame:
    """
    Return a Settlement Period and EFA lookup table for one date.

    Parameters
    ----------
    date : object or None, default None
        Date-like value accepted by `pandas.to_datetime`. If ``None``, use
        today's local date.

    Returns
    -------
    pandas.DataFrame
        Dataframe with ``'Datetime'``, ``'SP'``, and ``'EFA'`` columns.

    Examples
    --------
    >>> make_sp_efa_table("2024-03-14").head()
                 Datetime  SP  EFA
    0 2024-03-14 00:00:00   1    1
    1 2024-03-14 00:30:00   2    1

    """
    if date is None:
        start_date = pd.to_datetime('today').date()
    else:
        start_date = pd.to_datetime(date).date()

    sp_values = np.arange(1, 49)
    validate_sp_values(sp_values)

    return pd.DataFrame(
        {
            'Datetime': pd.date_range(start=start_date, periods=48, freq='30min'),
            'SP': sp_values,
            'EFA': sp_to_efa(sp_values),
        }
    )
