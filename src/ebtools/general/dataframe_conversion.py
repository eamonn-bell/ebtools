#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataframe helper functions.
"""

import json
from os import PathLike

import pandas as pd
import numpy as np



# ---- Dataframe - Correct Strings




def _correct_comma_numeric_column(
        df: pd.DataFrame,
        colname: str,
        dtype: type
        ) -> pd.DataFrame:
    """
    Return a dataframe copy with comma-formatted numeric strings converted.
    """
    df_update = df.copy()

    # Remove thousands separators before numeric conversion.
    clean_values = (
        df_update[colname]
        .astype(str)
        .str.replace(',', '', regex=False)
        )

    # Convert the cleaned column and cast to the requested numeric dtype.
    df_update[colname] = pd.to_numeric(
        clean_values,
        errors='raise',
        ).astype(dtype)

    return df_update





def correct_str_elements_float(
        df: pd.DataFrame,
        colname: str
        ) -> pd.DataFrame:
    """
    Convert a comma-formatted numeric column to float.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the column to convert.
    colname : str
        Name of the column to convert.

    Returns
    -------
    pandas.DataFrame
        Copy of `df` with `colname` converted to `numpy.float64`.

    Raises
    ------
    KeyError
        If `colname` is not present in `df`.
    ValueError
        If any cleaned value cannot be converted to a number.

    Examples
    --------
    >>> df = pd.DataFrame({"value": ["1,234.50", "2.50"]})
    >>> correct_str_elements_float(df, "value")["value"].to_list()
    [1234.5, 2.5]

    """
    return _correct_comma_numeric_column(
        df=df,
        colname=colname,
        dtype=np.float64,
        )





def correct_str_elements_int(
        df: pd.DataFrame,
        colname: str
        ) -> pd.DataFrame:
    """
    Convert a comma-formatted numeric column to integer.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the column to convert.
    colname : str
        Name of the column to convert.

    Returns
    -------
    pandas.DataFrame
        Copy of `df` with `colname` converted to `numpy.int64`.

    Raises
    ------
    KeyError
        If `colname` is not present in `df`.
    ValueError
        If any cleaned value cannot be converted to a number.

    Examples
    --------
    >>> df = pd.DataFrame({"value": ["1,234", "2"]})
    >>> correct_str_elements_int(df, "value")["value"].to_list()
    [1234, 2]

    """
    return _correct_comma_numeric_column(
        df=df,
        colname=colname,
        dtype=np.int64,
        )




def create_df_from_json(
        response: object
        ) -> pd.DataFrame:
    """
    Create a dataframe from a JSON-like response.

    Parameters
    ----------
    response : object
        JSON-like response accepted by `pandas.json_normalize`, such as a
        dictionary or a list of dictionaries.

    Returns
    -------
    pandas.DataFrame
        Dataframe created by normalizing `response`.

    Examples
    --------
    >>> response = [{"a": 1, "nested": {"b": 2}}]
    >>> create_df_from_json(response).columns.to_list()
    ['a', 'nested.b']

    """
    return pd.json_normalize(response)





def create_df_from_json_from_file(
        path: str | PathLike[str]
    ) -> pd.DataFrame:
    """
    Create a dataframe from the ``data`` key in a local JSON file.

    Parameters
    ----------
    path : str or os.PathLike[str]
        Path to a JSON file containing a top-level ``data`` key.

    Returns
    -------
    pandas.DataFrame
        Dataframe created from the JSON file's ``data`` value.

    Raises
    ------
    FileNotFoundError
        If `path` does not exist.
    KeyError
        If the JSON file does not contain a top-level ``data`` key.
    json.JSONDecodeError
        If the file does not contain valid JSON.

    Examples
    --------
    >>> path = "response.json"
    >>> create_df_from_json_from_file(path).head()
       a
    0  1
    1  2

    """
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    extracted_data = data['data']

    return pd.DataFrame(extracted_data)
