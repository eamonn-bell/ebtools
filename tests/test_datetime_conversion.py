import datetime

import pandas as pd
import pytest

from ebtools.general.datetime_conversion import (
    convert_date_to_datetime,
    convert_date_to_datetime_str,
    convert_date_to_first_of_month,
    convert_date_to_last_of_month,
    convert_date_to_standard_date_str,
    convert_datetime_to_date,
    convert_single_datetime_to_sp_end,
    convert_single_datetime_to_sp_start,
    move_date_to_end_of_month,
    move_date_to_start_of_month,
)


@pytest.mark.parametrize(
    "date, expected",
    [
        (
            datetime.datetime(2023, 1, 13, 14, 35),
            datetime.datetime(2023, 1, 13, 14, 30),
        ),
        (
            datetime.datetime(2024, 3, 14, 20, 0),
            datetime.datetime(2024, 3, 14, 20, 0),
        ),
        (
            datetime.datetime(2024, 3, 14, 23, 59),
            datetime.datetime(2024, 3, 14, 23, 30),
        ),
    ],
)
def test_convert_single_datetime_to_sp_start(date, expected):
    assert convert_single_datetime_to_sp_start(date) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        (
            datetime.datetime(2023, 1, 13, 14, 35),
            datetime.datetime(2023, 1, 13, 15, 0),
        ),
        (
            datetime.datetime(2024, 3, 14, 20, 0),
            datetime.datetime(2024, 3, 14, 20, 30),
        ),
        (
            datetime.datetime(2024, 3, 14, 23, 59),
            datetime.datetime(2024, 3, 15, 0, 0),
        ),
    ],
)
def test_convert_single_datetime_to_sp_end(date, expected):
    assert convert_single_datetime_to_sp_end(date) == expected


def test_convert_date_to_standard_date_str_removes_time_component():
    result = convert_date_to_standard_date_str("2024-03-14 15:30:00")

    assert result == "2024-03-14"


def test_convert_date_to_datetime_start_of_day():
    result = convert_date_to_datetime("2024-03-14", position="start")

    assert result == "2024-03-14 00:00:00"


def test_convert_date_to_datetime_end_of_day():
    result = convert_date_to_datetime("2024-03-14", position="end")

    assert result == "2024-03-14 23:59:59"


def test_convert_date_to_datetime_supports_custom_smallest_time_unit():
    result = convert_date_to_datetime(
        "2024-03-14",
        position="end",
        smallest_time_unit="1min",
    )

    assert result == "2024-03-14 23:59:00"


def test_convert_date_to_datetime_uses_custom_input_format():
    result = convert_date_to_datetime(
        "14/03/2024",
        date_format="%d/%m/%Y",
    )

    assert result == "2024-03-14 00:00:00"


def test_convert_datetime_to_date_normalises_scalar_string():
    result = convert_datetime_to_date("2024-03-14 15:30:00")

    assert result == pd.Timestamp("2024-03-14 00:00:00")


def test_convert_datetime_to_date_normalises_timestamp():
    result = convert_datetime_to_date(pd.Timestamp("2024-03-14 15:30:00"))

    assert result == pd.Timestamp("2024-03-14 00:00:00")


def test_convert_datetime_to_date_normalises_series():
    values = pd.Series(
        pd.to_datetime(["2024-03-14 15:30:00", "2024-03-15 01:00:00"]),
        name="Datetime",
    )
    expected = pd.Series(
        pd.to_datetime(["2024-03-14", "2024-03-15"]),
        name="Datetime",
    )

    result = convert_datetime_to_date(values)

    pd.testing.assert_series_equal(result, expected)


def test_convert_datetime_to_date_can_return_python_date_scalar():
    result = convert_datetime_to_date(
        "2024-03-14 15:30:00",
        as_python_date=True,
    )

    assert result == datetime.date(2024, 3, 14)


def test_convert_datetime_to_date_can_return_python_date_series():
    values = pd.Series(
        pd.to_datetime(["2024-03-14 15:30:00", "2024-03-15 01:00:00"]),
        name="Datetime",
    )
    expected = pd.Series(
        [datetime.date(2024, 3, 14), datetime.date(2024, 3, 15)],
        name="Datetime",
    )

    result = convert_datetime_to_date(values, as_python_date=True)

    pd.testing.assert_series_equal(result, expected)


def test_convert_date_to_datetime_rejects_invalid_position():
    with pytest.raises(ValueError, match="position must be"):
        convert_date_to_datetime("2024-03-14", position="middle")


def test_convert_date_to_datetime_str_api_start_format():
    result = convert_date_to_datetime_str("2024-03-14", position="start")

    assert result == "2024-03-14T00:00:00Z"


def test_convert_date_to_datetime_str_api_end_format():
    result = convert_date_to_datetime_str("2024-03-14", position="end")

    assert result == "2024-03-14T23:59:59Z"


def test_convert_date_to_datetime_str_uses_custom_return_format():
    result = convert_date_to_datetime_str(
        "2024-03-14",
        position="start",
        return_format="%Y%m%d%H%M",
    )

    assert result == "202403140000"


def test_convert_date_to_datetime_str_rejects_invalid_position():
    with pytest.raises(ValueError, match="position must be"):
        convert_date_to_datetime_str("2024-03-14", position="middle")


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-02-15", "2024-02-01"),
        ("2023-12-31", "2023-12-01"),
    ],
)
def test_convert_date_to_first_of_month_as_string(date, expected):
    assert convert_date_to_first_of_month(date, as_string=True) == expected


def test_convert_date_to_first_of_month_as_timestamp():
    assert convert_date_to_first_of_month(
        "2024-02-15",
        as_string=False,
    ) == pd.Timestamp("2024-02-01")


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-02-15", "2024-02-29"),
        ("2023-12-15", "2023-12-31"),
    ],
)
def test_convert_date_to_last_of_month_as_string(date, expected):
    assert convert_date_to_last_of_month(date, as_string=True) == expected


def test_convert_date_to_last_of_month_as_timestamp():
    assert convert_date_to_last_of_month(
        "2024-02-15",
        as_string=False,
    ) == pd.Timestamp("2024-02-29")


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-02-15", pd.Timestamp("2024-02-01")),
        ("2023-12-31", pd.Timestamp("2023-12-01")),
    ],
)
def test_move_date_to_start_of_month_with_scalar(date, expected):
    assert move_date_to_start_of_month(date) == expected


def test_move_date_to_start_of_month_with_series():
    dates = pd.Series(pd.to_datetime(["2024-02-15", "2023-12-31"]))
    expected = pd.Series(pd.to_datetime(["2024-02-01", "2023-12-01"]))

    pd.testing.assert_series_equal(
        move_date_to_start_of_month(dates),
        expected,
    )


def test_move_date_to_start_of_month_with_datetime_index():
    dates = pd.DatetimeIndex(["2024-02-15", "2023-12-31"])
    expected = pd.DatetimeIndex(["2024-02-01", "2023-12-01"])

    pd.testing.assert_index_equal(
        move_date_to_start_of_month(dates),
        expected,
    )


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-02-15", pd.Timestamp("2024-02-29")),
        ("2023-12-31", pd.Timestamp("2023-12-31")),
    ],
)
def test_move_date_to_end_of_month_with_scalar(date, expected):
    assert move_date_to_end_of_month(date) == expected


def test_move_date_to_end_of_month_with_series():
    dates = pd.Series(pd.to_datetime(["2024-02-15", "2023-12-31"]))
    expected = pd.Series(pd.to_datetime(["2024-02-29", "2023-12-31"]))

    pd.testing.assert_series_equal(
        move_date_to_end_of_month(dates),
        expected,
    )


def test_move_date_to_end_of_month_with_datetime_index():
    dates = pd.DatetimeIndex(["2024-02-15", "2023-12-31"])
    expected = pd.DatetimeIndex(["2024-02-29", "2023-12-31"])

    pd.testing.assert_index_equal(
        move_date_to_end_of_month(dates),
        expected,
    )
