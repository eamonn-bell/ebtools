#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 23:56:00 2023

@author: eamonnbell
"""





import numpy as np





# ---- General





def add_newaxis(arr: np.ndarray) -> np.ndarray:
    """
    Convert a one-dimensional array to a column vector.

    Parameters
    ----------
    arr : numpy.ndarray
        One-dimensional input array. Array-like inputs are converted with
        `numpy.asarray`.

    Returns
    -------
    numpy.ndarray
        View of `arr` with shape ``(n, 1)``.

    Raises
    ------
    ValueError
        If `arr` is not one-dimensional.

    Examples
    --------
    >>> arr = np.array([1, 2, 3])
    >>> add_newaxis(arr)
    array([[1],
           [2],
           [3]])
    >>> add_newaxis(arr).shape
    (3, 1)
    """
    arr = np.asarray(arr)

    if arr.ndim != 1:
        raise ValueError("arr must be one-dimensional.")

    return arr[:, np.newaxis]



# ---- Array Data Selection Tools





def n_smallest_values_per_row(
        arr: np.ndarray,
        smallest: int | np.ndarray = 6,
        replace=0
        ) -> np.ndarray:
    """
    Keep the n smallest values in each row of an array.

    The returned array has the same shape as the input array after
    one-dimensional inputs are reshaped to a single row. Selected values
    remain in their original column positions. Unselected values are replaced
    with `replace`.

    Parameters
    ----------
    arr : numpy.ndarray
        One- or two-dimensional array of values. A one-dimensional input is
        treated as a single row.
    smallest : int or numpy.ndarray of int, default 6
        Number of smallest values to keep in each row. If an integer, the same
        number is used for every row. If an array, it must contain one integer
        per row in `arr`.
    replace : scalar, default 0
        Value used to replace unselected elements. Use `numpy.nan` to mark
        unselected values as missing.

    Returns
    -------
    numpy.ndarray
        Two-dimensional array with selected values preserved in their original
        positions and all other values replaced.

    Raises
    ------
    ValueError
        If `arr` is not one- or two-dimensional.
    ValueError
        If `smallest` is array-like and does not contain one value per row.
    ValueError
        If any value in `smallest` is less than 0 or greater than the number
        of columns in `arr`.

    Notes
    -----
    When values are tied, selection is determined by NumPy's row-wise sort
    order.

    Examples
    --------
    >>> arr = np.array([[3, 1, 2], [9, 4, 8]])
    >>> n_smallest_values_per_row(arr, smallest=1, replace=0)
    array([[0, 1, 0],
           [0, 4, 0]])

    >>> n_smallest_values_per_row(arr, smallest=np.array([1, 2]), replace=np.nan)
    array([[nan,  1., nan],
           [nan,  4.,  8.]])
    """
    # Convert array-like input to a NumPy array and work on a copy so the
    # original object is not modified.
    result = np.asarray(arr).copy()

    # Treat a one-dimensional input as a single row. Reject higher-dimensional
    # input because row-wise selection is only defined for 1D or 2D arrays.
    if result.ndim == 1:
        result = result[np.newaxis, :]
    elif result.ndim != 2:
        raise ValueError("arr must be one- or two-dimensional.")

    # Normalize `smallest` to one integer per row so the masking logic can use
    # the same path for scalar and row-specific selections.
    if np.isscalar(smallest):
        smallest = np.full(result.shape[0], smallest, dtype=np.int64)
    else:
        smallest = np.asarray(smallest, dtype=np.int64)

    # Require a simple one-dimensional selector array.
    if smallest.ndim != 1:
        raise ValueError("smallest must be an integer or a one-dimensional array.")

    # Each row needs exactly one corresponding selection count.
    if len(smallest) != result.shape[0]:
        raise ValueError("smallest must contain one value per row in arr.")

    # Selection counts must be valid for the number of columns available.
    if np.any((smallest < 0) | (smallest > result.shape[1])):
        raise ValueError(
            "smallest values must be between 0 and the number of columns."
        )

    # Build row and column index helpers used to map rank positions back to
    # original column positions.
    row_indices = np.arange(result.shape[0])
    column_indices = np.arange(result.shape[1])

    # Create a rank-position mask. Before remapping, True values mark the first
    # `smallest` positions in each sorted row.
    mask = smallest[:, np.newaxis] > column_indices

    # Sort each row and then compute each element's rank within its row. This
    # lets the rank-position mask be aligned back to the original columns.
    sorted_indices = np.argsort(result, axis=1)
    rank_indices = np.argsort(sorted_indices, axis=1)

    # Reorder the mask from sorted-rank positions into the original column
    # positions of `result`.
    mask = mask[row_indices[:, np.newaxis], rank_indices]

    # Keep selected values in place and replace every unselected value.
    return np.where(mask, result, replace)




def n_largest_values_per_row(
        arr: np.ndarray,
        largest: int | np.ndarray = 6,
        replace=0
        ) -> np.ndarray:
    """
    Keep the n largest values in each row of an array.

    The returned array has the same shape as the input array after
    one-dimensional inputs are reshaped to a single row. Selected values
    remain in their original column positions. Unselected values are replaced
    with `replace`.

    Parameters
    ----------
    arr : numpy.ndarray
        One- or two-dimensional array of values. A one-dimensional input is
        treated as a single row.
    largest : int or numpy.ndarray of int, default 6
        Number of largest values to keep in each row. If an integer, the same
        number is used for every row. If an array, it must contain one integer
        per row in `arr`.
    replace : scalar, default 0
        Value used to replace unselected elements. Use `numpy.nan` to mark
        unselected values as missing.

    Returns
    -------
    numpy.ndarray
        Two-dimensional array with selected values preserved in their original
        positions and all other values replaced.

    Raises
    ------
    ValueError
        If `arr` is not one- or two-dimensional.
    ValueError
        If `largest` is array-like and does not contain one value per row.
    ValueError
        If any value in `largest` is less than 0 or greater than the number
        of columns in `arr`.

    Notes
    -----
    When values are tied, selection is determined by NumPy's row-wise sort
    order.

    Examples
    --------
    >>> arr = np.array([[3, 1, 2], [9, 4, 8]])
    >>> n_largest_values_per_row(arr, largest=1, replace=0)
    array([[3, 0, 0],
           [9, 0, 0]])

    >>> n_largest_values_per_row(arr, largest=np.array([1, 2]), replace=np.nan)
    array([[ 3., nan, nan],
           [ 9., nan,  8.]])
    """
    # Convert array-like input to a NumPy array and work on a copy so the
    # original object is not modified.
    result = np.asarray(arr).copy()

    # Treat a one-dimensional input as a single row. Reject higher-dimensional
    # input because row-wise selection is only defined for 1D or 2D arrays.
    if result.ndim == 1:
        result = result[np.newaxis, :]
    elif result.ndim != 2:
        raise ValueError("arr must be one- or two-dimensional.")

    # Normalize `largest` to one integer per row so the masking logic can use
    # the same path for scalar and row-specific selections.
    if np.isscalar(largest):
        largest = np.full(result.shape[0], largest, dtype=np.int64)
    else:
        largest = np.asarray(largest, dtype=np.int64)

    # Require a simple one-dimensional selector array.
    if largest.ndim != 1:
        raise ValueError("largest must be an integer or a one-dimensional array.")

    # Each row needs exactly one corresponding selection count.
    if len(largest) != result.shape[0]:
        raise ValueError("largest must contain one value per row in arr.")

    # Selection counts must be valid for the number of columns available.
    if np.any((largest < 0) | (largest > result.shape[1])):
        raise ValueError(
            "largest values must be between 0 and the number of columns."
        )

    # Build row and column index helpers used to map rank positions back to
    # original column positions.
    row_indices = np.arange(result.shape[0])
    column_indices = np.arange(result.shape[1])

    # Create a rank-position mask. Before remapping, True values mark the last
    # `largest` positions in each sorted row.
    mask = largest[:, np.newaxis] > column_indices[::-1]

    # Sort each row and then compute each element's rank within its row. This
    # lets the rank-position mask be aligned back to the original columns.
    sorted_indices = np.argsort(result, axis=1)
    rank_indices = np.argsort(sorted_indices, axis=1)

    # Reorder the mask from sorted-rank positions into the original column
    # positions of `result`.
    mask = mask[row_indices[:, np.newaxis], rank_indices]

    # Keep selected values in place and replace every unselected value.
    return np.where(mask, result, replace)
