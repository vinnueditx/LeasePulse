import os
import time
import uuid
import pickle
import logging
from contextlib import asynccontextmanager
from datetime import datetime

import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from app.schemas import HouseRequest

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("rent_prediction_api")

MODEL_PATH = os.getenv("MODEL_PATH", "models/rent_prediction_model.pkl")
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    if not os.path.exists(MODEL_PATH):
        logger.warning(f"Model file not found at {MODEL_PATH}. Make sure to train or mount it.")
    else:
        with open(MODEL_PATH, "rb") as file:
            model = pickle.load(file)
        logger.info("Production model loaded successfully.")
    yield
    model = None

app = FastAPI(
    title="House Rent Prediction API",
    description="Production ML API for predicting monthly house rent",
    version="1.0.0",
    lifespan=lifespan
)

PREDICTION_COUNTER = Counter("rent_predictions_total", "Total number of rent predictions")
ERROR_COUNTER = Counter("rent_prediction_errors_total", "Total prediction errors")
PREDICTION_LATENCY = Histogram("rent_prediction_latency_seconds", "Prediction request latency")

@app.get("/")
def home():
    return {
        "application": "House Rent Prediction API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }

@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model not loaded")
    return {"status": "healthy", "model": "loaded"}

@app.post("/api/v1/predict")
async def predict_rent(request: HouseRequest):
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model unavailable")

    start_time = time.perf_counter()
    try:
        PREDICTION_COUNTER.inc()

        input_data = pd.DataFrame([{
            "area": request.area,
            "bedrooms": request.bedrooms,
            "bathrooms": request.bathrooms,
            "age": request.age,
            "location": request.location,
            "furnished": request.furnished.value,
            "parking": request.parking.value
        }])

        prediction = max(0.0, float(model.predict(input_data)[0]))
        margin = prediction * 0.10
        lower = max(0.0, prediction - margin)
        upper = prediction + margin
        latency = time.perf_counter() - start_time

        PREDICTION_LATENCY.observe(latency)
        logger.info(f"Prediction generated: INR {prediction:,.2f}")

        return {
            "prediction_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "predicted_monthly_rent": round(prediction, 2),
            "currency": "INR",
            "confidence_interval": {
                "lower_bound": round(lower, 2),
                "upper_bound": round(upper, 2)
            },
            "model_version": "1.0.0",
            "prediction_latency_seconds": round(latency, 4),
            "property": request.model_dump()
        }
    except Exception:
        ERROR_COUNTER.inc()
        logger.exception("Prediction calculation failed")
        raise HTTPException(status_code=500, detail="Internal prediction error")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
