#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

import pandas as pd
import numpy as np

import ebtools.general.helper as helper



# ---- Dataframe - Processing





def unique_element_count(
        df: pd.DataFrame,
        col: str
        ) -> int:
    """
    Count unique non-null values in a dataframe column.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing `col`.
    col : str
        Name of the column to count.
    
    Returns
    -------
    int
        Number of unique non-null values in `col`.

    Raises
    ------
    KeyError
        If `col` is not present in `df`.

    Examples
    --------
    >>> df = pd.DataFrame({"category": ["a", "a", "b", None]})
    >>> unique_element_count(df, "category")
    2

    """
    return df[col].nunique(dropna=True)





def _join_string_values(
        values: object
        ) -> str:
    """
    Join values by converting each element to a string.
    """
    return ''.join(str(value) for value in values)





def non_numeric_pivot(
        df: pd.DataFrame,
        index: str,
        columns: str,
        values: str
        ) -> pd.DataFrame:
    """
    Pivot non-numeric values into a dataframe.

    Values are aggregated by joining their string representations. The
    function is intended for cases where each index-column pair has one
    logical value.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to pivot.
    index : str
        Column to use as the pivot index.
    columns : str
        Column to use as pivot columns.
    values : str
        Column containing values to aggregate.
    
    Returns
    -------
    pandas.DataFrame
        Pivoted dataframe.

    Raises
    ------
    KeyError
        If any selected column is not present in `df`.

    Examples
    --------
    >>> df = pd.DataFrame({"Date": ["2024-01-01"], "label": ["a"], "value": ["x"]})
    >>> non_numeric_pivot(df, index="Date", columns="label", values="value").loc["2024-01-01", "a"]
    'x'

    """
    return df.pivot_table(
        index=index,
        columns=columns,
        values=values,
        aggfunc=_join_string_values,
        )





def df_round_to_decimal(
        df: pd.DataFrame,
        colname: str | list[str],
        decimals: int = 2
        ) -> pd.DataFrame:
    """
    Round one or more dataframe columns to fixed decimal places.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing columns to round.
    colname : str or list of str
        Column name or names to round.
    decimals : int, default 2
        Number of decimal places to retain.

    Returns
    -------
    pandas.DataFrame
        Dataframe copy with selected columns rounded.

    Raises
    ------
    KeyError
        If any selected column is not present in `df`.

    Examples
    --------
    >>> df = pd.DataFrame({"a": [1.234], "b": [5.678]})
    >>> df_round_to_decimal(df, colname=["a", "b"], decimals=1).loc[0, "a"]
    1.2

    """
    df_decimal = df.copy()
    colnames = helper.force_to_list(colname)
    df_decimal[colnames] = df_decimal[colnames].round(decimals)
    
    return df_decimal
