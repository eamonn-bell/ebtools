#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

import pandas as pd



# ---- Dataframe - Formatting





def remove_df_index_name(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """
    Remove the index axis name from a dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to update.

    Returns
    -------
    pandas.DataFrame
        Copy of `df` with no index axis name.

    Examples
    --------
    >>> df = pd.DataFrame({"value": [1]})
    >>> df.index.name = "idx"
    >>> remove_df_index_name(df).index.name is None
    True

    """
    return df.rename_axis(index=None)





def remove_df_column_name(
        df: pd.DataFrame
        ) -> pd.DataFrame:
    """
    Remove the columns axis name from a dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to update.

    Returns
    -------
    pandas.DataFrame
        Copy of `df` with no columns axis name.

    Examples
    --------
    >>> df = pd.DataFrame({"value": [1]})
    >>> df.columns.name = "cols"
    >>> remove_df_column_name(df).columns.name is None
    True

    """
    return df.rename_axis(columns=None)
