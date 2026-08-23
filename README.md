# ⚙️ Bearing RUL Prediction

Predict the **Remaining Useful Life (RUL)** of rolling element bearings using machine learning. Upload vibration sensor data and get instant health assessments powered by XGBoost and the XJTU-SY bearing dataset.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
  - [Training the Model](#training-the-model)
  - [Testing the Model](#testing-the-model)
  - [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [Feature Engineering](#feature-engineering)
- [Dataset](#dataset)
- [License](#license)

---

## Overview

Bearing failure is one of the most common causes of rotating machinery breakdown. Early prediction of a bearing's remaining useful life allows operators to schedule maintenance proactively, reducing downtime and preventing catastrophic failures.

This project provides a **full-stack web application** that:

1. Accepts raw vibration signal data (CSV) from accelerometers.
2. Automatically extracts **28 engineered features** (time-domain and frequency-domain).
3. Feeds those features into a trained **XGBoost** regression model.
4. Returns a **RUL prediction in minutes** along with a health status indicator (Healthy / Warning / Critical).

---

## Features

- **🔮 Instant RUL Prediction** — Upload a CSV of vibration data and get the predicted remaining useful life in seconds.
- **📊 28 Engineered Features** — Automatically extracts 14 features per channel (horizontal + vertical) including RMS, peak, kurtosis, crest factor, spectral centroid, and more.
- **🎲 Demo Mode** — Try the predictor without any real data using synthetic vibration signals.
- **📈 Model Dashboard** — View model performance metrics (R², RMSE, MAE) and feature importances.
- **🩺 Health Status Gauge** — Visual gauge showing bearing health as Healthy (green), Warning (amber), or Critical (red).
- **⚡ Fast API Backend** — High-performance async API built with FastAPI.
- **🎨 Modern React Frontend** — Clean, responsive UI with glassmorphism design.

---

## Tech Stack

### Backend

| Technology   | Purpose                          |
| ------------ | -------------------------------- |
| Python 3.10+ | Core language                    |
| FastAPI      | REST API framework               |
| Uvicorn      | ASGI server                      |
| XGBoost      | Gradient boosted tree regression |
| scikit-learn | Preprocessing & evaluation       |
| NumPy/Pandas | Data manipulation                |
| SciPy        | Signal processing & statistics   |
| joblib       | Model serialization              |

### Frontend

| Technology      | Purpose            |
| --------------- | ------------------ |
| React 18        | UI framework       |
| React Router v6 | Client-side routing|
| Vite 5          | Build tool & dev server |

---

## Project Structure

```
RUL-bearing/
├── backend/
│   ├── app/
│   │   ├── __init__.py               # Package init
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── routes.py                 # API endpoints (/predict, /model-info, etc.)
│   │   ├── model.py                  # XGBoost training, prediction & persistence
│   │   ├── feature_extraction.py     # 28-feature extraction engine
│   │   └── data_preprocessing.py     # XJTU-SY data loading & RUL labeling
│   ├── saved_model/
│   │   ├── xgb_rul_model.joblib      # Trained XGBoost model
│   │   ├── scaler.joblib             # Fitted StandardScaler
│   │   └── metrics.joblib            # Saved training metrics
│   ├── train_model.py                # CLI script to train the model
│   ├── test_model.py                 # CLI script to evaluate the model
│   └── requirements.txt              # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx            # Navigation bar
│   │   │   ├── FileUpload.jsx        # Drag-and-drop CSV uploader
│   │   │   ├── RULGauge.jsx          # Visual health gauge
│   │   │   ├── FeatureChart.jsx      # Feature importance bar chart
│   │   │   └── FeaturesTable.jsx     # Extracted features table
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx         # Home / landing page
│   │   │   ├── Predict.jsx           # Prediction page with upload & results
│   │   │   └── About.jsx            # About / how-it-works page
│   │   ├── App.jsx                   # Root component with routing
│   │   ├── main.jsx                  # React entry point
│   │   └── index.css                 # Global styles
│   ├── index.html                    # HTML entry point
│   ├── vite.config.js                # Vite configuration (with API proxy)
│   └── package.json                  # Node.js dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python 3.10+** — [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** — [Download Node.js](https://nodejs.org/)
- **Git** — [Download Git](https://git-scm.com/)

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Train the model (demo mode — no dataset needed)
python train_model.py --demo

# 5. Start the API server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install Node.js dependencies
npm install

# 3. Start the dev server
npm run dev
```

The frontend will be available at `http://localhost:5173` and will proxy API requests to the backend.

---

## Usage

### Training the Model

You can train the model with either synthetic demo data or the real XJTU-SY dataset:

```bash
# Train with synthetic data (quick, no dataset required)
python train_model.py --demo

# Train with real XJTU-SY data
python train_model.py --data-dir /path/to/XJTU-SY-Bearing-Datasets

# Skip hyperparameter tuning for faster training
python train_model.py --demo --no-tune
```

### Testing the Model

Evaluate the saved model and view detailed metrics:

```bash
# Test with synthetic data
python test_model.py --demo

# Quick test (skip per-bearing breakdown)
python test_model.py --demo --quick

# Test with real data
python test_model.py --data-dir /path/to/XJTU-SY-Bearing-Datasets
```

### Running the Application

1. Start the backend: `uvicorn app.main:app --reload --port 8000` (from `backend/`)
2. Start the frontend: `npm run dev` (from `frontend/`)
3. Open `http://localhost:5173` in your browser.
4. Navigate to the **Predict** page, upload a vibration CSV, and click **Predict**.

---

## API Reference

| Method | Endpoint           | Description                                      |
| ------ | ------------------ | ------------------------------------------------ |
| GET    | `/`                | API root — returns version info                  |
| GET    | `/api/health`      | Health check — confirms model is loaded          |
| GET    | `/api/model-info`  | Model metadata, metrics & feature importances    |
| POST   | `/api/predict`     | Predict RUL from an uploaded vibration CSV        |
| POST   | `/api/predict-demo`| Generate a demo prediction with synthetic signals |

### `POST /api/predict`

**Request** (multipart form-data):

| Field                | Type   | Default | Description                                  |
| -------------------- | ------ | ------- | -------------------------------------------- |
| `file`               | File   | —       | CSV with 2 columns (horizontal, vertical)    |
| `operating_condition`| int    | 1       | Operating condition (1, 2, or 3)             |
| `normalized_time`    | float  | 0.5     | Lifecycle position (0 = new, 1 = end-of-life)|

**Response** (JSON):

```json
{
  "predicted_rul": 72.45,
  "health_status": "warning",
  "health_color": "#f59e0b",
  "unit": "minutes",
  "features_used": 30,
  "extracted_features": { "h_rms": 0.0523, "..." : "..." },
  "signal_info": {
    "samples": 32768,
    "duration_seconds": 1.28,
    "filename": "sample.csv"
  }
}
```

---

## Feature Engineering

The system extracts **28 features** from each vibration sample (14 per channel — horizontal and vertical):

### Time-Domain Features (10 per channel)

| Feature        | Description                             |
| -------------- | --------------------------------------- |
| RMS            | Root mean square of the signal          |
| Peak           | Maximum absolute amplitude              |
| Peak-to-Peak   | Difference between max and min          |
| Crest Factor   | Peak / RMS ratio                        |
| Kurtosis       | Tailedness of the amplitude distribution|
| Skewness       | Asymmetry of the amplitude distribution |
| Std Dev        | Standard deviation                      |
| Shape Factor   | RMS / Mean absolute value               |
| Impulse Factor | Peak / Mean absolute value              |
| Margin Factor  | Peak / (Mean of √|signal|)²            |

### Frequency-Domain Features (4 per channel)

| Feature              | Description                            |
| -------------------- | -------------------------------------- |
| Frequency Center     | Spectral centroid (weighted mean freq) |
| Mean Square Frequency | Power-weighted mean of freq²          |
| RMS Frequency        | Root of mean square frequency          |
| Frequency Variance   | Spread of power around the centroid    |

### Additional Input Features

| Feature              | Description                                  |
| -------------------- | -------------------------------------------- |
| Operating Condition  | XJTU-SY condition (1, 2, or 3)              |
| Normalized Time      | Position in the bearing's lifecycle (0 to 1) |

---

## Dataset

This project is built around the **[XJTU-SY Bearing Dataset](https://biaowang.tech/xjtu-sy-bearing-datasets/)** — a widely-used benchmark for bearing RUL prediction research.

- **15 bearings** across 3 operating conditions
- **Run-to-failure** accelerated degradation tests
- **2-channel accelerometer** data (horizontal + vertical) sampled at **25.6 kHz**

| Condition | Speed (RPM) | Radial Load (kN) | Bearings |
| --------- | ----------- | ----------------- | -------- |
| 1         | 2100        | 12.0              | 5        |
| 2         | 2250        | 11.0              | 5        |
| 3         | 2400        | 10.0              | 5        |

> **Note:** The dataset is not included in this repository. You can download it from the [official source](https://biaowang.tech/xjtu-sy-bearing-datasets/) or use `--demo` mode with synthetic data.

---

## License

This project is open source and available under the [MIT License](LICENSE).
