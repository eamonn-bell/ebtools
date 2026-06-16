#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datetime helper functions.
"""

import datetime
from typing import Literal

import pandas as pd

import ebtools.data as data
from ebtools.general.datetime_helpers import (
    _datetime_parse_summary,
    _normalise_format_list,
    _replace_column_with_temp,
    _restore_column_order,
    _validate_format_list,
)


ParseUtcOption = bool | Literal['infer']
ParseSummary = dict[str, int | dict[str, int]]


def _parse_datetime_column(
        df: pd.DataFrame,
        source_colname: str,
        parsed_colname: str,
        format_list: list[str],
        utc: ParseUtcOption = 'infer',
        use_object_dtype: bool = False
        ) -> tuple[pd.DataFrame, dict[str, int], int]:
    """
    Parse a dataframe column into a temporary parsed datetime column.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime string column.
    source_colname : str
        Name of the source column to parse.
    parsed_colname : str
        Name of the temporary column that will hold parsed values.
    format_list : list of str
        Datetime formats to try in order.
    utc : bool or {'infer'}, default 'infer'
        UTC handling passed to `pandas.to_datetime`. If ``'infer'``, UTC is
        enabled only for formats containing timezone directives.
    use_object_dtype : bool, default False
        If ``True``, create the temporary parsed column with object dtype.

    Returns
    -------
    tuple of pandas.DataFrame, dict, and int
        Updated dataframe, counts parsed by format, and number of unparsed
        rows.

    Examples
    --------
    Parse values by trying later formats only against rows that remain
    unparsed:

    >>> df = pd.DataFrame({"date": ["2024-03-14", "15/03/2024", "bad"]})
    >>> result, counts, unparsed = _parse_datetime_column(
    ...     df.copy(),
    ...     source_colname="date",
    ...     parsed_colname="date_parsed",
    ...     format_list=["%Y-%m-%d", "%d/%m/%Y"],
    ... )
    >>> counts
    {'%Y-%m-%d': 1, '%d/%m/%Y': 1}
    >>> unparsed
    1

    """
    parsed_by_format = {}

    # Create a holding column for parsed dates. Timezone-aware parsing uses
    # object dtype until the final timezone normalization step.
    if use_object_dtype:
        df[parsed_colname] = pd.Series(pd.NaT, index=df.index, dtype=object)
    else:
        df[parsed_colname] = pd.NaT

    # Try each format only against rows that have not yet been parsed.
    for format_to_check in format_list:
        unparsed_mask = df[parsed_colname].isnull()

        if not unparsed_mask.any():
            break

        # Infer UTC parsing for timezone-aware format strings when requested.
        if utc == 'infer':
            parse_utc = ('%z' in format_to_check) or ('%Z' in format_to_check)
        else:
            parse_utc = utc

        parsed_values = pd.to_datetime(
            df.loc[unparsed_mask, source_colname],
            format=format_to_check,
            errors='coerce',
            utc=parse_utc
            )

        parsed_mask = parsed_values.notna()
        parsed_by_format[format_to_check] = int(parsed_mask.sum())

        df.loc[parsed_values.index[parsed_mask], parsed_colname] =             \
            parsed_values.loc[parsed_mask]

    unparsed_rows = int(df[parsed_colname].isnull().sum())

    return df, parsed_by_format, unparsed_rows


def check_datetime_formats(
        df: pd.DataFrame,
        colname: str,
        format_list: str | list[str] | None = None,
        raise_on_unparsed: bool = False,
        report_summary: bool = False
        ) -> pd.DataFrame | tuple[pd.DataFrame, ParseSummary]:
    """
    Parse a dataframe column containing datetime strings.

    The function tries each format in `format_list` in order. Values that fail
    to parse with one format are retried with the next format. The original
    column is replaced with parsed datetime values, and the original column
    order is preserved. For timezone-aware strings, prefer
    `check_datetime_formats_tz`.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime string column.
    colname : str
        Name of the column to parse.
    format_list : str, list of str, or None, default None
        Datetime format or formats to try. If ``None``,
        `ebtools.data.format_list_standard` is used.
    raise_on_unparsed : bool, default False
        If ``True``, raise a `ValueError` when any values cannot be parsed.
        If ``False``, unparsed values remain `NaT`.
    report_summary : bool, default False
        If ``True``, return a tuple of ``(dataframe, summary)``. The summary
        reports total rows, parsed rows, unparsed rows, and rows parsed by
        each format.

    Returns
    -------
    pandas.DataFrame or tuple of pandas.DataFrame and dict
        Dataframe with `colname` converted to datetime values. If
        `report_summary` is ``True``, also return a parse summary dictionary.

    Raises
    ------
    KeyError
        If `colname` is not present in `df`.
    ValueError
        If `format_list` is empty.
    ValueError
        If `raise_on_unparsed` is ``True`` and any values cannot be parsed.

    Examples
    --------
    Parse a column with multiple possible formats:

    >>> df = pd.DataFrame({"date": ["2024-03-14", "15/03/2024"]})
    >>> result = check_datetime_formats(
    ...     df, colname="date", format_list=["%Y-%m-%d", "%d/%m/%Y"]
    ... )
    >>> result["date"].to_list()
    [Timestamp('2024-03-14 00:00:00'), Timestamp('2024-03-15 00:00:00')]

    Return a parse summary when requested:

    >>> result, summary = check_datetime_formats(
    ...     df, colname="date", format_list=["%Y-%m-%d", "%d/%m/%Y"],
    ...     report_summary=True
    ... )
    >>> summary["parsed_rows"]
    2

    """
    if colname not in df.columns:
        raise KeyError(f"Column {colname!r} not found in dataframe.")

    df = df.copy()
    parsed_colname = colname + '_correct'

    # Set default format list and cast to a list if a single format is passed.
    format_list = _normalise_format_list(
        format_list,
        default=data.format_list_standard
        )
    _validate_format_list(format_list, name='format_list')
    
    # Gather initial column order
    initial_columns = [x for x in df.columns]

    # Parse values into a temporary column, trying later formats only against
    # rows that previous formats could not parse.
    df, parsed_by_format, unparsed_rows = _parse_datetime_column(
        df=df,
        source_colname=colname,
        parsed_colname=parsed_colname,
        format_list=format_list,
        utc='infer'
        )

    if raise_on_unparsed and unparsed_rows > 0:
        raise ValueError(
            f"{unparsed_rows} value(s) in column {colname!r} could not be parsed."
        )

    # Replace the initial column with the parsed placeholder column.
    df = _replace_column_with_temp(df, colname, parsed_colname)
    
    # Return df columns to their original order
    df = _restore_column_order(df, initial_columns)

    if report_summary:
        return df, _datetime_parse_summary(
            total_rows=len(df),
            unparsed_rows=unparsed_rows,
            parsed_by_format=parsed_by_format,
            )

    return df


def check_datetime_formats_tz(
        df: pd.DataFrame,
        colname: str,
        format_list_tz: str | list[str] | None = None,
        include_utc: bool = False,
        raise_on_unparsed: bool = False,
        report_summary: bool = False
        ) -> pd.DataFrame | tuple[pd.DataFrame, ParseSummary]:
    """
    Parse a dataframe column containing timezone-aware datetime strings.

    The function tries each format in `format_list_tz` in order. Values that
    fail to parse with one format are retried with the next format. Parsed
    values are normalised through UTC. If `include_utc` is ``False``, the
    returned datetime values are timezone-naive after UTC conversion.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the datetime string column.
    colname : str
        Name of the column to parse.
    format_list_tz : str, list of str, or None, default None
        Timezone-aware datetime format or formats to try. If ``None``,
        `ebtools.data.format_list_tz` is used.
    include_utc : bool, default False
        If ``True``, keep the result as timezone-aware UTC datetimes. If
        ``False``, return timezone-naive datetimes after UTC conversion.
    raise_on_unparsed : bool, default False
        If ``True``, raise a `ValueError` when any values cannot be parsed.
        If ``False``, unparsed values remain `NaT`.
    report_summary : bool, default False
        If ``True``, return a tuple of ``(dataframe, summary)``. The summary
        reports total rows, parsed rows, unparsed rows, and rows parsed by
        each format.
        
    Returns
    -------
    pandas.DataFrame or tuple of pandas.DataFrame and dict
        Dataframe with `colname` converted to datetime values. If
        `report_summary` is ``True``, also return a parse summary dictionary.

    Raises
    ------
    KeyError
        If `colname` is not present in `df`.
    ValueError
        If `format_list_tz` is empty.
    ValueError
        If `raise_on_unparsed` is ``True`` and any values cannot be parsed.

    Examples
    --------
    Parse timezone-aware strings and return timezone-naive UTC-equivalent
    datetimes by default:

    >>> df = pd.DataFrame({"date": ["2024-03-15T01:30:00+01:00"]})
    >>> result = check_datetime_formats_tz(
    ...     df, colname="date", format_list_tz="%Y-%m-%dT%H:%M:%S%z"
    ... )
    >>> result.loc[0, "date"]
    Timestamp('2024-03-15 00:30:00')

    Keep UTC-aware datetimes when requested:

    >>> result = check_datetime_formats_tz(
    ...     df, colname="date", format_list_tz="%Y-%m-%dT%H:%M:%S%z",
    ...     include_utc=True
    ... )
    >>> result.loc[0, "date"]
    Timestamp('2024-03-15 00:30:00+0000', tz='UTC')

    """
    if colname not in df.columns:
        raise KeyError(f"Column {colname!r} not found in dataframe.")

    df = df.copy()
    parsed_colname = colname + '_correct'
    
    # Set default format list and cast to a list if a single format is passed.
    format_list_tz = _normalise_format_list(
        format_list_tz,
        default=data.format_list_tz
        )
    _validate_format_list(format_list_tz, name='format_list_tz')

    # Gather initial column order
    initial_columns = [x for x in df.columns]
    
    # Parse values into a temporary column, keeping timezone-aware values as
    # object dtype until all formats have been attempted.
    df, parsed_by_format, unparsed_rows = _parse_datetime_column(
        df=df,
        source_colname=colname,
        parsed_colname=parsed_colname,
        format_list=format_list_tz,
        utc=True,
        use_object_dtype=True
        )
    
    if raise_on_unparsed and unparsed_rows > 0:
        raise ValueError(
            f"{unparsed_rows} value(s) in column {colname!r} could not be parsed."
        )
    
    # Normalise all parsed values through UTC, then optionally remove timezone
    # awareness for downstream workflows that expect timezone-naive datetimes.
    df[parsed_colname] = pd.to_datetime(df[parsed_colname], utc=True)
    
    if not include_utc:
        df[parsed_colname] = df[parsed_colname].dt.tz_localize(None)
    
    # Replace the initial column with the parsed placeholder column.
    df = _replace_column_with_temp(df, colname, parsed_colname)
    
    # Return df columns to their original order
    df = _restore_column_order(df, initial_columns)
    
    if report_summary:
        return df, _datetime_parse_summary(
            total_rows=len(df),
            unparsed_rows=unparsed_rows,
            parsed_by_format=parsed_by_format,
            )
    
    return df


def check_string_datetime_formats(
        date_string: str,
        format_list: str | list[str] | None = None
        ) -> pd.Timestamp:
    """
    Parse a datetime string using one or more known formats.

    Formats are tried in order until one succeeds. If `format_list` is
    ``None``, `ebtools.data.format_list_standard` is used.

    Parameters
    ----------
    date_string : str
        Datetime string to parse.
    format_list : str, list of str, or None, default None
        Datetime format or formats to try.

    Returns
    -------
    pandas.Timestamp
        Parsed datetime value.

    Raises
    ------
    ValueError
        If `format_list` is empty, or if `date_string` does not match any
        format.

    Examples
    --------
    Parse a string with one explicit format:

    >>> check_string_datetime_formats("2024-03-14", format_list="%Y-%m-%d")
    Timestamp('2024-03-14 00:00:00')

    Try multiple formats in order:

    >>> check_string_datetime_formats(
    ...     "14/03/2024", format_list=["%Y-%m-%d", "%d/%m/%Y"]
    ... )
    Timestamp('2024-03-14 00:00:00')

    """
    format_list = _normalise_format_list(
        format_list,
        default=data.format_list_standard,
        )
    _validate_format_list(format_list, name='format_list')

    output_date = None

    # Cycle through the format string options in format_list until
    # date_string is parsed without an error.
    for format_string in format_list:
        try:
            output_date = datetime.datetime.strptime(date_string, format_string)
            break
        except ValueError:
            pass

    if output_date is None:
        raise ValueError(
            f"date_string {date_string!r} does not match any format in format_list."
        )
    
    return pd.to_datetime(output_date)





# ---- Adjust Dates
