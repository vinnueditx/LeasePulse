# LeasePulse
Production ML API for predicting monthly house rent using FastAPI, Scikit-Learn, and Pydantic. Features real-time inference with confidence intervals, Prometheus metrics for latency and error tracking, automated health checks, Docker containerization, and a robust CI/CD test suite. Designed for high-throughput, observable model serving.
# RentifyML — House Rent Prediction API

RentifyML is a production-grade machine learning inference service built to predict monthly residential house rent in real-time. Designed with enterprise best practices, the service exposes high-throughput RESTful endpoints using **FastAPI**, validates complex housing attributes via **Pydantic v2**, and exports production observability metrics directly to **Prometheus**.

---

## 🚀 Key Features

- **Fast & Scalable Inference:** Sub-millisecond latency model serving powered by FastAPI and Uvicorn.
- **Strict Data Validation:** Type checking, range enforcement, and categorical constraints using Pydantic schemas.
- **Estimated Confidence Bounds:** Automatically returns lower and upper valuation margins alongside point estimates.
- **Production Observability:** Native Prometheus metrics tracking prediction counts, error rates, and request latency histograms (`/metrics`).
- **Containerized & CI-Ready:** Multi-stage Docker setup and GitHub Actions CI workflow for automated testing and dependency validation.
- **Health Checks & Lifecycle Management:** Built-in `/health` endpoints using FastAPI lifespan handlers to prevent downtime and traffic routing to uninitialized models.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI, Uvicorn
- **ML Runtime:** Scikit-Learn, Pandas, NumPy
- **Monitoring:** Prometheus Client (`prometheus_client`)
- **Data Modeling:** Pydantic v2
- **Testing:** Pytest, HTTPX
- **DevOps:** Docker, GitHub Actions

---

## 📋 API Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API status, root metadata, and link to docs |
| `GET` | `/health` | Liveness and model loading status |
| `GET` | `/metrics` | Prometheus metrics scrape target |
| `POST` | `/api/v1/predict` | Main rent estimation inference endpoint |

### Example Request (`POST /api/v1/predict`)

```json
{
  "area": 1250.0,
  "bedrooms": 3,
  "bathrooms": 2,
  "age": 5,
  "location": "Indiranagar, Bangalore",
  "furnished": "Semi",
  "parking": "Yes"
}
