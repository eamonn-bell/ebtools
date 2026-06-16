import pytest
import pandas as pd
import pytz

from ebtools.general.datetime_calendar import (
    bst_date_range,
    get_daylight_savings_dates,
    is_year_leap_year,
)


@pytest.mark.parametrize(
    "year, expected",
    [
        (2024, True),
        (2023, False),
        (1900, False),
        (2000, True),
    ],
)
def test_is_year_leap_year(year, expected):
    assert is_year_leap_year(year) is expected


def test_get_daylight_savings_dates_returns_datetime_index_by_default():
    result = get_daylight_savings_dates()

    assert isinstance(result, pd.DatetimeIndex)
    assert result[0] != pd.Timestamp("0001-01-01")


def test_get_daylight_savings_dates_can_return_datetime_list():
    result = get_daylight_savings_dates(as_pandas_timestamp=False)

    assert isinstance(result, list)
    assert result[0].year > 1


def test_get_daylight_savings_dates_rejects_invalid_region():
    with pytest.raises(pytz.UnknownTimeZoneError):
        get_daylight_savings_dates(region="Not/A_Region")


def test_bst_date_range_returns_inclusive_range_for_known_year():
    result = bst_date_range(2024)

    assert isinstance(result, pd.DatetimeIndex)
    assert result[0] == pd.Timestamp("2024-03-31")
    assert result[-1] == pd.Timestamp("2024-10-27")
    assert len(result) == 211


def test_bst_date_range_rejects_unknown_year():
    with pytest.raises(ValueError, match="No UK clock-change dates"):
        bst_date_range(2031)
