# House Price Prediction

An end-to-end machine-learning learning project that compares regression
algorithms and serves an indicative house-price estimate through a Streamlit
interface and FastAPI endpoint. The dashboard includes property valuation,
sample-market exploration, model comparison, permutation importance, and a
session-based exportable estimate history. It uses the supplied 300-row dataset; the
root-level `house_prices.csv` is the training source and the copy in `data/` is
preserved as well.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m scripts.train
streamlit run app/streamlit_app.py
```

For the JSON API, open a second terminal and run
`python -m uvicorn app.api:app --reload`. Visit `/docs` for interactive API
documentation. To run tests, use `python -m pytest`; to inspect the dataset, use
`python -m notebooks.exploratory_analysis`.

Generate the detailed Word project report with embedded charts using
`python -m scripts.create_report`. It creates
`docs/House_Price_Prediction_Project_Report.docx` and its PNG figures under
`docs/report_figures/` from the latest trained model report.

## Project Layout

```text
app/                 Streamlit UI and FastAPI endpoints
data/                Preserved copy of the supplied CSV
docs/                Data dictionary, methodology, API, deployment, troubleshooting
config/              Reproducible split, cross-validation, and interpretation settings
models/              Timestamped serialized models and evaluation reports
notebooks/           Reproducible exploratory analysis
scripts/             Training command
src/                 Preprocessing, model training, and inference
tests/               Validation, training, and inference tests
house_prices.csv     Supplied source dataset
requirements.txt     Runtime and test dependencies
```

## Data and Method

The target is `Price` in INR. `Property_ID` is excluded. `Area`, `Bedrooms`,
`Bathrooms`, and `Age` are numeric; `Location` and `Property_Type` are one-hot
encoded. Learned preprocessing is embedded in each scikit-learn pipeline to
prevent train/test leakage. Linear Regression, Random Forest, and Gradient
Boosting are compared with five-fold cross-validation; the best mean CV R²
selects the final pipeline. Evaluation reports MAE, RMSE, R², MAPE, fold mean
and standard deviation, plus held-out permutation importance.

Read [the modeling methodology](docs/methodology.md) and [data dictionary](docs/data_dictionary.md)
for assumptions and interpretation limits. In particular, feature importance is
not causality and the error band is not a guaranteed confidence interval. This
small dataset is suitable for practice, not high-stakes valuation.

## Versioning and Operations

Each training run saves a timestamped `.joblib` pipeline and JSON evaluation
report. `models/latest.json` identifies the active pair. See [deployment](docs/deployment.md),
[API reference](docs/api.md), and [troubleshooting](docs/troubleshooting.md).
Do not load model artifacts from untrusted sources.

## Screenshots

Run the Streamlit quick start to view the valuation workspace, market overview,
and model lab. The UI renders the live evaluation report from the current model
version; estimate history lasts for the active browser session.