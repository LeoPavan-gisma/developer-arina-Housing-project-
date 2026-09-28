"""Train models from the supplied house_prices.csv file."""

from pathlib import Path

from src.model_training import train_and_evaluate


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    report = train_and_evaluate(root / "house_prices.csv", root / "models")
    print(f"Selected: {report['selected_algorithm']}")
    print(f"Test MAE: ₹{report['selected_metrics']['mae']:,.0f}")
    print(f"Test RMSE: ₹{report['selected_metrics']['rmse']:,.0f}")
    print(f"Test R²: {report['selected_metrics']['r2']:.3f}")
    print(f"Model version: {report['model_version']}")