"""
API Routes for the Bearing RUL Prediction service.
"""

import io
import numpy as np
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional

from app.feature_extraction import extract_all_features, FEATURE_NAMES
from app.model import load_model, predict_rul


router = APIRouter(prefix="/api", tags=["prediction"])

# Global model cache (loaded on startup)
_model = None
_scaler = None
_metadata = None


def init_model():
    """Load model into memory on startup."""
    global _model, _scaler, _metadata
    try:
        _model, _scaler, _metadata = load_model()
        print("[OK] Model loaded successfully")
    except FileNotFoundError as e:
        print(f"[WARN] {e}")
        print("   The API will return errors until a model is trained.")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": _model is not None,
    }


@router.get("/model-info")
async def model_info():
    """Get model metadata, metrics, and feature importances."""
    if _metadata is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Train the model first using the /api/train endpoint or train_model.py script."
        )
    
    return {
        "model_type": "XGBoost (Gradient Boosted Trees)",
        "metrics": _metadata['metrics'],
        "feature_importance": [
            {"feature": name, "importance": round(imp, 4)}
            for name, imp in _metadata['feature_importance']
        ],
        "total_features": len(FEATURE_NAMES) + 2,  # +2 for operating_condition, normalized_time
        "feature_names": FEATURE_NAMES,
    }


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    operating_condition: int = Form(default=1),
    normalized_time: float = Form(default=0.5),
):
    """
    Predict RUL from an uploaded vibration CSV file.
    
    The CSV file should have 2 columns:
    - Column 1: Horizontal vibration signal
    - Column 2: Vertical vibration signal
    
    Each column should contain vibration amplitude values
    (typically 32,768 data points for XJTU-SY data).
    """
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Train the model first."
        )
    
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported. Please upload a .csv file with 2 columns (horizontal, vertical vibration)."
        )
    
    try:
        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), header=None)
        
        if df.shape[1] < 2:
            raise HTTPException(
                status_code=400,
                detail=f"CSV must have at least 2 columns (horizontal, vertical). Found {df.shape[1]} column(s)."
            )
        
        horizontal = df.iloc[:, 0].values.astype(np.float64)
        vertical = df.iloc[:, 1].values.astype(np.float64)
        
        if len(horizontal) < 100:
            raise HTTPException(
                status_code=400,
                detail=f"Signal too short ({len(horizontal)} points). Need at least 100 data points."
            )
        
        # Extract features
        features = extract_all_features(horizontal, vertical)
        
        # Predict
        result = predict_rul(
            features=features,
            model=_model,
            scaler=_scaler,
            operating_condition=operating_condition,
            normalized_time=normalized_time,
        )
        
        # Add extracted features to response
        result['extracted_features'] = {
            k: round(v, 6) for k, v in features.items()
        }
        result['signal_info'] = {
            'samples': len(horizontal),
            'duration_seconds': round(len(horizontal) / 25600, 3),
            'filename': file.filename,
        }
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/predict-demo")
async def predict_demo():
    """
    Generate a demo prediction using synthetic vibration data.
    Useful for testing the UI without uploading real data.
    """
    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Train the model first."
        )
    
    # Generate synthetic vibration signal simulating mild degradation
    np.random.seed(None)  # Random each time
    n_points = 32768
    t = np.linspace(0, 1.28, n_points)
    
    # Base vibration + some fault-like impulses
    degradation_level = np.random.uniform(0.1, 0.9)
    base_freq = 2100 / 60  # Shaft frequency at ~2100 RPM
    
    horizontal = (
        0.05 * np.sin(2 * np.pi * base_freq * t)
        + 0.02 * degradation_level * np.sin(2 * np.pi * 4 * base_freq * t)
        + 0.01 * np.random.randn(n_points) * (1 + degradation_level)
    )
    
    vertical = (
        0.04 * np.sin(2 * np.pi * base_freq * t + np.pi / 4)
        + 0.03 * degradation_level * np.sin(2 * np.pi * 3 * base_freq * t)
        + 0.01 * np.random.randn(n_points) * (1 + degradation_level)
    )
    
    # Extract features
    features = extract_all_features(horizontal, vertical)
    
    # Random operating condition and lifecycle position
    op_cond = np.random.choice([1, 2, 3])
    norm_time = degradation_level
    
    # Predict
    result = predict_rul(
        features=features,
        model=_model,
        scaler=_scaler,
        operating_condition=op_cond,
        normalized_time=norm_time,
    )
    
    result['extracted_features'] = {
        k: round(v, 6) for k, v in features.items()
    }
    result['signal_info'] = {
        'samples': n_points,
        'duration_seconds': 1.28,
        'filename': 'demo_signal.csv',
        'is_demo': True,
        'degradation_level': round(degradation_level, 2),
    }
    
    return result
