# Local Deployment

1. Use Python 3.11 or newer and create/activate a virtual environment.
2. Install dependencies with `python -m pip install -r requirements.txt`.
3. Train with `python -m scripts.train`.
4. Launch the UI with `streamlit run app/streamlit_app.py`.
5. Optionally start the JSON API with `python -m uvicorn app.api:app --reload`.

Training appends a timestamped model and report under `models/` and updates
`models/latest.json`. Keep model files and manifest together; do not load
untrusted joblib files. The local development server is not authentication or
production infrastructure. Production deployment should add authentication,
request logging, resource limits, monitoring, and a controlled artifact store.