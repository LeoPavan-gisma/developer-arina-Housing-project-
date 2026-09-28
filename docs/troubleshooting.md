# Troubleshooting

- **No trained model found:** run `python -m scripts.train` from the project root.
- **Dataset not found:** ensure the supplied `house_prices.csv` is at the project
  root; training intentionally reads that file.
- **Missing CSV columns:** compare the header against the data dictionary and
  retain the original `Price` target spelling.
- **HTTP 422 / input error:** send all six documented features; numbers must be
  within the limits shown by the web form, and category values must be non-empty.
- **Model load error after moving artifacts:** restore the manifest, model, and
  matching report in `models/` from the same training version.
- **Predictions seem implausible:** inspect source data quality and category
  coverage, compare holdout errors, then retrain; the provided dataset is small.