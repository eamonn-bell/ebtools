import numpy as np
import pytest

from ebtools.general.array_selection import (
    add_newaxis,
    n_largest_values_per_row,
    n_smallest_values_per_row,
)


def test_add_newaxis_with_1d_array():
    arr = np.array([1, 2, 3])
    expected = np.array([[1], [2], [3]])

    result = add_newaxis(arr)

    np.testing.assert_array_equal(result, expected)
    assert result.shape == (3, 1)


def test_add_newaxis_with_list_input():
    result = add_newaxis([1, 2, 3])

    assert isinstance(result, np.ndarray)
    assert result.shape == (3, 1)


def test_add_newaxis_rejects_non_1d_input():
    arr = np.array([[1, 2], [3, 4]])

    with pytest.raises(ValueError, match="one-dimensional"):
        add_newaxis(arr)


def test_n_smallest_values_per_row_with_scalar_selection():
    arr = np.array([[3, 1, 2], [9, 4, 8]])
    expected = np.array([[0, 1, 0], [0, 4, 0]])

    result = n_smallest_values_per_row(arr, smallest=1, replace=0)

    np.testing.assert_array_equal(result, expected)


def test_n_smallest_values_per_row_with_row_specific_selection():
    arr = np.array([[3, 1, 2], [9, 4, 8]])
    expected = np.array([[np.nan, 1, np.nan], [np.nan, 4, 8]])

    result = n_smallest_values_per_row(
        arr,
        smallest=np.array([1, 2]),
        replace=np.nan,
    )

    np.testing.assert_equal(result, expected)


def test_n_smallest_values_per_row_with_list_input():
    expected = np.array([[0, 1, 2]])

    result = n_smallest_values_per_row([3, 1, 2], smallest=2, replace=0)

    np.testing.assert_array_equal(result, expected)


def test_n_smallest_values_per_row_with_zero_selection():
    arr = np.array([[3, 1, 2], [9, 4, 8]])
    expected = np.zeros_like(arr)

    result = n_smallest_values_per_row(arr, smallest=0, replace=0)

    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    "arr, smallest, match",
    [
        (np.zeros((1, 1, 1)), 1, "one- or two-dimensional"),
        (np.array([[3, 1, 2], [9, 4, 8]]), np.array([1]), "one value per row"),
        (np.array([[3, 1, 2], [9, 4, 8]]), -1, "between 0"),
        (np.array([[3, 1, 2], [9, 4, 8]]), 4, "between 0"),
    ],
)
def test_n_smallest_values_per_row_rejects_invalid_inputs(arr, smallest, match):
    with pytest.raises(ValueError, match=match):
        n_smallest_values_per_row(arr, smallest=smallest)


def test_n_largest_values_per_row_with_scalar_selection():
    arr = np.array([[3, 1, 2], [9, 4, 8]])
    expected = np.array([[3, 0, 0], [9, 0, 0]])

    result = n_largest_values_per_row(arr, largest=1, replace=0)

    np.testing.assert_array_equal(result, expected)


def test_n_largest_values_per_row_with_row_specific_selection():
    arr = np.array([[3, 1, 2], [9, 4, 8]])
    expected = np.array([[3, np.nan, np.nan], [9, np.nan, 8]])

    result = n_largest_values_per_row(
        arr,
        largest=np.array([1, 2]),
        replace=np.nan,
    )

    np.testing.assert_equal(result, expected)


def test_n_largest_values_per_row_with_list_input():
    expected = np.array([[3, 0, 2]])

    result = n_largest_values_per_row([3, 1, 2], largest=2, replace=0)

    np.testing.assert_array_equal(result, expected)


def test_n_largest_values_per_row_with_zero_selection():
    arr = np.array([[3, 1, 2], [9, 4, 8]])
    expected = np.zeros_like(arr)

    result = n_largest_values_per_row(arr, largest=0, replace=0)

    np.testing.assert_array_equal(result, expected)


@pytest.mark.parametrize(
    "arr, largest, match",
    [
        (np.zeros((1, 1, 1)), 1, "one- or two-dimensional"),
        (np.array([[3, 1, 2], [9, 4, 8]]), np.array([1]), "one value per row"),
        (np.array([[3, 1, 2], [9, 4, 8]]), -1, "between 0"),
        (np.array([[3, 1, 2], [9, 4, 8]]), 4, "between 0"),
    ],
)
def test_n_largest_values_per_row_rejects_invalid_inputs(arr, largest, match):
    with pytest.raises(ValueError, match=match):
        n_largest_values_per_row(arr, largest=largest)
