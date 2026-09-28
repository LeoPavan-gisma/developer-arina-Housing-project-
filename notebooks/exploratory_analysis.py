"""Small reproducible EDA report; run with ``python -m notebooks.exploratory_analysis``."""

from pathlib import Path

from src.data_preprocessing import load_dataset


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    features, target = load_dataset(root / "house_prices.csv")
    print(f"Rows: {len(features)}")
    print("Numeric summary:")
    print(features.describe().round(1).to_string())
    print("\nMedian price by location:")
    print(target.groupby(features["Location"]).median().sort_values(ascending=False).to_string())
    print("\nCategory counts:")
    for column in ("Location", "Property_Type"):
        print(f"{column}:\n{features[column].value_counts().to_string()}")