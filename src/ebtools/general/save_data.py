#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:21:07 2023

@author: eamonnbell
"""





import os

import pandas as pd
import ebtools.general.helper as helper
import ebtools.general.file_reading_tools as frt





# ---- Save data





def save_to_csv(
        df: pd.DataFrame,
        location: str | os.PathLike,
        file_name: str | os.PathLike,
        index: bool = False
        ) -> None:
    """
    Save a dataframe to a CSV file.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to save.
    location : str or os.PathLike
        Folder where the CSV file should be written.
    file_name : str or os.PathLike
        Name of the CSV file to write. The file name must end in ``.csv``.
    index : bool, default False
        If ``True``, write the dataframe index to the CSV file.
    
    Returns
    -------
    None
        The dataframe is written to disk.

    Raises
    ------
    ValueError
        If `file_name` does not have a ``.csv`` extension.

    Examples
    --------
    >>> save_to_csv(df, "data/", "prices.csv")

    >>> save_to_csv(df, "data/", "prices_with_index.csv", index=True)
    
    """
    
    file_type = frt.get_file_type(file_name)
    
    if file_type != 'csv':
        raise ValueError(f"The expected file_type is '*.csv'. User passed: *.{file_type}")
    
    df.to_csv(os.path.join(location, file_name), index=index)





def save_to_xlsx(
        df: pd.DataFrame | list[pd.DataFrame],
        location: str | os.PathLike,
        file_name: str | os.PathLike,
        sheet_name: str | list[str],
        startrow: int = 0,
        index: bool | list[bool] = False
        ) -> None:
    """
    Save one or more dataframes to an Excel workbook.

    Parameters
    ----------
    df : pandas.DataFrame or list of pandas.DataFrame
        Dataframe or dataframes to save.
    location : str or os.PathLike
        Folder where the Excel workbook should be written.
    file_name : str or os.PathLike
        Name of the Excel workbook to write. The file name must end in
        ``.xlsx``.
    sheet_name : str or list of str
        Worksheet name or names. If `df` is a list, this must contain one
        sheet name per dataframe.
    startrow : int, default 0
        Row in each worksheet where writing should start.
    index : bool or list of bool, default False
        Whether to write dataframe indexes. If a list is provided, it must
        contain one value per dataframe.
    
    Returns
    -------
    None
        The workbook is written to disk.

    Raises
    ------
    ValueError
        If `file_name` does not have a ``.xlsx`` extension.
    ValueError
        If the number of dataframes and sheet names do not match.
    ValueError
        If `index` is a list and its length does not match the number of
        dataframes.

    Examples
    --------
    >>> save_to_xlsx(df, "data/", "prices.xlsx", sheet_name="Prices")

    >>> save_to_xlsx(
    ...     [prices, volumes],
    ...     "data/",
    ...     "market_data.xlsx",
    ...     sheet_name=["Prices", "Volumes"],
    ... )
    
    """

    file_type = frt.get_file_type(file_name)
    
    if file_type != 'xlsx':
        raise ValueError(f"The expected file_type is '*.xlsx'. User passed: *.{file_type}")
    
    # Cast dataframe and sheet inputs to lists for a single write loop.
    df_list = helper.force_to_list(df)
    sheet_name_list = helper.force_to_list(sheet_name)
    
    if len(df_list) != len(sheet_name_list):
        raise ValueError("df and sheet_name must contain the same number of values.")
    
    if isinstance(index, list) and len(index) != len(df_list):
        raise ValueError(
            "index must contain one value per dataframe when passed as a list."
            )
    
    with pd.ExcelWriter(os.path.join(location, file_name)) as writer:
        # Write each dataframe to its corresponding worksheet.
        for n, item in enumerate(df_list):    
            write_index = index[n] if isinstance(index, list) else index
            item.to_excel(
                writer,
                sheet_name=sheet_name_list[n],
                startrow=startrow,
                index=write_index,
                )





def save_to_parquet(
        df: pd.DataFrame,
        location: str | os.PathLike,
        file_name: str | os.PathLike,
        index: bool = False
        ) -> None:
    """
    Save a dataframe to a Parquet file.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to save.
    location : str or os.PathLike
        Folder where the Parquet file should be written.
    file_name : str or os.PathLike
        Name of the Parquet file to write. The file name must end in
        ``.parquet``.
    index : bool, default False
        If ``True``, write the dataframe index to the Parquet file.

    Returns
    -------
    None
        The dataframe is written to disk.

    Raises
    ------
    ValueError
        If `file_name` does not have a ``.parquet`` extension.

    Examples
    --------
    >>> save_to_parquet(df, "data/", "prices.parquet")

    >>> save_to_parquet(df, "data/", "prices_with_index.parquet", index=True)

    """
    
    file_type = frt.get_file_type(file_name)
    
    if file_type != 'parquet':
        raise ValueError(f"The expected file_type is '*.parquet'. User passed: *.{file_type}")
    
    df.to_parquet(os.path.join(location, file_name), index=index)
