import numpy as np
import pytest

from ebtools.general.helper import (
    force_to_list,
    force_to_np_array,
    make_dict_keys_from_list,
    sort_dict_by_keys,
)


def test_sort_dict_by_keys_returns_items_in_sorted_key_order():
    result = sort_dict_by_keys({"beta": 2, "alpha": 1, "gamma": 3})

    assert list(result) == ["alpha", "beta", "gamma"]
    assert result == {"alpha": 1, "beta": 2, "gamma": 3}


def test_make_dict_keys_from_list_aligns_list_values():
    result = make_dict_keys_from_list(["A", "LongName"], print_to_console=False)

    assert result == ["'A'       : ,", "'LongName': ,"]


def test_make_dict_keys_from_list_accepts_scalar_string():
    result = make_dict_keys_from_list("Price", print_to_console=False)

    assert result == ["'Price': ,"]


def test_make_dict_keys_from_list_accepts_numpy_array():
    result = make_dict_keys_from_list(
        np.array(["A", "LongName"]),
        print_to_console=False,
    )

    assert result == ["'A'       : ,", "'LongName': ,"]


def test_make_dict_keys_from_list_raises_for_empty_input():
    with pytest.raises(ValueError, match="must contain at least one value"):
        make_dict_keys_from_list([], print_to_console=False)


def test_make_dict_keys_from_list_prints_generated_keys(capsys):
    result = make_dict_keys_from_list(["A", "LongName"], print_to_console=True)

    assert result == ["'A'       : ,", "'LongName': ,"]
    assert capsys.readouterr().out == "'A'       : ,\n'LongName': ,\n"


def test_force_to_list_wraps_scalar_value():
    assert force_to_list("Price") == ["Price"]


def test_force_to_list_returns_existing_list_unchanged():
    value = ["Price", "Volume"]

    result = force_to_list(value)

    assert result is value


def test_force_to_list_returns_numpy_array_unchanged():
    value = np.array([1, 2])

    result = force_to_list(value)

    assert result is value


def test_force_to_np_array_wraps_scalar_as_one_dimensional_array():
    result = force_to_np_array(1)

    np.testing.assert_array_equal(result, np.array([1]))


def test_force_to_np_array_converts_list_to_array():
    result = force_to_np_array([1, 2])

    np.testing.assert_array_equal(result, np.array([1, 2]))


def test_force_to_np_array_accepts_numpy_array():
    value = np.array([1, 2])

    result = force_to_np_array(value)

    np.testing.assert_array_equal(result, value)
