import json

from src.model_training import train_and_evaluate


def test_training_compares_models_and_writes_versioned_artifacts(tmp_path) -> None:
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[1]
    report = train_and_evaluate(project_root / "house_prices.csv", tmp_path)

    assert len(report["algorithms"]) == 3
    assert report["training_rows"] == 240
    assert report["test_rows"] == 60
    assert report["selected_metrics"]["mae"] >= 0
    assert len(report["feature_importance"]) == 6
    assert (tmp_path / report["model_file"]).is_file()
    assert json.loads((tmp_path / "latest.json").read_text())[
        "model_version"
    ] == report["model_version"]