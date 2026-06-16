import pandas as pd

from ebtools.general.dataframe_base import adjust_for_clock_change, base_df


def test_adjust_for_clock_change_removes_two_spring_periods():
    df = pd.DataFrame(
        {
            "Date": ["2024-03-31"] * 48,
            "SP": range(1, 49),
        }
    )

    result = adjust_for_clock_change(
        df,
        start_date="2024-03-31",
        end_date="2024-03-31",
    )

    assert len(result) == 46
    assert result["SP"].to_list() == list(range(1, 47))


def test_adjust_for_clock_change_adds_two_autumn_periods():
    df = pd.DataFrame(
        {
            "Date": ["2024-10-27"] * 48,
            "SP": range(1, 49),
        }
    )

    result = adjust_for_clock_change(
        df,
        start_date="2024-10-27",
        end_date="2024-10-27",
    )

    assert len(result) == 50
    assert result["SP"].to_list() == [1, 2, 3, 3, 4, 4, *range(7, 51)]


def test_adjust_for_clock_change_preserves_datetime_date_dtype():
    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-03-31"] * 48),
            "SP": range(1, 49),
        }
    )

    result = adjust_for_clock_change(
        df,
        start_date="2024-03-31",
        end_date="2024-03-31",
    )

    assert pd.api.types.is_datetime64_any_dtype(result["Date"])


def test_base_df_returns_48_settlement_periods_per_normal_day():
    result = base_df(start_date="2024-01-01", end_date="2024-01-02")

    assert len(result) == 96
    assert result.columns.to_list() == ["Date", "SP", "EFA", "Start_Time", "Delivery_Year"]
    assert result.groupby("Date")["SP"].count().to_list() == [48, 48]
    assert result["Delivery_Year"].unique().tolist() == ["2023_24"]


def test_base_df_can_return_start_time_as_string():
    result = base_df(
        start_date="2024-01-01",
        end_date="2024-01-01",
        time_col_str=True,
    )

    assert result.loc[0, "Start_Time"] == "00:00"


def test_base_df_can_adjust_clock_change_periods():
    result = base_df(
        start_date="2024-03-31",
        end_date="2024-03-31",
        add_clock_change_sps=True,
    )

    assert len(result) == 46
    assert result["SP"].to_list() == list(range(1, 47))


def test_base_df_spring_clock_change_keeps_skipped_hour_start_times():
    result = base_df(
        start_date="2024-03-31",
        end_date="2024-03-31",
        time_col_str=True,
        add_clock_change_sps=True,
    )

    assert result.loc[result["SP"].isin([1, 2, 3, 4]), "Start_Time"].to_list() == [
        "00:00",
        "00:30",
        "02:00",
        "02:30",
    ]
    assert result.loc[result["SP"].isin([1, 2, 3, 4]), "EFA"].to_list() == [1, 1, 1, 1]


def test_base_df_autumn_clock_change_keeps_repeated_hour_start_times():
    result = base_df(
        start_date="2024-10-27",
        end_date="2024-10-27",
        time_col_str=True,
        add_clock_change_sps=True,
    )

    assert result.loc[result["SP"].isin([3, 4]), "Start_Time"].to_list() == [
        "01:00",
        "01:00",
        "01:30",
        "01:30",
    ]
    assert result.tail(2)["SP"].to_list() == [49, 50]
    assert result.tail(2)["Start_Time"].to_list() == ["23:00", "23:30"]
    assert result.tail(2)["EFA"].to_list() == [1, 1]
