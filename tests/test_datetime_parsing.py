import pandas as pd
import pytest

from ebtools.general.datetime_parsing import (
    _parse_datetime_column,
    check_datetime_formats,
    check_datetime_formats_tz,
    check_string_datetime_formats,
)


def test_check_string_datetime_formats_with_single_format():
    result = check_string_datetime_formats(
        "2024-03-14",
        format_list="%Y-%m-%d",
    )

    assert result == pd.Timestamp("2024-03-14")


def test_check_string_datetime_formats_uses_default_formats():
    result = check_string_datetime_formats("2024-03-14")

    assert result == pd.Timestamp("2024-03-14")


def test_check_string_datetime_formats_with_multiple_formats():
    result = check_string_datetime_formats(
        "14/03/2024",
        format_list=["%Y-%m-%d", "%d/%m/%Y"],
    )

    assert result == pd.Timestamp("2024-03-14")


def test_check_string_datetime_formats_raises_for_unmatched_format():
    with pytest.raises(ValueError, match="does not match any format"):
        check_string_datetime_formats(
            "14-03-2024",
            format_list=["%Y/%m/%d", "%d/%m/%Y"],
        )


def test_check_string_datetime_formats_rejects_empty_format_list():
    with pytest.raises(ValueError, match="format_list must contain"):
        check_string_datetime_formats("2024-03-14", format_list=[])


def test_parse_datetime_column_tries_formats_against_unparsed_rows_only():
    df = pd.DataFrame(
        {
            "date": ["2024-03-14", "15/03/2024", "not-a-date"],
            "value": [1, 2, 3],
        }
    )

    result, parsed_by_format, unparsed_rows = _parse_datetime_column(
        df=df.copy(),
        source_colname="date",
        parsed_colname="date_correct",
        format_list=["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"],
    )

    assert parsed_by_format == {
        "%Y-%m-%d": 1,
        "%d/%m/%Y": 1,
        "%Y/%m/%d": 0,
    }
    assert unparsed_rows == 1
    assert result["date_correct"].to_list() == [
        pd.Timestamp("2024-03-14"),
        pd.Timestamp("2024-03-15"),
        pd.NaT,
    ]
    assert "date_correct" not in df.columns


def test_check_datetime_formats_with_mixed_formats_preserves_column_order():
    df = pd.DataFrame(
        {
            "site": ["a", "b"],
            "date": ["2024-03-14", "15/03/2024"],
            "value": [1, 2],
        }
    )

    result = check_datetime_formats(
        df,
        colname="date",
        format_list=["%Y-%m-%d", "%d/%m/%Y"],
    )

    assert result.columns.to_list() == ["site", "date", "value"]
    assert result["date"].to_list() == [
        pd.Timestamp("2024-03-14"),
        pd.Timestamp("2024-03-15"),
    ]


def test_check_datetime_formats_uses_default_formats():
    df = pd.DataFrame({"date": ["2024-03-14"]})

    result = check_datetime_formats(df, colname="date")

    assert result.loc[0, "date"] == pd.Timestamp("2024-03-14")


def test_check_datetime_formats_does_not_mutate_input_dataframe():
    df = pd.DataFrame(
        {
            "site": ["a", "b"],
            "date": ["2024-03-14", "15/03/2024"],
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)

    result = check_datetime_formats(
        df,
        colname="date",
        format_list=["%Y-%m-%d", "%d/%m/%Y"],
    )

    pd.testing.assert_frame_equal(df, original)
    assert result is not df


def test_check_datetime_formats_rejects_missing_column():
    df = pd.DataFrame({"date": ["2024-03-14"]})

    with pytest.raises(KeyError, match="not found"):
        check_datetime_formats(df, colname="missing", format_list="%Y-%m-%d")


def test_check_datetime_formats_rejects_empty_format_list():
    df = pd.DataFrame({"date": ["2024-03-14"]})

    with pytest.raises(ValueError, match="format_list must contain"):
        check_datetime_formats(df, colname="date", format_list=[])


def test_check_datetime_formats_can_raise_for_unparsed_values():
    df = pd.DataFrame({"date": ["2024-03-14", "not-a-date"]})

    with pytest.raises(ValueError, match="1 value"):
        check_datetime_formats(
            df,
            colname="date",
            format_list="%Y-%m-%d",
            raise_on_unparsed=True,
        )


def test_check_datetime_formats_can_return_summary():
    df = pd.DataFrame({"date": ["2024-03-14", "15/03/2024", "not-a-date"]})

    result, summary = check_datetime_formats(
        df,
        colname="date",
        format_list=["%Y-%m-%d", "%d/%m/%Y"],
        report_summary=True,
    )

    assert result["date"].to_list() == [
        pd.Timestamp("2024-03-14"),
        pd.Timestamp("2024-03-15"),
        pd.NaT,
    ]
    assert summary == {
        "total_rows": 3,
        "parsed_rows": 2,
        "unparsed_rows": 1,
        "parsed_by_format": {
            "%Y-%m-%d": 1,
            "%d/%m/%Y": 1,
        },
    }


def test_check_datetime_formats_tz_without_utc_preserves_column_order():
    df = pd.DataFrame(
        {
            "site": ["a", "b"],
            "date": ["2024-03-14T23:30:00Z", "2024-03-15T01:30:00+01:00"],
            "value": [1, 2],
        }
    )

    result = check_datetime_formats_tz(
        df,
        colname="date",
        format_list_tz=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"],
        include_utc=False,
    )

    assert result.columns.to_list() == ["site", "date", "value"]
    assert result["date"].to_list() == [
        pd.Timestamp("2024-03-14 23:30:00"),
        pd.Timestamp("2024-03-15 00:30:00"),
    ]
    assert result["date"].dt.tz is None


def test_check_datetime_formats_tz_uses_default_formats():
    df = pd.DataFrame({"date": ["2024-03-14T23:30:00Z"]})

    result = check_datetime_formats_tz(df, colname="date")

    assert result.loc[0, "date"] == pd.Timestamp("2024-03-14 23:30:00")


def test_check_datetime_formats_tz_rejects_empty_format_list():
    df = pd.DataFrame({"date": ["2024-03-14T23:30:00Z"]})

    with pytest.raises(ValueError, match="format_list_tz must contain"):
        check_datetime_formats_tz(df, colname="date", format_list_tz=[])


def test_check_datetime_formats_tz_rejects_missing_column():
    df = pd.DataFrame({"date": ["2024-03-14T23:30:00Z"]})

    with pytest.raises(KeyError, match="not found"):
        check_datetime_formats_tz(df, colname="missing")


def test_check_datetime_formats_tz_with_utc_preserves_timezone():
    df = pd.DataFrame(
        {
            "site": ["a", "b"],
            "date": ["2024-03-14T23:30:00Z", "2024-03-15T01:30:00+01:00"],
            "value": [1, 2],
        }
    )

    result = check_datetime_formats_tz(
        df,
        colname="date",
        format_list_tz=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"],
        include_utc=True,
    )

    assert result.columns.to_list() == ["site", "date", "value"]
    assert result["date"].to_list() == [
        pd.Timestamp("2024-03-14 23:30:00", tz="UTC"),
        pd.Timestamp("2024-03-15 00:30:00", tz="UTC"),
    ]
    assert str(result["date"].dt.tz) == "UTC"


def test_check_datetime_formats_tz_does_not_mutate_input_dataframe():
    df = pd.DataFrame(
        {
            "site": ["a", "b"],
            "date": ["2024-03-14T23:30:00Z", "2024-03-15T01:30:00+01:00"],
            "value": [1, 2],
        }
    )
    original = df.copy(deep=True)

    result = check_datetime_formats_tz(
        df,
        colname="date",
        format_list_tz=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"],
    )

    pd.testing.assert_frame_equal(df, original)
    assert result is not df


def test_check_datetime_formats_tz_can_raise_for_unparsed_values():
    df = pd.DataFrame(
        {
            "date": ["2024-03-14T23:30:00Z", "not-a-date"],
        }
    )

    with pytest.raises(ValueError, match="1 value"):
        check_datetime_formats_tz(
            df,
            colname="date",
            format_list_tz="%Y-%m-%dT%H:%M:%SZ",
            raise_on_unparsed=True,
        )


def test_check_datetime_formats_tz_can_return_summary():
    df = pd.DataFrame(
        {
            "date": [
                "2024-03-14T23:30:00Z",
                "2024-03-15T01:30:00+01:00",
                "not-a-date",
            ],
        }
    )

    result, summary = check_datetime_formats_tz(
        df,
        colname="date",
        format_list_tz=["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"],
        report_summary=True,
    )

    assert result["date"].to_list() == [
        pd.Timestamp("2024-03-14 23:30:00"),
        pd.Timestamp("2024-03-15 00:30:00"),
        pd.NaT,
    ]
    assert summary == {
        "total_rows": 3,
        "parsed_rows": 2,
        "unparsed_rows": 1,
        "parsed_by_format": {
            "%Y-%m-%dT%H:%M:%SZ": 1,
            "%Y-%m-%dT%H:%M:%S%z": 1,
        },
    }
