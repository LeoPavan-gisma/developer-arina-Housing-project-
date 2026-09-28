from pathlib import Path

import pytest

from src.data_preprocessing import FEATURES, InputValidationError, load_dataset, validate_record


ROOT = Path(__file__).resolve().parents[1]


def valid_record() -> dict:
    return {
        "Area": 1_500,
        "Bedrooms": 3,
        "Bathrooms": 2,
        "Age": 5,
        "Location": "City Center",
        "Property_Type": "Apartment",
    }


def test_loads_supplied_dataset_without_identifier_feature() -> None:
    features, target = load_dataset(ROOT / "house_prices.csv")
    assert len(features) == 300
    assert list(features.columns) == FEATURES
    assert "Property_ID" not in features.columns
    assert target.name == "Price"


def test_valid_record_is_normalized() -> None:
    record = valid_record() | {"Area": "1500", "Location": " City Center "}
    normalized = validate_record(record)
    assert normalized["Area"] == 1_500
    assert normalized["Location"] == "City Center"


@pytest.mark.parametrize(
    "update, message",
    [({"Area": 99}, "Area must be between"), ({"Bedrooms": 1.5}, "Bedrooms must be a whole number"),
     ({"Location": " "}, "Location must be a non-empty string"), ({"Age": True}, "Age must be a number")],
)
def test_rejects_invalid_inputs(update: dict, message: str) -> None:
    with pytest.raises(InputValidationError, match=message):
        validate_record(valid_record() | update)


def test_rejects_missing_fields() -> None:
    record = valid_record()
    del record["Property_Type"]
    with pytest.raises(InputValidationError, match="Missing required fields"):
        validate_record(record)