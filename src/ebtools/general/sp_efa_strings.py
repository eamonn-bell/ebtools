#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""String parsing functions for Settlement Period and EFA values."""

import pandas as pd
import numpy as np

import ebtools.general.helper as helper
from ebtools.general._sp_efa_helpers import return_scalar_or_array
from ebtools.general.sp_efa_conversion import sp_to_efa


def make_sp_from_string(
        time_str: str | list[str] | np.ndarray,
        time_format: str = '%H:%M',
        start: bool = True
        ) -> int | np.ndarray:
    """
    Convert time strings to Settlement Period values.

    Parameters
    ----------
    time_str : str, list of str, or numpy.ndarray
        Time string or strings to convert.
    time_format : str, default '%H:%M'
        Format used to parse `time_str`.
    start : bool, default True
        If ``True``, interpret each time as the start of a Settlement Period.
        If ``False``, interpret each time as the end of a Settlement Period.

    Returns
    -------
    int or numpy.ndarray
        Settlement Period value or values. A scalar integer is returned for a
        scalar string input. A NumPy array is returned for list or array input.

    Raises
    ------
    ValueError
        If any parsed time is not on a half-hour boundary.

    Examples
    --------
    >>> make_sp_from_string("15:00")
    31

    >>> make_sp_from_string("15:00", start=False)
    30

    >>> make_sp_from_string(["00:00", "00:30", "23:30"])
    array([ 1,  2, 48])

    """
    time_str_is_str = isinstance(time_str, str)

    # Convert scalar or list-like input to an array for vectorized parsing.
    time_array = helper.force_to_np_array(time_str)
    time_convert = pd.to_datetime(time_array, format=time_format)

    if not start:
        time_convert = time_convert - pd.Timedelta(minutes=30)

    arr_hour = time_convert.hour
    arr_minute = time_convert.minute

    if np.any(~np.isin(arr_minute, [0, 30])):
        raise ValueError("time_str values must be on a half-hour boundary.")

    arr_sp = (arr_hour * 2) + (arr_minute // 30) + 1
    arr_sp = np.asarray(arr_sp, dtype=int)

    return return_scalar_or_array(arr_sp, time_str_is_str)


def make_efa_from_string(
        time_str: str | list[str] | np.ndarray,
        time_format: str = '%H:%M',
        start: bool = True
        ) -> int | np.ndarray:
    """
    Convert time strings to EFA block values.

    Parameters
    ----------
    time_str : str, list of str, or numpy.ndarray
        Time string or strings to convert.
    time_format : str, default '%H:%M'
        Format used to parse `time_str`.
    start : bool, default True
        If ``True``, interpret each time as the start of a period. If
        ``False``, interpret each time as the end of a period.

    Returns
    -------
    int or numpy.ndarray
        EFA block value or values. A scalar integer is returned for a scalar
        string input. A NumPy array is returned for list or array input.

    Raises
    ------
    ValueError
        If any parsed time is not on a half-hour boundary.
    ValueError
        If the resulting Settlement Period values are invalid.

    Examples
    --------
    >>> make_efa_from_string("15:00")
    5

    >>> make_efa_from_string("15:00", start=False)
    4

    >>> make_efa_from_string(["00:00", "11:00", "23:30"])
    array([1, 4, 1])

    """
    sp = make_sp_from_string(time_str, time_format=time_format, start=start)
    return sp_to_efa(sp)
