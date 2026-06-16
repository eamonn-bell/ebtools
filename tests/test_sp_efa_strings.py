import numpy as np
import pytest

from ebtools.general.sp_efa_strings import make_efa_from_string, make_sp_from_string


def test_make_sp_from_string_returns_scalar_and_array():
    assert make_sp_from_string("15:00") == 31
    assert make_sp_from_string("15:00", start=False) == 30

    result = make_sp_from_string(["00:00", "00:30", "23:30"])

    np.testing.assert_array_equal(result, np.array([1, 2, 48]))


def test_make_sp_from_string_rejects_non_half_hour_time():
    with pytest.raises(ValueError, match="half-hour"):
        make_sp_from_string("15:15")


def test_make_efa_from_string_returns_scalar_and_array():
    assert make_efa_from_string("15:00") == 5
    assert make_efa_from_string("15:00", start=False) == 4

    result = make_efa_from_string(["00:00", "11:00", "23:30"])

    np.testing.assert_array_equal(result, np.array([1, 4, 1]))


def test_make_efa_from_string_rejects_non_half_hour_time():
    with pytest.raises(ValueError, match="half-hour"):
        make_efa_from_string("15:15")
