"""
Data Preprocessing Pipeline for XJTU-SY Bearing Dataset.

Handles:
- Loading raw CSV files from the XJTU-SY folder structure
- Extracting features from each vibration sample
- Generating piecewise-linear RUL labels
- Building the complete feature matrix for model training
"""

import os
import numpy as np
import pandas as pd
from typing import Tuple, Optional

from app.feature_extraction import extract_all_features, FEATURE_NAMES


# XJTU-SY operating conditions
OPERATING_CONDITIONS = {
    'Bearing1_1': 1, 'Bearing1_2': 1, 'Bearing1_3': 1, 'Bearing1_4': 1, 'Bearing1_5': 1,
    'Bearing2_1': 2, 'Bearing2_2': 2, 'Bearing2_3': 2, 'Bearing2_4': 2, 'Bearing2_5': 2,
    'Bearing3_1': 3, 'Bearing3_2': 3, 'Bearing3_3': 3, 'Bearing3_4': 3, 'Bearing3_5': 3,
}

# Operating condition parameters
CONDITION_PARAMS = {
    1: {'speed_rpm': 2100, 'load_kn': 12.0},
    2: {'speed_rpm': 2250, 'load_kn': 11.0},
    3: {'speed_rpm': 2400, 'load_kn': 10.0},
}


def load_single_csv(filepath: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Load a single XJTU-SY CSV file.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        Tuple of (horizontal_signal, vertical_signal)
    """
    df = pd.read_csv(filepath, header=None)
    horizontal = df.iloc[:, 0].values.astype(np.float64)
    vertical = df.iloc[:, 1].values.astype(np.float64)
    return horizontal, vertical


def load_bearing_data(bearing_dir: str) -> list:
    """
    Load all samples for a single bearing.
    
    Args:
        bearing_dir: Path to the bearing directory containing CSV files
        
    Returns:
        List of (horizontal, vertical) signal tuples, sorted chronologically
    """
    csv_files = sorted([
        f for f in os.listdir(bearing_dir) if f.endswith('.csv')
    ])
    
    samples = []
    for csv_file in csv_files:
        filepath = os.path.join(bearing_dir, csv_file)
        try:
            h, v = load_single_csv(filepath)
            samples.append((h, v))
        except Exception as e:
            print(f"Warning: Could not load {filepath}: {e}")
    
    return samples


def generate_rul_labels(num_samples: int, rul_cap: float = 125.0) -> np.ndarray:
    """
    Generate piecewise-linear RUL labels for a bearing's lifecycle.
    
    The RUL decreases linearly from the cap value to 0 at failure.
    Samples far from failure are capped at `rul_cap`.
    
    Args:
        num_samples: Total number of samples in the bearing's life
        rul_cap: Maximum RUL value (minutes). Samples with true RUL > cap
                 are assigned this value.
        
    Returns:
        Array of RUL values (in minutes, since samples are 1 minute apart)
    """
    # True RUL decreases from (num_samples - 1) down to 0
    true_rul = np.arange(num_samples - 1, -1, -1, dtype=np.float64)
    
    # Cap at rul_cap
    rul = np.minimum(true_rul, rul_cap)
    
    return rul


def extract_bearing_features(bearing_dir: str, bearing_name: str) -> pd.DataFrame:
    """
    Extract features from all samples of a single bearing.
    
    Args:
        bearing_dir: Path to the bearing directory
        bearing_name: Name of the bearing (e.g., 'Bearing1_1')
        
    Returns:
        DataFrame with features, RUL labels, and metadata
    """
    samples = load_bearing_data(bearing_dir)
    num_samples = len(samples)
    
    if num_samples == 0:
        return pd.DataFrame()
    
    # Extract features for each sample
    all_features = []
    for h, v in samples:
        feat = extract_all_features(h, v)
        all_features.append(feat)
    
    df = pd.DataFrame(all_features)
    
    # Generate RUL labels
    df['rul'] = generate_rul_labels(num_samples)
    
    # Add metadata
    condition = OPERATING_CONDITIONS.get(bearing_name, 0)
    df['bearing_name'] = bearing_name
    df['operating_condition'] = condition
    df['normalized_time'] = np.linspace(0, 1, num_samples)
    
    return df


def build_feature_matrix(data_dir: str) -> pd.DataFrame:
    """
    Build the complete feature matrix from the XJTU-SY dataset.
    
    Expected directory structure:
        data_dir/
        ├── Bearing1_1/
        │   ├── 1.csv
        │   ├── 2.csv
        │   └── ...
        ├── Bearing1_2/
        └── ...
    
    OR:
        data_dir/
        ├── 35Hz12kN/  (or similar condition folder names)
        │   ├── Bearing1_1/
        │   └── ...
        └── ...
    
    Args:
        data_dir: Root directory of the XJTU-SY dataset
        
    Returns:
        Complete feature DataFrame ready for model training
    """
    all_dfs = []
    
    # Try flat structure first (all Bearing folders in data_dir)
    for item in os.listdir(data_dir):
        item_path = os.path.join(data_dir, item)
        
        if os.path.isdir(item_path):
            if item.startswith('Bearing'):
                # Direct bearing directory
                print(f"Processing {item}...")
                df = extract_bearing_features(item_path, item)
                if not df.empty:
                    all_dfs.append(df)
            else:
                # Might be a condition folder, check for bearing subdirs
                for sub_item in os.listdir(item_path):
                    sub_path = os.path.join(item_path, sub_item)
                    if os.path.isdir(sub_path) and sub_item.startswith('Bearing'):
                        print(f"Processing {sub_item}...")
                        df = extract_bearing_features(sub_path, sub_item)
                        if not df.empty:
                            all_dfs.append(df)
    
    if not all_dfs:
        raise ValueError(f"No bearing data found in {data_dir}")
    
    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"\nTotal samples: {len(combined)}")
    print(f"Bearings found: {combined['bearing_name'].nunique()}")
    
    return combined


def generate_synthetic_dataset(n_bearings: int = 6, samples_per_bearing: int = 200) -> pd.DataFrame:
    """
    Generate a synthetic dataset that mimics XJTU-SY feature distributions.
    Used for demo mode when the real dataset is not available.
    
    The synthetic data simulates bearing degradation patterns:
    - Features start at healthy baseline values
    - Gradually increase (RMS, peak, kurtosis) as bearing degrades
    - RUL decreases linearly with cap
    
    Args:
        n_bearings: Number of synthetic bearings to generate
        samples_per_bearing: Samples per bearing lifecycle
        
    Returns:
        Synthetic feature DataFrame
    """
    np.random.seed(42)
    all_dfs = []
    
    for i in range(n_bearings):
        condition = (i % 3) + 1
        bearing_name = f"Synthetic_{condition}_{i + 1}"
        
        t = np.linspace(0, 1, samples_per_bearing)
        
        # Simulate degradation: features increase exponentially near failure
        degradation = 1 + 2 * np.exp(3 * (t - 0.8))
        noise_scale = 0.1
        
        features = {}
        for prefix in ['h', 'v']:
            base_noise = np.random.randn(samples_per_bearing) * noise_scale
            
            # Time-domain features that increase with degradation
            features[f'{prefix}_rms'] = 0.05 * degradation + base_noise * 0.01
            features[f'{prefix}_peak'] = 0.15 * degradation + np.abs(base_noise) * 0.02
            features[f'{prefix}_peak_to_peak'] = 0.30 * degradation + np.abs(base_noise) * 0.03
            features[f'{prefix}_crest_factor'] = 3.0 + 0.5 * t + base_noise * 0.1
            features[f'{prefix}_kurtosis'] = 3.0 + 5.0 * (t ** 3) + base_noise * 0.5
            features[f'{prefix}_skewness'] = 0.0 + 0.5 * t + base_noise * 0.1
            features[f'{prefix}_std_dev'] = 0.05 * degradation + base_noise * 0.005
            features[f'{prefix}_shape_factor'] = 1.25 + 0.1 * t + base_noise * 0.02
            features[f'{prefix}_impulse_factor'] = 4.0 + 1.0 * degradation + base_noise * 0.2
            features[f'{prefix}_margin_factor'] = 5.0 + 2.0 * degradation + base_noise * 0.3
            
            # Frequency-domain features
            features[f'{prefix}_freq_center'] = 3000 + 500 * t + base_noise * 100
            features[f'{prefix}_mean_sq_freq'] = 1.5e7 + 5e6 * t + base_noise * 1e6
            features[f'{prefix}_rms_freq'] = 3800 + 600 * t + base_noise * 150
            features[f'{prefix}_freq_variance'] = 5e6 + 3e6 * t + base_noise * 5e5
        
        df = pd.DataFrame(features)
        df['rul'] = generate_rul_labels(samples_per_bearing)
        df['bearing_name'] = bearing_name
        df['operating_condition'] = condition
        df['normalized_time'] = t
        
        all_dfs.append(df)
    
    combined = pd.concat(all_dfs, ignore_index=True)
    return combined
