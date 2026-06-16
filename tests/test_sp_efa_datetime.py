import pytest

from ebtools.general.sp_efa_datetime import (
    convert_date_to_efa_datetime,
    convert_datetime_to_date_and_efa,
)


def test_convert_date_to_efa_datetime_returns_start_string():
    assert convert_date_to_efa_datetime("2023-03-14", efa=1) == "2023-03-13T23:00:00"
    assert convert_date_to_efa_datetime("2023-03-14", efa=4) == "2023-03-14T11:00:00"


def test_convert_date_to_efa_datetime_rejects_invalid_efa():
    with pytest.raises(ValueError, match="efa"):
        convert_date_to_efa_datetime("2023-03-14", efa=7)


def test_convert_datetime_to_date_and_efa_returns_delivery_date_and_efa():
    assert convert_datetime_to_date_and_efa("2023-03-13T23:00:00") == ("2023-03-14", 1)
    assert convert_datetime_to_date_and_efa("2023-03-14T11:00:00") == ("2023-03-14", 4)


def test_convert_datetime_to_date_and_efa_rejects_invalid_start_time():
    with pytest.raises(ValueError, match="valid EFA"):
        convert_datetime_to_date_and_efa("2023-03-14T12:00:00")
