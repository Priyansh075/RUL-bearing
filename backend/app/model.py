"""
ML Model Module for Bearing RUL Prediction.

Uses XGBoost Gradient Boosted Trees for regression.
Handles training, prediction, model persistence, and feature importance.
"""

import os
import numpy as np
import pandas as pd
import joblib
from typing import Tuple, Optional, Dict
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor

from app.feature_extraction import FEATURE_NAMES


# Default paths for saved model artifacts
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'saved_model')
MODEL_PATH = os.path.join(MODEL_DIR, 'xgb_rul_model.joblib')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.joblib')
METRICS_PATH = os.path.join(MODEL_DIR, 'metrics.joblib')


def get_training_features() -> list:
    """Get the list of feature columns used for training (excludes metadata)."""
    return FEATURE_NAMES + ['operating_condition', 'normalized_time']


def train_model(
    df: pd.DataFrame,
    test_size: float = 0.2,
    tune_hyperparams: bool = True,
) -> Dict:
    """
    Train an XGBoost model for RUL prediction.
    
    Args:
        df: Feature DataFrame with 'rul' column
        test_size: Fraction of data for testing
        tune_hyperparams: Whether to perform grid search for hyperparameters
        
    Returns:
        Dictionary with model, scaler, metrics, and feature importances
    """
    feature_cols = get_training_features()
    
    X = df[feature_cols].values
    y = df['rul'].values
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    if tune_hyperparams:
        # Grid search for best hyperparameters
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [4, 6, 8],
            'learning_rate': [0.05, 0.1, 0.2],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0],
            'reg_alpha': [0, 0.1],
            'reg_lambda': [1, 2],
        }
        
        # Use a smaller grid for faster training
        param_grid_small = {
            'n_estimators': [200, 300],
            'max_depth': [5, 7],
            'learning_rate': [0.05, 0.1],
            'subsample': [0.8],
            'colsample_bytree': [0.8],
            'reg_alpha': [0.1],
            'reg_lambda': [1],
        }
        
        xgb = XGBRegressor(random_state=42, objective='reg:squarederror')
        grid_search = GridSearchCV(
            xgb,
            param_grid_small,
            cv=3,
            scoring='neg_mean_squared_error',
            n_jobs=-1,
            verbose=1,
        )
        grid_search.fit(X_train_scaled, y_train)
        model = grid_search.best_estimator_
        print(f"Best params: {grid_search.best_params_}")
    else:
        model = XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1,
            random_state=42,
            objective='reg:squarederror',
        )
        model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    metrics = {
        'train_rmse': float(np.sqrt(mean_squared_error(y_train, y_pred_train))),
        'test_rmse': float(np.sqrt(mean_squared_error(y_test, y_pred_test))),
        'train_mae': float(mean_absolute_error(y_train, y_pred_train)),
        'test_mae': float(mean_absolute_error(y_test, y_pred_test)),
        'train_r2': float(r2_score(y_train, y_pred_train)),
        'test_r2': float(r2_score(y_test, y_pred_test)),
        'n_train': len(y_train),
        'n_test': len(y_test),
        'n_features': len(feature_cols),
    }
    
    # Feature importances
    importances = model.feature_importances_
    feature_importance = sorted(
        zip(feature_cols, importances.tolist()),
        key=lambda x: x[1],
        reverse=True,
    )
    
    print(f"\n{'='*50}")
    print(f"Model Training Results")
    print(f"{'='*50}")
    print(f"Train RMSE: {metrics['train_rmse']:.2f} minutes")
    print(f"Test  RMSE: {metrics['test_rmse']:.2f} minutes")
    print(f"Train MAE:  {metrics['train_mae']:.2f} minutes")
    print(f"Test  MAE:  {metrics['test_mae']:.2f} minutes")
    print(f"Train R²:   {metrics['train_r2']:.4f}")
    print(f"Test  R²:   {metrics['test_r2']:.4f}")
    print(f"\nTop 10 Features:")
    for name, imp in feature_importance[:10]:
        print(f"  {name}: {imp:.4f}")
    
    return {
        'model': model,
        'scaler': scaler,
        'metrics': metrics,
        'feature_importance': feature_importance,
    }


def save_model(model, scaler, metrics, feature_importance):
    """Save model artifacts to disk."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump({
        'metrics': metrics,
        'feature_importance': feature_importance,
    }, METRICS_PATH)
    
    print(f"\nModel saved to {MODEL_DIR}")


def load_model() -> Tuple[XGBRegressor, StandardScaler, Dict]:
    """
    Load saved model artifacts.
    
    Returns:
        Tuple of (model, scaler, metadata_dict)
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No saved model found at {MODEL_PATH}. "
            "Run train_model.py first to train and save the model."
        )
    
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    metadata = joblib.load(METRICS_PATH)
    
    return model, scaler, metadata


def predict_rul(
    features: dict,
    model: XGBRegressor,
    scaler: StandardScaler,
    operating_condition: int = 1,
    normalized_time: float = 0.5,
) -> dict:
    """
    Predict RUL from extracted features.
    
    Args:
        features: Dictionary of 28 extracted features
        model: Trained XGBoost model
        scaler: Fitted StandardScaler
        operating_condition: Operating condition (1, 2, or 3)
        normalized_time: Normalized lifecycle position (0-1)
        
    Returns:
        Dictionary with prediction and confidence info
    """
    feature_cols = get_training_features()
    
    # Build feature vector
    feature_vector = []
    for col in feature_cols:
        if col == 'operating_condition':
            feature_vector.append(operating_condition)
        elif col == 'normalized_time':
            feature_vector.append(normalized_time)
        else:
            feature_vector.append(features.get(col, 0.0))
    
    X = np.array([feature_vector])
    X_scaled = scaler.transform(X)
    
    # Predict
    rul_pred = float(model.predict(X_scaled)[0])
    
    # Clamp to reasonable range
    rul_pred = max(0, rul_pred)
    
    # Determine health status based on predicted RUL
    if rul_pred > 80:
        health_status = 'healthy'
        health_color = '#10b981'  # Green
    elif rul_pred > 30:
        health_status = 'warning'
        health_color = '#f59e0b'  # Amber
    else:
        health_status = 'critical'
        health_color = '#ef4444'  # Red
    
    return {
        'predicted_rul': round(rul_pred, 2),
        'health_status': health_status,
        'health_color': health_color,
        'unit': 'minutes',
        'features_used': len(feature_cols),
    }
