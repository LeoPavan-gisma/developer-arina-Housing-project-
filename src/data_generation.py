"""Generate a reproducible sample dataset for the house-price project."""

from __future__ import annotations

import csv
import random
from pathlib import Path


FIELDS = (
    "area_sqft",
    "bedrooms",
    "bathrooms",
    "age_years",
    "location",
    "property_type",
    "price_inr",
)


def generate_dataset(output_path: Path, rows: int = 300, seed: int = 42) -> Path:
    """Write deterministic synthetic listings to ``output_path``."""
    if rows < 1:
        raise ValueError("rows must be at least 1")

    randomizer = random.Random(seed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    locations = ("City Center", "Suburb", "Outskirts", "Riverside")
    location_premiums = {
        "City Center": 5_000,
        "Suburb": 2_200,
        "Outskirts": 0,
        "Riverside": 3_600,
    }

    with output_path.open("w", newline="", encoding="utf-8") as dataset_file:
        writer = csv.DictWriter(dataset_file, fieldnames=FIELDS)
        writer.writeheader()
        for _ in range(rows):
            area = randomizer.randint(450, 2_800)
            bedrooms = max(1, min(5, round(area / 550) + randomizer.choice((-1, 0, 0, 1))))
            bathrooms = max(1, min(4, bedrooms - randomizer.choice((0, 0, 1))))
            age = randomizer.randint(0, 35)
            location = randomizer.choice(locations)
            property_type = randomizer.choice(("Apartment", "Independent House", "Townhouse"))
            type_premium = {"Apartment": 0, "Independent House": 900, "Townhouse": 450}[property_type]
            noise = randomizer.randint(-1_000, 1_000)
            price = max(
                1_000_000,
                int(area * 7_800 + bedrooms * 520_000 + bathrooms * 260_000
                    + location_premiums[location] * area / 1_000
                    + type_premium * area / 1_000 - age * 32_000 + noise),
            )
            writer.writerow(
                {
                    "area_sqft": area,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "age_years": age,
                    "location": location,
                    "property_type": property_type,
                    "price_inr": price,
                }
            )

    return output_path


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    destination = generate_dataset(project_root / "data" / "generated_house_prices.csv")
    print(f"Generated {destination}")