from pydantic import BaseModel, Field
from typing import Optional

# I'm defining the input data contract for the API using Pydantic
# This ensures every transaction request is validated before it reaches the model
# If any required field is missing or the wrong type, the API automatically returns a 400 error

class TransactionInput(BaseModel):
    Time: float = Field(..., description="Seconds elapsed between this transaction and the first transaction in the dataset")
    V1: float = Field(..., description="PCA transformed feature 1")
    V2: float = Field(..., description="PCA transformed feature 2")
    V3: float = Field(..., description="PCA transformed feature 3")
    V4: float = Field(..., description="PCA transformed feature 4")
    V5: float = Field(..., description="PCA transformed feature 5")
    V6: float = Field(..., description="PCA transformed feature 6")
    V7: float = Field(..., description="PCA transformed feature 7")
    V8: float = Field(..., description="PCA transformed feature 8")
    V9: float = Field(..., description="PCA transformed feature 9")
    V10: float = Field(..., description="PCA transformed feature 10")
    V11: float = Field(..., description="PCA transformed feature 11")
    V12: float = Field(..., description="PCA transformed feature 12")
    V13: float = Field(..., description="PCA transformed feature 13")
    V14: float = Field(..., description="PCA transformed feature 14")
    V15: float = Field(..., description="PCA transformed feature 15")
    V16: float = Field(..., description="PCA transformed feature 16")
    V17: float = Field(..., description="PCA transformed feature 17")
    V18: float = Field(..., description="PCA transformed feature 18")
    V19: float = Field(..., description="PCA transformed feature 19")
    V20: float = Field(..., description="PCA transformed feature 20")
    V21: float = Field(..., description="PCA transformed feature 21")
    V22: float = Field(..., description="PCA transformed feature 22")
    V23: float = Field(..., description="PCA transformed feature 23")
    V24: float = Field(..., description="PCA transformed feature 24")
    V25: float = Field(..., description="PCA transformed feature 25")
    V26: float = Field(..., description="PCA transformed feature 26")
    V27: float = Field(..., description="PCA transformed feature 27")
    V28: float = Field(..., description="PCA transformed feature 28")
    Amount: float = Field(..., ge=0.01, description="Transaction amount in USD — must be greater than 0")

# I'm defining the response structure so the API always returns data in a consistent format
# The decision field maps the risk score to a human readable label
class PredictionOutput(BaseModel):
    fraud_risk_score: float = Field(..., description="Probability of fraud between 0.0 and 1.0")
    decision: str = Field(..., description="approve, flag, or decline based on risk score thresholds")
    model_version: str = Field(..., description="Version of the model that made this prediction")

# I'm defining the response structure for the health check endpoint
class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str