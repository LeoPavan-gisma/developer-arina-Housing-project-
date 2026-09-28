"""Train and compare house-price models; save the winning pipeline and report."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data_preprocessing import CATEGORICAL_FEATURES, FEATURES, NUMERIC_FEATURES, load_dataset


RANDOM_STATE = 42


def build_pipeline(regressor: Any) -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="most_frequent")),
               ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline(steps=[("preprocessor", preprocessor), ("regressor", regressor)])


def model_candidates(random_state: int = RANDOM_STATE) -> dict[str, Any]:
    return {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(
            n_estimators=250, min_samples_leaf=2, random_state=random_state, n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=150, learning_rate=0.05, max_depth=2, random_state=random_state
        ),
    }


def _metrics(actual: pd.Series, predicted: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(mean_absolute_error(actual, predicted)),
        "rmse": float(np.sqrt(mean_squared_error(actual, predicted))),
        "r2": float(r2_score(actual, predicted)),
        "mape": float(mean_absolute_percentage_error(actual, predicted) * 100),
    }


def train_and_evaluate(data_path: Path, models_dir: Path) -> dict[str, Any]:
    """Compare three regression approaches and persist the CV-selected pipeline."""
    project_root = Path(__file__).resolve().parents[1]
    config = json.loads((project_root / "config" / "training.json").read_text(encoding="utf-8"))
    random_state = int(config["random_state"])
    features, target = load_dataset(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=float(config["test_size"]), random_state=random_state
    )
    cross_validator = KFold(
        n_splits=int(config["cv_folds"]), shuffle=True, random_state=random_state
    )
    comparisons: dict[str, dict[str, float]] = {}
    fitted: dict[str, Pipeline] = {}

    for name, estimator in model_candidates(random_state).items():
        pipeline = build_pipeline(estimator)
        cv_scores = cross_val_score(
            pipeline, X_train, y_train, cv=cross_validator, scoring="r2", n_jobs=1
        )
        pipeline.fit(X_train, y_train)
        fitted[name] = pipeline
        comparisons[name] = {
            "cv_r2_mean": float(cv_scores.mean()),
            "cv_r2_std": float(cv_scores.std()),
            **_metrics(y_test, pipeline.predict(X_test)),
        }

    best_name = max(comparisons, key=lambda name: comparisons[name]["cv_r2_mean"])
    best_pipeline = fitted[best_name]
    test_residuals = np.abs(y_test.to_numpy() - best_pipeline.predict(X_test))
    error_band_90 = float(np.quantile(test_residuals, 0.9))
    interpretation = permutation_importance(
        best_pipeline, X_test, y_test, scoring="r2",
        n_repeats=int(config["permutation_repeats"]), random_state=random_state, n_jobs=1
    )
    importance = sorted(
        [
            {"feature": feature, "importance_mean": float(mean), "importance_std": float(std)}
            for feature, mean, std in zip(FEATURES, interpretation.importances_mean,
                                          interpretation.importances_std, strict=True)
        ],
        key=lambda item: item["importance_mean"],
        reverse=True,
    )

    models_dir.mkdir(parents=True, exist_ok=True)
    version = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    model_filename = f"house_price_{version}.joblib"
    trained_at = datetime.now(timezone.utc).isoformat()
    report: dict[str, Any] = {
        "model_version": version,
        "trained_at_utc": trained_at,
        "dataset": str(data_path),
        "rows": int(len(features)),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "features": FEATURES,
        "algorithms": comparisons,
        "selected_algorithm": best_name,
        "selected_metrics": comparisons[best_name],
        "absolute_error_90th_percentile": error_band_90,
        "feature_importance": importance,
        "interpretation_method": "Permutation importance on held-out test rows (R2 decrease)",
        "random_state": random_state,
        "model_file": model_filename,
    }
    joblib.dump(best_pipeline, models_dir / model_filename)
    report_path = models_dir / f"report_{version}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (models_dir / "latest.json").write_text(
        json.dumps({"model_version": version, "model_file": model_filename,
                    "report_file": report_path.name}, indent=2),
        encoding="utf-8",
    )
    return report


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    report = train_and_evaluate(project_root / "house_prices.csv", project_root / "models")
    print(json.dumps(report, indent=2))