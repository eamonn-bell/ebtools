import numpy as np
import pandas as pd
import pytest

from ebtools.general.sp_efa_conversion import (
    current_efa,
    current_sp,
    hour_to_efa,
    make_sp_efa_table,
    sp_to_efa,
)


def test_sp_to_efa_returns_scalar_for_int():
    assert sp_to_efa(1) == 1
    assert sp_to_efa(23) == 4
    assert sp_to_efa(47) == 1


def test_sp_to_efa_returns_array_for_list():
    result = sp_to_efa([1, 8, 23, 47])

    np.testing.assert_array_equal(result, np.array([1, 2, 4, 1]))


@pytest.mark.parametrize("sp", [0, 49, [1, 49]])
def test_sp_to_efa_rejects_out_of_range_values(sp):
    with pytest.raises(ValueError, match="range 1 to 48"):
        sp_to_efa(sp)


@pytest.mark.parametrize("sp", [1.5, "bad", [1, 2.5]])
def test_sp_to_efa_rejects_non_integer_values(sp):
    with pytest.raises(ValueError, match="integer-like"):
        sp_to_efa(sp)


def test_hour_to_efa_returns_scalar_for_int():
    assert hour_to_efa(0) == 1
    assert hour_to_efa(23) == 1
    assert hour_to_efa(24, first_hour=1) == 1


def test_hour_to_efa_returns_array_for_list():
    result = hour_to_efa([0, 4, 12, 23])

    np.testing.assert_array_equal(result, np.array([1, 2, 4, 1]))


def test_hour_to_efa_rejects_invalid_first_hour():
    with pytest.raises(ValueError, match="first_hour"):
        hour_to_efa(0, first_hour=2)


@pytest.mark.parametrize("hour", [-1, 24])
def test_hour_to_efa_rejects_out_of_range_zero_based_hours(hour):
    with pytest.raises(ValueError, match="range 0 to 23"):
        hour_to_efa(hour)


@pytest.mark.parametrize("hour", [0, 25])
def test_hour_to_efa_rejects_out_of_range_one_based_hours(hour):
    with pytest.raises(ValueError, match="range 1 to 24"):
        hour_to_efa(hour, first_hour=1)


def test_current_sp_returns_containing_settlement_period():
    assert current_sp("2024-03-14 06:12:26") == 13
    assert current_sp("2024-03-14 06:30:00") == 14


def test_current_efa_returns_containing_efa_block():
    assert current_efa("2024-03-14 06:12:26") == 2
    assert current_efa("2024-03-14 23:15:00") == 1


def test_make_sp_efa_table_returns_lookup_for_date():
    result = make_sp_efa_table("2024-03-14")

    assert len(result) == 48
    assert result.loc[0, "Datetime"] == pd.Timestamp("2024-03-14 00:00:00")
    assert result.loc[0, "SP"] == 1
    assert result.loc[0, "EFA"] == 1
    assert result.loc[46, "SP"] == 47
    assert result.loc[46, "EFA"] == 1
