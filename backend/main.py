import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow.keras.models import load_model
from datetime import datetime

MODEL_PATH = 'models/nyc_lstm_model.h5'
SCALER_PATH = 'models/nyc_scaler.gz'
ENCODER_PATH = 'models/nyc_label_encoder.gz'

app = FastAPI(title='Will It Rain On My Parade - NYC')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model + artifacts at startup
try:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(project_root, "models", "nyc_lstm_model.h5")
    scaler_path = os.path.join(project_root, "models", "nyc_scaler.gz")
    encoder_path = os.path.join(project_root, "models", "nyc_label_encoder.gz")
    
    model = load_model(model_path)
    artifacts = joblib.load(scaler_path)
    le = joblib.load(encoder_path)
    scaler, time_scaler = artifacts['scaler'], artifacts['time_scaler']
    seq_features, time_features = artifacts['seq_features'], artifacts['time_features']
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class ForecastRequest(BaseModel):
    city: str
    datetime: str

@app.get('/api/v1/health')
def health():
    return {'status': 'ok'}

@app.post('/api/v1/forecast')
def forecast(req: ForecastRequest):
    if req.city.lower() not in ['new york', 'nyc', 'new york city']:
        raise HTTPException(status_code=400, detail='Forecasting available for NYC only (Team T-Minus Rain).')
    try:
        target_time = pd.to_datetime(req.datetime)
    except Exception:
        raise HTTPException(status_code=400, detail='Invalid datetime format.')

    if model is None:
        raise HTTPException(status_code=500, detail='Model not loaded')

    X_seq = np.zeros((1, 30, len(seq_features)))
    X_time = np.zeros((1, len(time_features)))
    X_time = time_scaler.transform(X_time)

    X = np.concatenate([X_seq.reshape(1, -1), X_time], axis=1)
    X = scaler.transform(X)
    X = X.reshape(1, 30, len(seq_features) + len(time_features))

    yhat = model.predict(X)[0]
    probs = {le.inverse_transform([i])[0]: float(round(p * 100, 2)) for i, p in enumerate(yhat)}
    pred = le.inverse_transform([np.argmax(yhat)])[0]

    return {
        'time': str(target_time),
        'prediction': pred,
        'probabilities': probs
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)