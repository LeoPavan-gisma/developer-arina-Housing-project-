import numpy as np

from src import model_inference


class StubModel:
    def predict(self, records):
        assert len(records) == 1
        return np.array([12_000_000.0])


def test_prediction_includes_model_version_and_empirical_range(monkeypatch) -> None:
    monkeypatch.setattr(
        model_inference,
        "load_latest_model",
        lambda: (StubModel(), {
            "model_version": "test-v1",
            "selected_algorithm": "Stub",
            "absolute_error_90th_percentile": 500_000,
        }),
    )
    result = model_inference.predict_property(
        {"Area": 1_500, "Bedrooms": 3, "Bathrooms": 2, "Age": 5,
         "Location": "City Center", "Property_Type": "Apartment"}
    )
    assert result["estimated_price"] == 12_000_000
    assert result["estimated_range_low"] == 11_500_000
    assert result["estimated_range_high"] == 12_500_000
    assert result["model_version"] == "test-v1"