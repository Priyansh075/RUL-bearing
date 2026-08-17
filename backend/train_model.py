"""
Model Training Script.

Run this script to train the XGBoost model and save it for the API.

Usage:
    # Train with synthetic demo data (no dataset needed):
    python train_model.py --demo

    # Train with real XJTU-SY dataset:
    python train_model.py --data-dir /path/to/XJTU-SY-Bearing-Datasets
"""

import argparse
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from app.data_preprocessing import build_feature_matrix, generate_synthetic_dataset
from app.model import train_model, save_model


def main():
    parser = argparse.ArgumentParser(description='Train Bearing RUL Prediction Model')
    parser.add_argument(
        '--data-dir',
        type=str,
        default=None,
        help='Path to XJTU-SY dataset root directory',
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Train with synthetic demo data (no real dataset needed)',
    )
    parser.add_argument(
        '--no-tune',
        action='store_true',
        help='Skip hyperparameter tuning (faster training)',
    )
    
    args = parser.parse_args()
    
    if args.demo:
        print("=" * 60)
        print("TRAINING WITH SYNTHETIC DEMO DATA")
        print("=" * 60)
        print("\nGenerating synthetic dataset...")
        df = generate_synthetic_dataset(n_bearings=8, samples_per_bearing=300)
        print(f"Generated {len(df)} samples from {df['bearing_name'].nunique()} synthetic bearings")
    elif args.data_dir:
        print("=" * 60)
        print(f"TRAINING WITH XJTU-SY DATA FROM: {args.data_dir}")
        print("=" * 60)
        df = build_feature_matrix(args.data_dir)
    else:
        print("No data source specified. Using demo mode.")
        print("Use --data-dir /path/to/data for real training, or --demo for demo mode.\n")
        df = generate_synthetic_dataset(n_bearings=8, samples_per_bearing=300)
    
    print(f"\nDataset shape: {df.shape}")
    print(f"RUL range: {df['rul'].min():.1f} - {df['rul'].max():.1f} minutes")
    print(f"Operating conditions: {sorted(df['operating_condition'].unique())}")
    
    # Train model
    print("\nTraining XGBoost model...")
    result = train_model(
        df,
        test_size=0.2,
        tune_hyperparams=not args.no_tune,
    )
    
    # Save model
    save_model(
        result['model'],
        result['scaler'],
        result['metrics'],
        result['feature_importance'],
    )
    
    print("\n[OK] Training complete! You can now start the API server.")
    print("   Run: uvicorn app.main:app --reload --port 8000")


if __name__ == '__main__':
    main()
