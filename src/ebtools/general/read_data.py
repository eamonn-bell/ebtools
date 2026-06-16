#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:18:29 2023

@author: eamonnbell
"""





import os

import pandas as pd
import numpy as np

import ebtools.data as data
import ebtools.general.dataframe_filtering as df_tools
import ebtools.general.datetime_parsing as dtf
import ebtools.general.file_reading_tools as frt





# ---- Read data





def read_from_csv(
        location: str | os.PathLike,
        file_name: str | os.PathLike
        ) -> pd.DataFrame:
    """
    Read a CSV file into a dataframe.
    
    Parameters
    ----------
    location : str or os.PathLike
        Folder containing the CSV file.
    file_name : str or os.PathLike
        Name of the CSV file to read. The file name must end in ``.csv``.
   
    Returns
    -------
    pandas.DataFrame
        Dataframe containing the CSV file contents.

    Raises
    ------
    ValueError
        If `file_name` does not have a ``.csv`` extension.

    Examples
    --------
    >>> read_from_csv("data/", "prices.csv")
       Date  Price
    0  ...
   
    """
    file_type = frt.get_file_type(file_name)
    
    if file_type != 'csv':
        raise ValueError(f"The expected file_type is '*.csv'. User passed: *.{file_type}")
    
    return pd.read_csv(
        os.path.join(location, file_name),
        header=0, 
        index_col=None
        )





def read_from_xlsx(
        location: str | os.PathLike,
        file_name: str | os.PathLike,
        sheet_name: str | int | None = 0
        ) -> pd.DataFrame | dict[str, pd.DataFrame]:
    """
    Read an Excel workbook into a dataframe.
    
    Parameters
    ----------
    location : str or os.PathLike
        Folder containing the Excel workbook.
    file_name : str or os.PathLike
        Name of the Excel workbook to read. The file name must end in
        ``.xlsx``.
    sheet_name : str, int, or None, default 0
        Worksheet to read. The default value of ``0`` reads the first
        worksheet in the workbook. Pass a worksheet name to read a specific
        tab, or ``None`` to return all worksheets as a dictionary of
        dataframes.
    
    Returns
    -------
    pandas.DataFrame or dict of str to pandas.DataFrame
        Dataframe containing the selected worksheet contents. If `sheet_name`
        is ``None``, return a dictionary mapping worksheet names to
        dataframes.

    Raises
    ------
    ValueError
        If `file_name` does not have a ``.xlsx`` extension.

    Examples
    --------
    >>> read_from_xlsx("data/", "prices.xlsx")
       Date  Price
    0  ...

    >>> sheets = read_from_xlsx("data/", "prices.xlsx", sheet_name=None)
    >>> list(sheets)
    ['Sheet1', 'Sheet2']
    
    """
    file_type = frt.get_file_type(file_name)
    
    if file_type != 'xlsx':
        raise ValueError(f"The expected file_type is '*.xlsx'. User passed: *.{file_type}")

    return pd.read_excel(
        os.path.join(location, file_name),
        sheet_name=sheet_name,
        header=0, 
        index_col=None
        )





def read_from_parquet(
        location: str | os.PathLike,
        file_name: str | os.PathLike
        ) -> pd.DataFrame:
    """
    Read a Parquet file into a dataframe.

    Parameters
    ----------
    location : str or os.PathLike
        Folder containing the Parquet file.
    file_name : str or os.PathLike
        Name of the Parquet file to read. The file name must end in
        ``.parquet``.

    Returns
    -------
    pandas.DataFrame
        Dataframe containing the Parquet file contents.

    Raises
    ------
    ValueError
        If `file_name` does not have a ``.parquet`` extension.

    Examples
    --------
    >>> read_from_parquet("data/", "prices.parquet")
       Date  Price
    0  ...

    """
    
    file_type = frt.get_file_type(file_name)
    
    if file_type != 'parquet':
        raise ValueError(f"The expected file_type is '*.parquet'. User passed: *.{file_type}")
        
    return pd.read_parquet(os.path.join(location, file_name))





# ---- HH Data


_PERIOD_VARIABLE_NAMES = {
    48: 'SP',
    24: 'Hour',
    6: 'EFA',
}


def _validate_hh_inputs(
        df: pd.DataFrame,
        file_type: str,
        date_col_name: str | None,
        mpan_col_name: str | None,
        select_mpan: int | list[int] | None,
        no_periods: int
        ) -> None:
    """
    Validate HH data loader inputs.
    """
    if file_type not in {'csv', 'xlsx'}:
        raise ValueError(
            "The expected file_type is '*.csv' or '*.xlsx'. "
            f"User passed: *.{file_type}"
            )

    if no_periods not in _PERIOD_VARIABLE_NAMES:
        raise ValueError("no_periods must be one of 48, 24, or 6.")

    if date_col_name is None:
        raise ValueError("date_col_name must be provided.")

    if date_col_name not in df.columns:
        raise KeyError(f"Column {date_col_name!r} not found in dataframe.")

    if select_mpan is not None and mpan_col_name is None:
        raise ValueError("mpan_col_name must be provided when select_mpan is used.")

    if mpan_col_name is not None and mpan_col_name not in df.columns:
        raise KeyError(f"Column {mpan_col_name!r} not found in dataframe.")

    if len(df.columns) < no_periods:
        raise ValueError(
            f"Dataframe must contain at least {no_periods} period columns."
            )


def _read_hh_file(
        location: str | os.PathLike,
        file_name: str | os.PathLike,
        sheet_name: str | int | None
        ) -> tuple[pd.DataFrame, str]:
    """
    Read a CSV or Excel HH data file.
    """
    file_type = frt.get_file_type(file_name)
    file_path = os.path.join(location, file_name)

    if file_type == 'csv':
        return pd.read_csv(file_path, header=0, index_col=None), file_type

    if file_type == 'xlsx':
        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=0,
            index_col=None,
            )

        if isinstance(df, dict):
            raise ValueError(
                "load_hh_data requires a single worksheet. "
                "Pass a worksheet name or integer sheet_name."
                )

        return df, file_type

    return pd.DataFrame(), file_type


def _parse_hh_dates(
        df: pd.DataFrame,
        date_col_name: str,
        format_list: str | list[str] | None
        ) -> pd.DataFrame:
    """
    Parse the HH date column and use it as the dataframe index.
    """
    if format_list is None:
        format_list = data.format_list_standard

    df = dtf.check_datetime_formats(
        df,
        colname=date_col_name,
        format_list=format_list,
        )

    # Use the parsed date column as the index and standardise the index name.
    df = df.set_index(date_col_name)
    return df.rename_axis('Date', axis=0).rename_axis(None, axis=1)


def _trim_hh_date_range(
        df: pd.DataFrame,
        start_date: object | None,
        end_date: object | None
        ) -> pd.DataFrame:
    """
    Trim HH data to an optional inclusive date range.
    """
    if start_date is None and end_date is None:
        return df

    if start_date is None:
        start_date = df.index[0]

    if end_date is None:
        end_date = df.index[-1]

    return df.loc[
        (df.index >= pd.to_datetime(start_date))
        & (df.index <= pd.to_datetime(end_date))
        ]


def _rename_period_columns(
        df: pd.DataFrame,
        no_periods: int
        ) -> tuple[pd.DataFrame, list]:
    """
    Rename the final period columns to period numbers.
    """
    col_names = df.columns.to_list()
    col_names[-no_periods:] = range(1, no_periods + 1)

    df = df.copy()
    df.columns = col_names

    return df, col_names


def _process_hh_mpan(
        df: pd.DataFrame,
        mpan_col_name: str | None,
        select_mpan: int | list[int] | None,
        aggregate_by_mpan: bool,
        drop_mpan_col: bool
        ) -> tuple[pd.DataFrame, list[str]]:
    """
    Filter and aggregate HH data by MPAN when requested.
    """
    if mpan_col_name is None:
        return df, []

    df = df.copy()
    expected_cols = [mpan_col_name]

    # Normalise MPAN values before filtering or grouping.
    df[mpan_col_name] = df[mpan_col_name].astype('int64')

    if select_mpan is not None:
        df = df_tools.df_filter(
            df,
            colname=mpan_col_name,
            term=select_mpan,
            include=True,
            )

    if aggregate_by_mpan:
        if drop_mpan_col:
            df = df.drop([mpan_col_name], axis=1)
            expected_cols = []

        df = df.groupby(df.index).sum()

    return df, expected_cols


def _select_hh_output_columns(
        df: pd.DataFrame,
        expected_cols: list[str],
        no_periods: int
        ) -> tuple[pd.DataFrame, list]:
    """
    Keep only metadata and period columns expected in the HH output.
    """
    col_list = expected_cols + list(range(1, no_periods + 1))
    cols_to_remove = list(set(df.columns.to_list()) - set(col_list))

    return df.drop(cols_to_remove, axis=1), col_list


def _hh_time_columns(no_periods: int) -> pd.Index | np.ndarray:
    """
    Return HH period labels formatted as time strings.
    """
    if no_periods == 48:
        return pd.date_range(start='00:00', periods=48, freq='30min').strftime('%H:%M')

    if no_periods == 24:
        return pd.date_range(start='00:00', periods=24, freq='1h').strftime('%H:%M')

    return np.roll(
        pd.date_range(start='03:00', periods=6, freq='4h').strftime('%H:%M'),
        1,
        )


def _apply_hh_time_columns(
        df: pd.DataFrame,
        col_list: list,
        no_periods: int
        ) -> tuple[pd.DataFrame, list]:
    """
    Replace period-number columns with time string labels.
    """
    col_list = col_list.copy()
    col_list[-no_periods:] = _hh_time_columns(no_periods)

    df = df.copy()
    df.columns = col_list

    return df, col_list


def _melt_hh_data(
        df: pd.DataFrame,
        mpan_col_name: str | None,
        aggregate_by_mpan: bool,
        drop_mpan_col: bool,
        no_periods: int
        ) -> pd.DataFrame:
    """
    Convert pivot-format HH data into long format.
    """
    variable_name = _PERIOD_VARIABLE_NAMES[no_periods]

    if mpan_col_name is None or (aggregate_by_mpan and drop_mpan_col):
        df = (
            df
            .melt(ignore_index=False)
            .reset_index(drop=False)
            .rename(columns={
                'variable': variable_name,
                'value': 'Outturn',
                })
            )

    elif not drop_mpan_col:
        df = (
            df
            .reset_index()
            .melt(id_vars=['Date', mpan_col_name])
            .rename(columns={
                mpan_col_name: 'MPAN',
                'variable': variable_name,
                'value': 'Outturn',
                })
            )

    return df.sort_values(by=['Date', variable_name]).reset_index(drop=True)


def load_hh_data(
        location: str | os.PathLike,
        file_name: str | os.PathLike,
        start_date: object | None = None,
        end_date: object | None = None,
        date_col_name: str | None = None,
        mpan_col_name: str | None = None,
        name_col_name: str | None = None,
        select_mpan: int | list[int] | None = None,
        aggregate_by_mpan: bool = True,
        drop_mpan_col: bool = True,
        pivot_format: bool = True,
        cols_as_time: bool = False,
        format_list: str | list[str] | None = None,
        no_periods: int = 48,
        sheet_name: str | int | None = 0,
        ) -> pd.DataFrame:
    """
    Load electricity period data from a CSV or Excel file.

    The input data is expected in wide format: one row per date or site-date
    pair, with the final `no_periods` columns containing period values. The
    function can return the data in wide pivot format or melt it into a long
    dataframe.

    Parameters
    ----------
    location : str or os.PathLike
        Folder containing the input file.
    file_name : str or os.PathLike
        CSV or Excel filename to load.
    start_date, end_date : object or None, default None
        Optional inclusive date range used to trim the parsed date index.
    date_col_name : str or None, default None
        Name of the date column in the input data. This must be provided.
    mpan_col_name : str or None, default None
        Name of the MPAN column, if the data contains MPAN-level rows.
    name_col_name : str or None, default None
        Reserved for compatibility with existing calls. The column is not
        required in processing.
    select_mpan : int, list of int, or None, default None
        MPAN value or values to keep. Requires `mpan_col_name`.
    aggregate_by_mpan : bool, default True
        If ``True``, aggregate MPAN rows by date after optional MPAN filtering.
    drop_mpan_col : bool, default True
        If ``True`` and aggregating, drop the MPAN column before grouping.
    pivot_format : bool, default True
        If ``True``, return wide period columns. If ``False``, return long
        format with ``'Outturn'`` values.
    cols_as_time : bool, default False
        If ``True``, label period columns with time strings rather than period
        numbers.
    format_list : str, list of str, or None, default None
        Datetime formats used to parse `date_col_name`. If ``None``,
        `ebtools.data.format_list_standard` is used.
    no_periods : {48, 24, 6}, default 48
        Number of period value columns expected at the end of the input data.
    sheet_name : str, int, or None, default 0
        Excel worksheet to read for ``.xlsx`` files. The default value of
        ``0`` reads the first worksheet.

    Returns
    -------
    pandas.DataFrame
        Processed period data in wide or long format.

    Raises
    ------
    ValueError
        If the file type, `no_periods`, or argument combination is invalid.
    KeyError
        If required columns are missing from the input data.

    Examples
    --------
    >>> load_hh_data("data/", "hh.csv", date_col_name="Date")
                1    2    3
    Date
    2024-01-01  ...

    >>> load_hh_data(
    ...     "data/",
    ...     "hh.xlsx",
    ...     date_col_name="Date",
    ...     mpan_col_name="MPAN",
    ...     select_mpan=123,
    ...     pivot_format=False,
    ... )
            Date  SP  Outturn
    0 2024-01-01   1      ...

    """
    df, file_type = _read_hh_file(
        location=location,
        file_name=file_name,
        sheet_name=sheet_name,
        )

    _validate_hh_inputs(
        df=df,
        file_type=file_type,
        date_col_name=date_col_name,
        mpan_col_name=mpan_col_name,
        select_mpan=select_mpan,
        no_periods=no_periods,
        )

    df = _parse_hh_dates(
        df=df,
        date_col_name=date_col_name,
        format_list=format_list,
        )
    df = _trim_hh_date_range(
        df=df,
        start_date=start_date,
        end_date=end_date,
        )
    df, _ = _rename_period_columns(df=df, no_periods=no_periods)
    df, expected_cols = _process_hh_mpan(
        df=df,
        mpan_col_name=mpan_col_name,
        select_mpan=select_mpan,
        aggregate_by_mpan=aggregate_by_mpan,
        drop_mpan_col=drop_mpan_col,
        )
    df, col_list = _select_hh_output_columns(
        df=df,
        expected_cols=expected_cols,
        no_periods=no_periods,
        )

    if cols_as_time:
        df, col_list = _apply_hh_time_columns(
            df=df,
            col_list=col_list,
            no_periods=no_periods,
            )

    if not pivot_format:
        df = _melt_hh_data(
            df=df,
            mpan_col_name=mpan_col_name,
            aggregate_by_mpan=aggregate_by_mpan,
            drop_mpan_col=drop_mpan_col,
            no_periods=no_periods,
            )

    return df
