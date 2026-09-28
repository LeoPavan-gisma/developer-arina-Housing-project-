"""Input loading, feature definitions, and request validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


TARGET = "Price"
NUMERIC_FEATURES = ["Area", "Bedrooms", "Bathrooms", "Age"]
CATEGORICAL_FEATURES = ["Location", "Property_Type"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
CSV_COLUMNS = ["Property_ID", *FEATURES, TARGET]


class InputValidationError(ValueError):
    """Raised when a property record is incomplete or outside supported limits."""


def load_dataset(path: Path) -> tuple[pd.DataFrame, pd.Series]:
    """Load and validate the source CSV, excluding identifiers from model features."""
    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")
    frame = pd.read_csv(path)
    missing_columns = set(CSV_COLUMNS) - set(frame.columns)
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {', '.join(sorted(missing_columns))}")
    if frame.empty:
        raise ValueError("Dataset contains no records")

    frame = frame[FEATURES + [TARGET]].copy()
    for column in NUMERIC_FEATURES + [TARGET]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    if frame.isna().any().any():
        raise ValueError("Dataset contains missing or non-numeric values in required columns")
    if (frame[TARGET] <= 0).any():
        raise ValueError("Price values must be greater than zero")

    return frame[FEATURES], frame[TARGET]


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a single prediction record and return normalized model inputs."""
    missing = [feature for feature in FEATURES if feature not in record]
    if missing:
        raise InputValidationError(f"Missing required fields: {', '.join(missing)}")

    result: dict[str, Any] = {}
    bounds = {"Area": (100, 10_000), "Bedrooms": (1, 10), "Bathrooms": (1, 10), "Age": (0, 150)}
    for feature, (minimum, maximum) in bounds.items():
        raw_value = record[feature]
        if isinstance(raw_value, bool):
            raise InputValidationError(f"{feature} must be a number")
        try:
            value = float(raw_value)
        except (TypeError, ValueError) as error:
            raise InputValidationError(f"{feature} must be a number") from error
        if not minimum <= value <= maximum:
            raise InputValidationError(f"{feature} must be between {minimum} and {maximum}")
        if feature in ("Bedrooms", "Bathrooms", "Age") and not value.is_integer():
            raise InputValidationError(f"{feature} must be a whole number")
        result[feature] = int(value) if value.is_integer() else value

    for feature in CATEGORICAL_FEATURES:
        value = record[feature]
        if not isinstance(value, str) or not value.strip():
            raise InputValidationError(f"{feature} must be a non-empty string")
        result[feature] = value.strip()

    return result