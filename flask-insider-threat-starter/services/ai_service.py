import pandas as pd
from ai.ai_engine import predict_anomalies

def evaluate_user_activity(activity_data):
    """
    Evaluates user activity to determine if it is an anomaly.
    Expects a dictionary with: 'files_accessed', 'usb_used', 'failed_logins'
    """
    # Create DataFrame with same structure as training data
    df = pd.DataFrame([activity_data])
    
    # Get predictions
    results = predict_anomalies(df)
    
    # Return True if anomaly (-1), False if normal (1)
    if not results.empty:
        return results.iloc[0]['anomaly'] == -1
    return False
