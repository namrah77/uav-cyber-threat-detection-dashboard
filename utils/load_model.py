import joblib
import pandas as pd
import os

def load_isolation_forest():
    """Load the Isolation Forest model for anomaly detection."""
    return joblib.load(os.path.join("models", "isolation_forest.pkl"))

def load_classifier():
    """Load the trained classifier for spoofing vs jamming detection."""
    return joblib.load(os.path.join("models", "random_forest_model.pkl"))

def load_data():
    """Load the UAV GPS dataset."""
    return pd.read_csv(os.path.join("datasets", "data_sorted.csv"))

def load_unscaled():
    """Load the UAV GPS dataset."""
    return pd.read_csv(os.path.join("datasets", "merged_data_unscaled.csv"))

def load_training_data():
    """Load the training data for the classifier."""
    return pd.read_csv(os.path.join("datasets", "Training Data.csv"))

def load_scaler_function():
    return joblib.load(os.path.join("models", "preprocessor.pkl"))