#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 21:16:43 2023

@author: eamonnbell
"""





import numpy as np





# ---- Dict Tools





def sort_dict_by_keys(
        dict_to_sort: dict
        ) -> dict:
    """
    Return a dictionary sorted by key.

    Parameters
    ----------
    dict_to_sort : dict
        Dictionary to sort by key.

    Returns
    -------
    dict
        New dictionary containing the same key-value pairs as `dict_to_sort`,
        inserted in sorted-key order.

    Examples
    --------
    >>> sort_dict_by_keys({"b": 2, "a": 1})
    {'a': 1, 'b': 2}

    """
    
    return {key: dict_to_sort[key] for key in sorted(dict_to_sort)}





def make_dict_keys_from_list(
        list_of_str: str | list[str] | np.ndarray,
        print_to_console: bool = True
        ) -> list[str]:
    """
    Return aligned dictionary-key template strings.

    Parameters
    ----------
    list_of_str : str, list of str, or numpy.ndarray
        String values to format as dictionary keys.
    print_to_console : bool, default True
        If ``True``, print each generated key template.

    Returns
    -------
    list of str
        Formatted dictionary-key template strings, aligned to the longest
        input string.

    Raises
    ------
    ValueError
        If `list_of_str` is empty.

    Examples
    --------
    >>> make_dict_keys_from_list(["A", "LongName"], print_to_console=False)
    ["'A'       : ,", "'LongName': ,"]

    >>> make_dict_keys_from_list("Price", print_to_console=False)
    ["'Price': ,"]

    """
    
    values = force_to_list(list_of_str)
    
    if len(values) == 0:
        raise ValueError("list_of_str must contain at least one value.")
    
    # Build aligned key templates based on the longest input string.
    max_len = max(len(value) for value in values)
    key_list = [
        f"'{value}'{(max_len - len(value)) * ' '}: ,"
        for value in values
        ]
    
    if print_to_console:
        for key_text in key_list:
            print(key_text)
        
    return key_list





# ---- Force To Type





def force_to_list(
        value: object
        ) -> list | np.ndarray:
    """
    Return a value as a list unless it is already list-like.

    Parameters
    ----------
    value : object
        Value to normalize.

    Returns
    -------
    list or numpy.ndarray
        If `value` is a list or NumPy array, it is returned unchanged.
        Otherwise, `value` is wrapped in a one-item list.

    Notes
    -----
    NumPy arrays are preserved for backward compatibility. A future version
    could add a stricter helper that always returns a Python list.

    Examples
    --------
    >>> force_to_list("Price")
    ['Price']

    >>> force_to_list(["Price", "Volume"])
    ['Price', 'Volume']

    >>> force_to_list(np.array([1, 2]))
    array([1, 2])

    """
    if isinstance(value, list | np.ndarray):
        return value

    return [value]




def force_to_np_array(
        value: object
        ) -> np.ndarray:
    """
    Return a value as a NumPy array.

    Scalar values are first wrapped in a one-item list so the returned array is
    one-dimensional. Lists and existing NumPy arrays are converted with
    `numpy.asarray`.

    Parameters
    ----------
    value : object
        Scalar, list, or NumPy array to convert.

    Returns
    -------
    numpy.ndarray
        One-dimensional NumPy array for scalar and list inputs. Existing NumPy
        arrays are returned as arrays without an unnecessary copy where
        possible.

    Examples
    --------
    >>> force_to_np_array(1)
    array([1])

    >>> force_to_np_array([1, 2])
    array([1, 2])

    >>> force_to_np_array(np.array([1, 2]))
    array([1, 2])

    """
    value = force_to_list(value)
    return np.asarray(value)


