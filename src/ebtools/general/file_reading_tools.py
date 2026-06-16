#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:35:11 2023

@author: eamonnbell
"""





import os
import zipfile





def does_file_exist(
        file_name: str | os.PathLike
        ) -> bool:
    """
    Return whether a path exists and is a file.

    Parameters
    ----------
    file_name : str or os.PathLike
        Path to the file to check.

    Returns
    -------
    bool
        ``True`` if `file_name` exists and is a file. ``False`` if the path
        does not exist or points to a directory.

    Examples
    --------
    >>> does_file_exist("data/example.csv")
    True

    >>> does_file_exist("data/")
    False

    """
    return os.path.isfile(file_name)





def get_file_type(
        file_name: str | os.PathLike
        ) -> str:
    """
    Return the file extension from a filename or path.

    Parameters
    ----------
    file_name : str or os.PathLike
        Filename or path whose extension should be returned.

    Returns
    -------
    str
        File extension without the leading dot. If `file_name` has no
        extension, return an empty string.

    Examples
    --------
    >>> get_file_type("data/example.csv")
    'csv'

    >>> get_file_type("README")
    ''

    >>> get_file_type("archive.tar.gz")
    'gz'

    """
    return os.path.splitext(file_name)[1].lstrip(".")





def list_all_files_in_folder(
        location: str | os.PathLike
        ) -> list[str]:
    """
    Return filenames found below a folder.

    Parameters
    ----------
    location : str or os.PathLike
        Folder path to search.

    Returns
    -------
    list of str
        Sorted list of filenames found below `location`. Directory paths are
        not included in the returned values. macOS ``.DS_Store`` files are
        excluded.

    Notes
    -----
    A future version could add a ``return_relative_paths`` flag to return file
    paths relative to `location`. This would preserve subfolder context when
    recursively searching nested folders.

    Examples
    --------
    >>> list_all_files_in_folder("data/")
    ['prices.csv', 'volumes.csv']

    """

    allfiles = []
    
    # Walk the folder tree and collect filenames from each directory.
    for _, _, filenames in os.walk(location):
        allfiles.extend(
            filename for filename in filenames
            if filename != '.DS_Store'
            )
    
    return sorted(allfiles)


def _validate_zip_checker_options(
        output: str,
        value_type: str
        ) -> None:
    """
    Validate zip checker output options.
    """
    if output not in {'list', 'dict'}:
        raise ValueError("output must be either 'list' or 'dict'.")

    if value_type not in {'list', 'str'}:
        raise ValueError("value_type must be either 'list' or 'str'.")


def _zip_files_to_check(
        location: str | os.PathLike,
        assess_folder: bool,
        file_name: str | os.PathLike | None
        ) -> list[str | os.PathLike]:
    """
    Return the zipfile names that should be inspected.
    """
    if assess_folder:
        return list_all_files_in_folder(location)

    if file_name is None:
        raise ValueError("file_name must be provided when assess_folder is False.")

    return [file_name]


def _read_zip_names(
        location: str | os.PathLike,
        zip_name: str | os.PathLike
        ) -> list[str]:
    """
    Return the filenames contained in one zipfile.
    """
    zip_path = os.path.join(location, zip_name)

    with zipfile.ZipFile(zip_path) as zf:
        return zf.namelist()


def _zip_value(
        names: list[str],
        value_type: str
        ) -> list[str] | str:
    """
    Format one zipfile's contents according to value type.
    """
    if value_type == 'list':
        return names

    return names[0] if names else ''


def _format_zip_checker_output(
        zip_contents: dict[str | os.PathLike, list[str] | str],
        output: str
        ) -> list[list[str]] | list[str] | dict[str | os.PathLike, list[str] | str]:
    """
    Format zip checker results into the requested return shape.
    """
    if output == 'dict':
        return zip_contents

    return list(zip_contents.values())


def zip_checker(
        location: str | os.PathLike,
        assess_folder: bool = True,
        file_name: str | os.PathLike | None = None,
        output: str = 'list',
        value_type: str = 'list'
        ) -> list[list[str]] | list[str] | dict[str | os.PathLike, list[str] | str]:
    """
    Return the filenames contained inside one or more zipfiles.

    Parameters
    ----------
    location : str or os.PathLike
        Folder containing the zipfiles to inspect.
    assess_folder : bool, default True
        If ``True``, inspect every file returned by
        `list_all_files_in_folder(location)`. If ``False``, inspect only
        `file_name`.
    file_name : str, os.PathLike, or None, default None
        Zipfile name to inspect when `assess_folder` is ``False``.
    output : {'list', 'dict'}, default 'list'
        Shape of the returned object.
    value_type : {'list', 'str'}, default 'list'
        Shape of the zipfile contents in the returned object. If ``'str'``,
        the first filename in each zipfile is used.

    Returns
    -------
    list of list of str, list of str, or dict of str to list of str or str
        Names of files contained in the inspected zipfiles. The exact return
        type depends on `output` and `value_type`.

    Raises
    ------
    ValueError
        If `output` or `value_type` is not recognised.
    ValueError
        If `assess_folder` is ``False`` and `file_name` is ``None``.

    Notes
    -----
    Folder mode assumes that every file returned by
    `list_all_files_in_folder(location)` is a zipfile. A future version could
    add a ``zip_only`` flag to ignore non-zip files.

    Examples
    --------
    >>> zip_checker("data/zips/", output="list", value_type="list")
    [['file_a.csv'], ['file_b.csv']]

    >>> zip_checker(
    ...     "data/zips/",
    ...     assess_folder=False,
    ...     file_name="archive.zip",
    ...     output="dict",
    ... )
    {'archive.zip': ['file_a.csv']}

    """
    _validate_zip_checker_options(output=output, value_type=value_type)

    # Identify the zipfiles that should be inspected.
    allzips = _zip_files_to_check(
        location=location,
        assess_folder=assess_folder,
        file_name=file_name,
        )

    zip_contents = {}

    # Read and format the contents of each zipfile.
    for zip_name in allzips:
        names = _read_zip_names(location=location, zip_name=zip_name)
        zip_contents[zip_name] = _zip_value(
            names=names,
            value_type=value_type,
            )

    # Convert the dictionary into the requested return shape.
    return _format_zip_checker_output(
        zip_contents=zip_contents,
        output=output,
        )
