"""FastAPI endpoints for house-price predictions."""

from fastapi import FastAPI, HTTPException

from src.data_preprocessing import InputValidationError
from src.model_inference import load_latest_model, predict_property


app = FastAPI(title="House Price Prediction API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    try:
        _, report = load_latest_model()
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return {"status": "ok", "model_version": report["model_version"]}


@app.post("/predict")
def predict(payload: dict) -> dict:
    try:
        return predict_property(payload)
    except InputValidationError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error