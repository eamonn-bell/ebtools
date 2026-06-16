import pandas as pd
import pytest

from ebtools.general.dataframe_helpers import (
    _date_range_frequency,
    _delivery_year_from_dates,
    _full_week_index,
)


def test_date_range_frequency_returns_supported_frequency():
    assert _date_range_frequency("day") == "D"
    assert _date_range_frequency("efa") == "4h"
    assert _date_range_frequency("SP") == "30min"


def test_date_range_frequency_rejects_unsupported_period():
    with pytest.raises(ValueError, match="period must be"):
        _date_range_frequency("month")


def test_delivery_year_from_dates_labels_april_delivery_year_boundary():
    result = _delivery_year_from_dates(
        pd.Series(["2024-01-01", "2024-03-31", "2024-04-01"])
    )

    assert result == ["2023_24", "2023_24", "2024_25"]


def test_full_week_index_returns_complete_week_shape():
    result = _full_week_index(week=3, sp_col="SP", periods_per_day=2)

    assert result.columns.to_list() == ["Week", "Day", "SP"]
    assert len(result) == 14
    assert result["Week"].unique().tolist() == [3]
    assert result["Day"].to_list() == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6]
    assert result["SP"].to_list() == [1, 2] * 7
