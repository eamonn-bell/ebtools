#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Private helpers for Settlement Period and EFA conversions."""

import datetime

import numpy as np
import pandas as pd

import ebtools.general.helper as helper


EFA_START_HOURS = {
    1: -1,
    2: 3,
    3: 7,
    4: 11,
    5: 15,
    6: 19,
}

TIME_TO_EFA = {
    datetime.time(23, 0): 1,
    datetime.time(3, 0): 2,
    datetime.time(7, 0): 3,
    datetime.time(11, 0): 4,
    datetime.time(15, 0): 5,
    datetime.time(19, 0): 6,
}


def as_integer_array(values: object, name: str) -> np.ndarray:
    """Return values as an integer NumPy array, preserving integer semantics."""
    value_array = helper.force_to_np_array(values)

    try:
        value_int = value_array.astype(int)
    except (TypeError, ValueError):
        raise ValueError(f"{name} values must be integer-like.") from None

    try:
        integer_like = np.all(np.equal(value_array, value_int))
    except TypeError:
        integer_like = False

    if not integer_like:
        raise ValueError(f"{name} values must be integer-like.")

    return value_int


def return_scalar_or_array(
        values: np.ndarray,
        scalar_input: bool
        ) -> int | np.ndarray:
    """Return a scalar integer for scalar input, otherwise return an array."""
    if scalar_input:
        return int(values[0])

    return values


def require_columns(
        df: pd.DataFrame,
        columns: list[str]
        ) -> None:
    """Raise a KeyError if any expected DataFrame columns are missing."""
    missing_cols = [col for col in columns if col not in df.columns]

    if missing_cols:
        raise KeyError(f"Column(s) not found in dataframe: {missing_cols}")


def validate_range(
        values: np.ndarray | pd.Series,
        name: str,
        min_value: int,
        max_value: int
        ) -> None:
    """Raise a ValueError if values fall outside an inclusive range."""
    if np.any((values < min_value) | (values > max_value)):
        raise ValueError(
            f"{name} values must be in the range {min_value} to {max_value}."
        )


def validate_sp_values(values: np.ndarray | pd.Series) -> None:
    """Validate that values are valid Settlement Period numbers."""
    validate_range(values, "SP", 1, 48)
