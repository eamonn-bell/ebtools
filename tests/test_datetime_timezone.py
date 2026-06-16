import pandas as pd
import pytest

from ebtools.general.datetime_timezone import (
    convert_datetime_by_tz,
    convert_datetime_remove_tz_aware,
)


def test_convert_datetime_remove_tz_aware_returns_copy():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(
                ["2024-01-01 12:00:00+00:00", "2024-01-02 13:00:00+00:00"],
                utc=True,
            ),
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2024-01-01 12:00:00", "2024-01-02 13:00:00"]),
        name="Date",
    )

    result = convert_datetime_remove_tz_aware(df, colname="Date")

    pd.testing.assert_series_equal(result["Date"], expected)
    pd.testing.assert_frame_equal(df, original)


def test_convert_datetime_remove_tz_aware_leaves_naive_column_unchanged():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01 12:00:00"]),
            "value": [1],
        }
    )
    original = df.copy(deep=True)

    result = convert_datetime_remove_tz_aware(df, colname="Date")

    pd.testing.assert_series_equal(result["Date"], original["Date"])
    pd.testing.assert_frame_equal(df, original)


def test_convert_datetime_remove_tz_aware_rejects_missing_column():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01 12:00:00"])})

    with pytest.raises(KeyError):
        convert_datetime_remove_tz_aware(df, colname="missing")


def test_convert_datetime_by_tz_returns_copy_with_local_naive_times():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-07-01 12:00:00", "2024-12-01 12:00:00"]),
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)
    expected = pd.Series(
        pd.to_datetime(["2024-07-01 13:00:00", "2024-12-01 12:00:00"]),
        name="Date",
    )

    result = convert_datetime_by_tz(df, colname="Date", use_tz="Europe/London")

    pd.testing.assert_series_equal(result["Date"], expected)
    pd.testing.assert_frame_equal(df, original)


def test_convert_datetime_by_tz_preserves_column_order():
    df = pd.DataFrame(
        {
            "site": ["a"],
            "Date": pd.to_datetime(["2024-07-01 12:00:00"]),
            "value": [1],
        }
    )

    result = convert_datetime_by_tz(df, colname="Date", use_tz="Europe/London")

    assert result.columns.to_list() == ["site", "Date", "value"]


def test_convert_datetime_by_tz_supports_custom_timezone():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01 12:00:00"])})

    result = convert_datetime_by_tz(df, colname="Date", use_tz="Europe/Paris")

    assert result.loc[0, "Date"] == pd.Timestamp("2024-01-01 13:00:00")


def test_convert_datetime_by_tz_rejects_missing_column():
    df = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01 12:00:00"])})

    with pytest.raises(KeyError):
        convert_datetime_by_tz(df, colname="missing")


def test_convert_datetime_by_tz_rejects_string_column():
    df = pd.DataFrame({"Date": ["2024-01-01 12:00:00"]})

    with pytest.raises(AttributeError, match=".dt accessor"):
        convert_datetime_by_tz(df, colname="Date")


def test_convert_datetime_by_tz_rejects_already_aware_column():
    df = pd.DataFrame(
        {"Date": pd.to_datetime(["2024-01-01 12:00:00+00:00"], utc=True)}
    )

    with pytest.raises(TypeError, match="Already tz-aware"):
        convert_datetime_by_tz(df, colname="Date")
