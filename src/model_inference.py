"""Load the latest persisted model and make validated predictions."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from src.data_preprocessing import validate_record


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"


@lru_cache(maxsize=1)
def load_latest_model() -> tuple[Any, dict[str, Any]]:
    manifest_path = MODELS_DIR / "latest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError("No trained model found. Run scripts/train.py first.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    model_path = MODELS_DIR / manifest["model_file"]
    report_path = MODELS_DIR / manifest["report_file"]
    if not model_path.is_file() or not report_path.is_file():
        raise FileNotFoundError("The latest model version is incomplete. Train the model again.")
    return joblib.load(model_path), json.loads(report_path.read_text(encoding="utf-8"))


def predict_property(record: dict[str, Any]) -> dict[str, Any]:
    normalized = validate_record(record)
    pipeline, report = load_latest_model()
    estimate = float(pipeline.predict(pd.DataFrame([normalized]))[0])
    error_band = float(report.get("absolute_error_90th_percentile", 0))
    return {
        "estimated_price": max(0.0, estimate),
        "estimated_range_low": max(0.0, estimate - error_band),
        "estimated_range_high": estimate + error_band,
        "range_method": "90th percentile of absolute errors on the held-out test set",
        "model_version": report["model_version"],
        "algorithm": report["selected_algorithm"],
    }