#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

import pandas as pd
import numpy as np

import ebtools.data as data
from ebtools.general.dataframe_helpers import _delivery_year_from_dates



# ---- Dataframe - BASE





def _base_time_range(
        time_col_str: bool
        ) -> pd.Index | np.ndarray:
    """
    Return the normal-day Settlement Period start-time range.

    Parameters
    ----------
    time_col_str : bool
        If ``True``, return start times as ``'HH:MM'`` strings. If ``False``,
        return start times as `datetime.time` values.

    Returns
    -------
    pandas.Index or numpy.ndarray
        Forty-eight half-hourly start times from midnight. String output is
        returned as a pandas index; time output is returned as a NumPy array of
        `datetime.time` values.

    Examples
    --------
    >>> _base_time_range(time_col_str=True)[0]
    '00:00'

    >>> _base_time_range(time_col_str=False)[0]
    datetime.time(0, 0)

    """
    time_range = pd.date_range(
        start='00:00',
        periods=48,
        freq='30min',
        )

    if time_col_str:
        return time_range.strftime('%H:%M')

    return time_range.time





def _base_efa_range(
        no_of_days: int
        ) -> np.ndarray:
    """
    Return the normal-day EFA block range for a date range.

    Parameters
    ----------
    no_of_days : int
        Number of days over which to repeat the daily EFA block pattern.

    Returns
    -------
    numpy.ndarray
        EFA block values for `no_of_days` normal days, with 48 values per day.

    Examples
    --------
    >>> _base_efa_range(no_of_days=1)[:4]
    array([1, 1, 1, 1])

    >>> len(_base_efa_range(no_of_days=2))
    96

    """
    efa_blocks = np.arange(1, 7)
    sps_per_efa_block = 8
    efa_roll_offset = -2

    # EFA 1 starts at 23:00, so the daily EFA pattern is rolled back two
    # settlement periods relative to the calendar day.
    daily_efa = np.roll(
        np.repeat(efa_blocks, sps_per_efa_block),
        efa_roll_offset,
        )

    # Repeat the daily EFA pattern over the full date range.
    return np.tile(daily_efa, no_of_days)





def _resolve_date_bound(
        value: object | None,
        fallback: object
        ) -> str:
    """
    Return a date-bound value formatted as ``YYYY-MM-DD``.
    """
    if value is None:
        return str(fallback)

    return pd.to_datetime(value).strftime('%Y-%m-%d')





def _dates_between(
        dates: list[str],
        start_date: str,
        end_date: str
        ) -> list[str]:
    """
    Return date strings between two inclusive date bounds.
    """
    return [date for date in dates if start_date <= date <= end_date]





def _date_sp_mask(
        df: pd.DataFrame,
        date_col: str,
        sp_col: str,
        dates: list[str],
        sps: list[int]
        ) -> pd.Series:
    """
    Return a mask for rows matching date and Settlement Period values.
    """
    return df[date_col].isin(dates) & df[sp_col].isin(sps)





def adjust_for_clock_change(
        df: pd.DataFrame,
        start_date: object | None = None,
        end_date: object | None = None,
        date_col: str = 'Date',
        sp_col: str = 'SP'
        ) -> pd.DataFrame:
    """
    Adjust settlement periods for UK clock-change days.

    Spring clock-change days remove settlement periods 3 and 4. Autumn
    clock-change days duplicate settlement periods 3 and 4 and renumber later
    periods. Clock-change dates are read from `ebtools.data`.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing date and Settlement Period columns.
    start_date : object or None, default None
        First date to check. If ``None``, the minimum value in `date_col` is
        used.
    end_date : object or None, default None
        Last date to check. If ``None``, the maximum value in `date_col` is
        used.
    date_col : str, default 'Date'
        Name of the date column.
    sp_col : str, default 'SP'
        Name of the Settlement Period column.

    Returns
    -------
    pandas.DataFrame
        Dataframe adjusted to the correct number of Settlement Periods on UK
        clock-change days.

    Examples
    --------
    >>> df = pd.DataFrame({"Date": ["2024-03-31"] * 48, "SP": range(1, 49)})
    >>> len(adjust_for_clock_change(df, "2024-03-31", "2024-03-31"))
    46

    >>> df = pd.DataFrame({"Date": ["2024-10-27"] * 48, "SP": range(1, 49)})
    >>> len(adjust_for_clock_change(df, "2024-10-27", "2024-10-27"))
    50

    """
    
    df = df.copy()
    original_date_dtype = df[date_col].dtype
    df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%m-%d')

    # ====================================================================
    # Set up useful data
    # ====================================================================
    
    # Settlement Periods to adjust: 
    #   -- FORWARD  --> substract 2 from each SP
    #   -- BACKWARD --> add 2 to each SP
    sps_to_adjust = list(range(5, 49))
    
    # Set start_date and end_date if either passed as None.
    start_date = _resolve_date_bound(start_date, df[date_col].min())
    end_date = _resolve_date_bound(end_date, df[date_col].max())
    
    # Set up dates for CLOCK GOING FORWARDS - SPRING
    forward_dates_use = _dates_between(
        data.uk_clock_change_forward,
        start_date,
        end_date,
        )
    backward_dates_use = _dates_between(
        data.uk_clock_change_backward,
        start_date,
        end_date,
        )
    
    # ====================================================================
    # Adjust df for FORWARD CLOCK CHANGE
    # ====================================================================        
    
    if forward_dates_use:
        # Remove SPs 3 and 4 from spring clock-change dates.
        mask_forward = _date_sp_mask(
            df,
            date_col,
            sp_col,
            forward_dates_use,
            [3, 4],
            )
        
        df = df.loc[~mask_forward].copy()
        
        # Renumber later SPs down by two after the skipped hour.
        mask_forward_roll = _date_sp_mask(
            df,
            date_col,
            sp_col,
            forward_dates_use,
            sps_to_adjust,
            )
        df.loc[mask_forward_roll, sp_col] = (
            df.loc[mask_forward_roll, sp_col] - 2
            )

    # ====================================================================
    # Adjust df for BACKWARDS CLOCK CHANGE
    # ====================================================================
    
    if backward_dates_use:
        # Duplicate SPs 3 and 4 for autumn clock-change dates.
        mask_backward = _date_sp_mask(
            df,
            date_col,
            sp_col,
            backward_dates_use,
            [3, 4],
            )
        
        df_backward_extra = df.loc[mask_backward].copy()  
        
        # Renumber later SPs up by two after the repeated hour.
        mask_backward_roll = _date_sp_mask(
            df,
            date_col,
            sp_col,
            backward_dates_use,
            sps_to_adjust,
            )
        df.loc[mask_backward_roll, sp_col] = (
            df.loc[mask_backward_roll, sp_col] + 2
            )

        # Add SP 3&4 df values back and sort. 
        df = pd.concat([df, df_backward_extra], ignore_index=True)
        df = df.sort_values(by=[date_col, sp_col])

    # Return the date column in its original dtype where possible.
    if pd.api.types.is_datetime64_any_dtype(original_date_dtype):
        df[date_col] = pd.to_datetime(df[date_col])

    return df





def _normal_day_base_df(
        base_date_range: pd.DatetimeIndex,
        time_col_str: bool
        ) -> pd.DataFrame:
    """
    Return a base dataframe before clock-change adjustments.
    """
    no_of_days = len(base_date_range)
    sps_per_day = 48

    sp_range = np.tile(np.arange(1, sps_per_day + 1), no_of_days)
    date_range = np.repeat(base_date_range, sps_per_day)
    time_range = np.tile(_base_time_range(time_col_str=time_col_str), no_of_days)
    efa_range = _base_efa_range(no_of_days=no_of_days)

    return pd.DataFrame(
        {
            'Date': date_range,
            'SP': sp_range,
            'EFA': efa_range,
            'Start_Time': time_range,
        }
    )





def base_df(
        start_date: object | None = None,
        end_date: object | None = None,
        time_col_str: bool = False,
        add_clock_change_sps: bool = False
        ) -> pd.DataFrame:
    """
    Create a base Settlement Period dataframe for a date range.

    The returned dataframe contains one row per Settlement Period, with columns
    for date, Settlement Period, EFA block, start time, and delivery year. A
    normal day contains 48 Settlement Periods.

    Parameters
    ----------
    start_date : object or None, default None
        First date in the output range.
    end_date : object or None, default None
        Last date in the output range.
    time_col_str : bool, default False
        If ``True``, return ``Start_Time`` values as ``'HH:MM'`` strings.
        Otherwise return `datetime.time` values.
    add_clock_change_sps : bool, default False
        If ``True``, adjust Settlement Periods on UK clock-change days.

    Returns
    -------
    pandas.DataFrame
        Base dataframe with ``Date``, ``SP``, ``EFA``, ``Start_Time``, and
        ``Delivery_Year`` columns.

    Examples
    --------
    >>> base_df("2024-01-01", "2024-01-01").shape
    (48, 5)

    >>> base_df("2024-01-01", "2024-01-01", time_col_str=True).loc[0, "Start_Time"]
    '00:00'

    >>> base_df("2024-03-31", "2024-03-31", add_clock_change_sps=True).shape
    (46, 5)

    """
    
    # Create the unadjusted normal-day Settlement Period rows.
    base_date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq='D',
        )
    df = _normal_day_base_df(
        base_date_range=base_date_range,
        time_col_str=time_col_str,
        )

    # ========================================================================
    # Delivery Year column
    # ========================================================================
    
    # Create an 'Operational Year' column based on the April delivery-year
    # boundary.
    df['Delivery_Year'] = _delivery_year_from_dates(df['Date'])

    # ========================================================================
    # Adjust df for CLOCK CHANGE times
    # ========================================================================
    
    if add_clock_change_sps:
        # Keep the chronological Start_Time and EFA values carried by the
        # adjusted source rows. Recalculating from the adjusted SP labels would
        # lose the repeated/skipped-hour semantics on clock-change days.
        df = adjust_for_clock_change(
            df,
            start_date=start_date,
            end_date=end_date,
            date_col='Date',
            sp_col='SP'
            )
        df['Date'] = pd.to_datetime(df['Date'])
    
    return df
