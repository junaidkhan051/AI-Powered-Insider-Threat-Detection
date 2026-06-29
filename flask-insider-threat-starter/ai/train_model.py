import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os

def train():
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, 'sample_dataset.csv')
    model_path = os.path.join(current_dir, 'isolation_forest_model.pkl')

    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        return

    df = pd.read_csv(data_path)
    
    # We use files_accessed, usb_used, failed_logins for features
    features = ['files_accessed', 'usb_used', 'failed_logins']
    X = df[features]

    # Contamination defines the proportion of outliers in the data set
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X)

    joblib.dump(model, model_path)
    print("Model trained and saved to", model_path)

if __name__ == '__main__':
    train()
