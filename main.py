from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from model import TransactionInput, PredictionOutput, HealthResponse

ml_models = {}
MODEL_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading fraud detection model...")
    ml_models["model"] = joblib.load("model.pkl")
    ml_models["scaler"] = joblib.load("scaler.pkl")
    ml_models["feature_names"] = joblib.load("feature_names.pkl")
    print("Model loaded successfully!")
    yield
    ml_models.clear()
    print("Model unloaded")


app = FastAPI(
    title="NovaGuard AI — Fraud Detection API",
    description="A real time credit card fraud detection API powered by a trained Random Forest model. Submit a transaction and receive a fraud risk score and decision instantly.",
    version=MODEL_VERSION,
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        model_loaded="model" in ml_models,
        version=MODEL_VERSION
    )


@app.post("/predict", response_model=PredictionOutput)
def predict(transaction: TransactionInput):
    if "model" not in ml_models:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        data = pd.DataFrame([transaction.model_dump()])

        scaler = ml_models["scaler"]

        # scale Time and Amount together
        scaled_values = scaler.transform(data[["Time", "Amount"]].values)

        data = data.copy()
        data["Time"] = scaled_values[0, 0]
        data["Amount"] = scaled_values[0, 1]

        # reorder columns to match training
        data = data[ml_models["feature_names"]]

        fraud_probability = ml_models["model"].predict_proba(data)[0][1]

        if fraud_probability < 0.3:
            decision = "approve"
        elif fraud_probability < 0.7:
            decision = "flag"
        else:
            decision = "decline"

        return PredictionOutput(
            fraud_risk_score=round(float(fraud_probability), 4),
            decision=decision,
            model_version=MODEL_VERSION
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/")
def root():
    return {
        "message": "Welcome to the NovaGuard AI Fraud Detection API",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict"
    }