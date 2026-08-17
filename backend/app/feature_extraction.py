"""
Feature Extraction Engine for XJTU-SY Bearing Vibration Data.

Extracts 28 features (14 per channel) from raw vibration signals:
- 10 time-domain features per channel
- 4 frequency-domain features per channel
"""

import numpy as np
from scipy import stats
from scipy.fft import fft, fftfreq


def extract_time_domain_features(signal: np.ndarray) -> dict:
    """
    Extract 10 time-domain statistical features from a vibration signal.
    
    Args:
        signal: 1D numpy array of vibration amplitudes
        
    Returns:
        Dictionary of feature names to values
    """
    n = len(signal)
    abs_signal = np.abs(signal)
    mean_abs = np.mean(abs_signal)
    
    # Avoid division by zero
    eps = 1e-10
    
    rms = np.sqrt(np.mean(signal ** 2))
    peak = np.max(abs_signal)
    peak_to_peak = np.max(signal) - np.min(signal)
    crest_factor = peak / (rms + eps)
    kurtosis = stats.kurtosis(signal, fisher=True)  # Excess kurtosis
    skewness = stats.skew(signal)
    std_dev = np.std(signal, ddof=1)
    shape_factor = rms / (mean_abs + eps)
    impulse_factor = peak / (mean_abs + eps)
    
    # Margin factor: Peak / (mean of sqrt of abs values)^2
    mean_sqrt_abs = np.mean(np.sqrt(abs_signal))
    margin_factor = peak / (mean_sqrt_abs ** 2 + eps)
    
    return {
        'rms': rms,
        'peak': peak,
        'peak_to_peak': peak_to_peak,
        'crest_factor': crest_factor,
        'kurtosis': kurtosis,
        'skewness': skewness,
        'std_dev': std_dev,
        'shape_factor': shape_factor,
        'impulse_factor': impulse_factor,
        'margin_factor': margin_factor,
    }


def extract_frequency_domain_features(signal: np.ndarray, fs: float = 25600.0) -> dict:
    """
    Extract 4 frequency-domain features from a vibration signal.
    
    Args:
        signal: 1D numpy array of vibration amplitudes
        fs: Sampling frequency in Hz (default: 25.6 kHz for XJTU-SY)
        
    Returns:
        Dictionary of feature names to values
    """
    n = len(signal)
    
    # Compute single-sided amplitude spectrum
    yf = fft(signal)
    xf = fftfreq(n, 1.0 / fs)
    
    # Take positive frequencies only
    positive_mask = xf > 0
    xf_pos = xf[positive_mask]
    magnitude = np.abs(yf[positive_mask])
    
    # Normalize to get power spectral density approximation
    power = magnitude ** 2
    total_power = np.sum(power)
    eps = 1e-10
    
    # Frequency center (spectral centroid) — FC
    fc = np.sum(xf_pos * power) / (total_power + eps)
    
    # Mean square frequency — MSF
    msf = np.sum((xf_pos ** 2) * power) / (total_power + eps)
    
    # Root mean square frequency — RMSF
    rmsf = np.sqrt(msf)
    
    # Frequency variance — VF
    vf = np.sum(((xf_pos - fc) ** 2) * power) / (total_power + eps)
    
    return {
        'freq_center': fc,
        'mean_sq_freq': msf,
        'rms_freq': rmsf,
        'freq_variance': vf,
    }


def extract_all_features(
    horizontal: np.ndarray,
    vertical: np.ndarray,
    fs: float = 25600.0,
) -> dict:
    """
    Extract all 28 features from a two-channel vibration sample.
    
    Args:
        horizontal: Horizontal channel vibration signal
        vertical: Vertical channel vibration signal
        fs: Sampling frequency in Hz
        
    Returns:
        Dictionary with 28 features (prefixed with 'h_' or 'v_')
    """
    features = {}
    
    # Horizontal channel
    h_time = extract_time_domain_features(horizontal)
    h_freq = extract_frequency_domain_features(horizontal, fs)
    for key, val in h_time.items():
        features[f'h_{key}'] = val
    for key, val in h_freq.items():
        features[f'h_{key}'] = val
    
    # Vertical channel
    v_time = extract_time_domain_features(vertical)
    v_freq = extract_frequency_domain_features(vertical, fs)
    for key, val in v_time.items():
        features[f'v_{key}'] = val
    for key, val in v_freq.items():
        features[f'v_{key}'] = val
    
    return features


# Ordered list of all feature names (used for consistent column ordering)
FEATURE_NAMES = [
    'h_rms', 'h_peak', 'h_peak_to_peak', 'h_crest_factor', 'h_kurtosis',
    'h_skewness', 'h_std_dev', 'h_shape_factor', 'h_impulse_factor', 'h_margin_factor',
    'h_freq_center', 'h_mean_sq_freq', 'h_rms_freq', 'h_freq_variance',
    'v_rms', 'v_peak', 'v_peak_to_peak', 'v_crest_factor', 'v_kurtosis',
    'v_skewness', 'v_std_dev', 'v_shape_factor', 'v_impulse_factor', 'v_margin_factor',
    'v_freq_center', 'v_mean_sq_freq', 'v_rms_freq', 'v_freq_variance',
]
