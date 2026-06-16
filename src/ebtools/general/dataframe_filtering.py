#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

import pandas as pd

import ebtools.general.helper as helper



# ---- Dataframe - Filtering




def df_filter(
        df: pd.DataFrame,
        colname: str,
        term: object = None,
        include: bool = True
        ) -> pd.DataFrame:
    """
    Filter a dataframe by values in a column.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to filter.
    colname : str
        Name of the column to filter.
    term : object, default None
        Value or values to include or exclude.
    include : bool, default True
        If ``True``, keep rows where `colname` is in `term`. If ``False``,
        keep rows where `colname` is not in `term`.
    
    Returns
    -------
    pandas.DataFrame
        Filtered dataframe copy.

    Raises
    ------
    KeyError
        If `colname` is not present in `df`.

    Examples
    --------
    >>> df = pd.DataFrame({"category": ["a", "b", "a"], "value": [1, 2, 3]})
    >>> df_filter(df, colname="category", term="a")["value"].to_list()
    [1, 3]

    >>> df_filter(df, colname="category", term="a", include=False)["value"].to_list()
    [2]

    """
    terms = helper.force_to_list(term)
    mask = df[colname].isin(terms)

    if not include:
        mask = ~mask

    return df.loc[mask, :].copy()





# Formerly tender_cutoff()
def df_cutoff(
        df: pd.DataFrame,
        target_date: object,
        colname: str,
        direction: str = 'after',
        reset_index: bool = True
        ) -> pd.DataFrame:
    """
    Filter a dataframe before or after a target date.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to filter.
    target_date : object
        Date-like cutoff value.
    colname : str
        Name of the datetime-like column to filter.
    direction : {'before', 'after'}, default 'after'
        If ``'before'``, keep rows earlier than `target_date`. If
        ``'after'``, keep rows later than or equal to `target_date`.
    reset_index : bool, default True
        If ``True``, reset the index after filtering.
    
    Returns
    -------
    pandas.DataFrame
        Filtered dataframe copy.

    Raises
    ------
    KeyError
        If `colname` is not present in `df`.
    ValueError
        If `direction` is not ``'before'`` or ``'after'``.

    Examples
    --------
    >>> df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01", "2024-01-02"])})
    >>> df_cutoff(df, target_date="2024-01-02", colname="Date")["Date"].to_list()
    [Timestamp('2024-01-02 00:00:00')]

    >>> df_cutoff(df, target_date="2024-01-02", colname="Date", direction="before").shape
    (1, 1)

    """
    if direction == 'after':
        mask = df[colname] >= target_date
    elif direction == 'before':
        mask = df[colname] < target_date
    else:
        raise ValueError("direction must be 'before' or 'after'.")

    df_cut = df.loc[mask, :].copy()

    if reset_index:
        df_cut = df_cut.reset_index(drop=True)

    return df_cut





def drop_empty_df_cols(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """
    Drop columns containing only zero values.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to process.

    Returns
    -------
    pandas.DataFrame
        Copy of `df` with columns removed where every value is exactly zero.

    Examples
    --------
    >>> df = pd.DataFrame({"empty": [0, 0], "value": [0, 1]})
    >>> drop_empty_df_cols(df).columns.to_list()
    ['value']

    """
    # Identify columns where every row is exactly zero.
    empty_cols = df.columns[df.eq(0).all(axis=0)]

    # Drop only the all-zero columns.
    return df.drop(columns=empty_cols)





def melt_df(
        df: pd.DataFrame,
        interval_type: str,
        value_name: str
        ) -> pd.DataFrame:
    """
    Convert a pivot dataframe to long form.

    Parameters
    ----------
    df : pandas.DataFrame
        Pivot-style dataframe with dates in the index and interval periods in
        the columns.
    interval_type : str
        Name to use for the melted interval column, such as ``'SP'`` or
        ``'Hour'``.
    value_name : str
        Name to use for the melted value column.

    Returns
    -------
    pandas.DataFrame
        Long-form dataframe with ``Date``, `interval_type`, and `value_name`
        columns.

    Examples
    --------
    >>> df = pd.DataFrame({1: [10], 2: [20]}, index=pd.to_datetime(["2024-01-01"]))
    >>> melt_df(df, interval_type="SP", value_name="value").columns.to_list()
    ['Date', 'SP', 'value']

    """
    df_melt = df.copy().melt(
        var_name=interval_type,
        value_name=value_name,
        ignore_index=False,
        )

    df_melt = df_melt.reset_index(drop=False)
    df_melt = df_melt.rename(columns={df_melt.columns[0]: 'Date'})
    df_melt = df_melt.sort_values(by=['Date', interval_type])
    df_melt = df_melt.reset_index(drop=True)

    return df_melt
