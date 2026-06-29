import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'isolation_forest_model.pkl')

def predict_anomalies(data_df):
    """
    Uses the trained Isolation Forest model to predict anomalies.
    Returns the DataFrame with 'anomaly' column added. (-1 for anomaly, 1 for normal)
    """
    if not os.path.exists(MODEL_PATH):
        # Fallback if model not trained
        data_df['anomaly'] = 1
        return data_df

    model = joblib.load(MODEL_PATH)
    predictions = model.predict(data_df)
    data_df['anomaly'] = predictions
    return data_df
