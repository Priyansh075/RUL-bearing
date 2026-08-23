"""
Model Testing / Evaluation Script.

Loads the saved XGBoost model and evaluates it on a holdout dataset,
reporting R² score and other key regression metrics.

Usage:
    # Test with synthetic demo data:
    python test_model.py --demo

    # Test with real XJTU-SY dataset:
    python test_model.py --data-dir /path/to/XJTU-SY-Bearing-Datasets

    # Quick test (skip per-bearing breakdown):
    python test_model.py --demo --quick
"""

import argparse
import sys
import os
import numpy as np
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from app.data_preprocessing import build_feature_matrix, generate_synthetic_dataset
from app.model import load_model, get_training_features


def print_header(title: str, char: str = "=", width: int = 60):
    """Print a formatted section header."""
    print(f"\n{char * width}")
    print(f"  {title}")
    print(f"{char * width}")


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    label: str = "Test",
) -> dict:
    """
    Compute and return regression metrics for a set of predictions.

    Returns:
        Dictionary with rmse, mae, r2, max_error, and median_ae.
    """
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred))
    residuals = y_true - y_pred
    max_err = float(np.max(np.abs(residuals)))
    median_ae = float(np.median(np.abs(residuals)))
    mean_residual = float(np.mean(residuals))
    std_residual = float(np.std(residuals))

    metrics = {
        "label": label,
        "n_samples": len(y_true),
        "rmse": rmse,
        "mae": mae,
        "median_ae": median_ae,
        "r2": r2,
        "max_error": max_err,
        "mean_residual": mean_residual,
        "std_residual": std_residual,
    }
    return metrics


def print_metrics(metrics: dict):
    """Pretty-print a metrics dictionary."""
    label = metrics["label"]
    print(f"\n  [{label}]  ({metrics['n_samples']} samples)")
    print(f"  {'-' * 40}")
    print(f"    R2 Score        : {metrics['r2']:.6f}")
    print(f"    RMSE            : {metrics['rmse']:.4f} min")
    print(f"    MAE             : {metrics['mae']:.4f} min")
    print(f"    Median AE       : {metrics['median_ae']:.4f} min")
    print(f"    Max Error       : {metrics['max_error']:.4f} min")
    print(f"    Mean Residual   : {metrics['mean_residual']:.4f} min")
    print(f"    Std  Residual   : {metrics['std_residual']:.4f} min")

    # Visual R² quality indicator
    r2 = metrics["r2"]
    if r2 >= 0.95:
        quality = "[*****] Excellent"
    elif r2 >= 0.90:
        quality = "[**** ] Good"
    elif r2 >= 0.80:
        quality = "[***  ] Fair"
    elif r2 >= 0.60:
        quality = "[**   ] Poor"
    else:
        quality = "[*    ] Very Poor"
    print(f"    Quality         : {quality}")


def per_bearing_breakdown(df: pd.DataFrame, model, scaler, feature_cols: list):
    """Evaluate and print metrics for each individual bearing."""
    print_header("Per-Bearing Breakdown", char="-")

    results = []
    for bearing_name in sorted(df["bearing_name"].unique()):
        subset = df[df["bearing_name"] == bearing_name]
        X = subset[feature_cols].values
        y = subset["rul"].values
        X_scaled = scaler.transform(X)
        y_pred = model.predict(X_scaled)

        m = evaluate_predictions(y, y_pred, label=bearing_name)
        results.append(m)

    # Table header
    print(f"\n  {'Bearing':<22} {'R2':>9} {'RMSE':>10} {'MAE':>10} {'Samples':>9}")
    print(f"  {'-' * 62}")

    for m in results:
        print(
            f"  {m['label']:<22} {m['r2']:>9.4f} {m['rmse']:>10.2f} {m['mae']:>10.2f} {m['n_samples']:>9d}"
        )

    # Summary stats
    r2_values = [m["r2"] for m in results]
    print(f"\n  R2 across bearings - "
          f"min: {min(r2_values):.4f}  "
          f"max: {max(r2_values):.4f}  "
          f"mean: {np.mean(r2_values):.4f}  "
          f"std: {np.std(r2_values):.4f}")


def run_saved_metrics_check():
    """Load and display the metrics that were saved during training."""
    print_header("Saved Training Metrics (from model file)")

    try:
        _, _, metadata = load_model()
        saved_metrics = metadata.get("metrics", {})
        if saved_metrics:
            print(f"\n  Train R2  : {saved_metrics.get('train_r2', 'N/A'):.6f}")
            print(f"  Test  R2  : {saved_metrics.get('test_r2', 'N/A'):.6f}")
            print(f"  Train RMSE: {saved_metrics.get('train_rmse', 'N/A'):.4f} min")
            print(f"  Test  RMSE: {saved_metrics.get('test_rmse', 'N/A'):.4f} min")
            print(f"  Train MAE : {saved_metrics.get('train_mae', 'N/A'):.4f} min")
            print(f"  Test  MAE : {saved_metrics.get('test_mae', 'N/A'):.4f} min")
            print(f"  N Train   : {saved_metrics.get('n_train', 'N/A')}")
            print(f"  N Test    : {saved_metrics.get('n_test', 'N/A')}")
        else:
            print("  No saved metrics found in model file.")
    except FileNotFoundError as e:
        print(f"  ⚠ Could not load saved model: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Test & Evaluate Bearing RUL Prediction Model"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Path to XJTU-SY dataset root directory",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Test with synthetic demo data (no real dataset needed)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip per-bearing breakdown for faster output",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of data to use as the test set (default: 0.2)",
    )

    args = parser.parse_args()

    # ── Step 1: Display saved training metrics ──────────────────────────
    run_saved_metrics_check()

    # ── Step 2: Load the saved model ────────────────────────────────────
    print_header("Loading Saved Model")
    try:
        model, scaler, metadata = load_model()
        print("  [OK] Model loaded successfully")
        print("  [OK] Scaler loaded successfully")
    except FileNotFoundError as e:
        print(f"  [FAIL] {e}")
        print("  Run `python train_model.py --demo` first to train a model.")
        sys.exit(1)

    # ── Step 3: Prepare evaluation data ─────────────────────────────────
    print_header("Preparing Evaluation Data")

    if args.demo:
        print("  Mode: Synthetic demo data")
        df = generate_synthetic_dataset(n_bearings=8, samples_per_bearing=300)
    elif args.data_dir:
        print(f"  Mode: Real XJTU-SY data from {args.data_dir}")
        df = build_feature_matrix(args.data_dir)
    else:
        print("  Mode: Synthetic demo data (default)")
        df = generate_synthetic_dataset(n_bearings=8, samples_per_bearing=300)

    print(f"  Total samples : {len(df)}")
    print(f"  Unique bearings: {df['bearing_name'].nunique()}")
    print(f"  RUL range     : {df['rul'].min():.1f} - {df['rul'].max():.1f} min")

    feature_cols = get_training_features()

    # ── Step 4: Split and evaluate ──────────────────────────────────────
    X = df[feature_cols].values
    y = df["rul"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=42
    )

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)

    print_header("Evaluation Results")

    train_metrics = evaluate_predictions(y_train, y_pred_train, label="Train Set")
    test_metrics = evaluate_predictions(y_test, y_pred_test, label="Test Set")

    print_metrics(train_metrics)
    print_metrics(test_metrics)

    # ── Step 5: Overall (full dataset) ──────────────────────────────────
    X_all_scaled = scaler.transform(X)
    y_pred_all = model.predict(X_all_scaled)
    all_metrics = evaluate_predictions(y, y_pred_all, label="Full Dataset")
    print_metrics(all_metrics)

    # ── Step 6: Per-bearing breakdown ───────────────────────────────────
    if not args.quick:
        per_bearing_breakdown(df, model, scaler, feature_cols)

    # ── Step 7: Summary verdict ─────────────────────────────────────────
    print_header("Summary")
    r2_test = test_metrics["r2"]
    print(f"\n  Test R2 = {r2_test:.6f}")
    if r2_test >= 0.90:
        print("  [PASS] Model generalises well (R2 >= 0.90)")
    elif r2_test >= 0.70:
        print("  [WARN] Model may need tuning (0.70 <= R2 < 0.90)")
    else:
        print("  [FAIL] Model performs poorly (R2 < 0.70)")
    print()


if __name__ == "__main__":
    main()
