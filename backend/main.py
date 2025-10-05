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

    # Load trained LSTM and preprocessing artifacts
    model = load_model(model_path)
    artifacts = joblib.load(scaler_path)
    le = joblib.load(encoder_path)
    scaler, time_scaler = artifacts['scaler'], artifacts['time_scaler']
    seq_features, time_features = artifacts['seq_features'], artifacts['time_features']
    print("✅ LSTM model and artifacts loaded")
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

    # Build inputs to match training pipeline
    month = target_time.month
    day_of_year = target_time.timetuple().tm_yday
    hour = target_time.hour
    day_of_week = target_time.weekday()

    # Generate a synthetic recent 720-timestep window around the target time
    # Create raw sequence features in the exact order of seq_features
    total_steps = 720
    seq_raw = []  # list of length 720, each is list of 9 features
    for i in range(total_steps):
        # simulate a short history leading to the target (older -> newer)
        offset_hours = (i - (total_steps - 1))  # negative values up to 0
        hour_i = (hour + offset_hours) % 24
        day_i = ((day_of_year - (1 if hour + offset_hours < 0 else 0)) - ((total_steps - 1) - i))
        if day_i <= 0:
            day_i = (day_i % 365) or 365

        hour_sin = np.sin(2 * np.pi * hour_i / 24)
        hour_cos = np.cos(2 * np.pi * hour_i / 24)
        doy_sin = np.sin(2 * np.pi * day_i / 365)
        doy_cos = np.cos(2 * np.pi * day_i / 365)

        # seasonal/realistic signals for weather variables
        temp_c = 10 + 20 * np.sin(2 * np.pi * (day_i - 80) / 365) + np.random.normal(0, 0.8)
        pressure_hpa = 1013 + 10 * np.sin(2 * np.pi * (day_i - 200) / 365) + np.random.normal(0, 2)
        rain_mmhr = np.random.exponential(0.3) if (month in [3,4,5,9,10,11] and np.random.rand() < 0.15) else 0.0
        humidity = np.clip(50 + 30 * np.sin(2 * np.pi * (day_i - 120) / 365) + np.random.normal(0, 5), 20, 95)
        wind_ms = max(0.0, 3 + np.random.normal(0, 1))

        # order must match seq_features from artifacts
        feature_map = {
            'temp_c': temp_c,
            'pressure_hpa': pressure_hpa,
            'rain_mmhr': rain_mmhr,
            'humidity': humidity,
            'wind_ms': wind_ms,
            'hour_sin': hour_sin,
            'hour_cos': hour_cos,
            'doy_sin': doy_sin,
            'doy_cos': doy_cos,
        }
        seq_raw.append([feature_map[name] for name in seq_features])

    seq_raw = np.array(seq_raw)  # (720, 9)

    # Scale sequence features per timestep using the 9-feature scaler
    seq_scaled = scaler.transform(seq_raw)  # (720, 9)

    # Time/context features for the target time in the exact order of time_features
    hour_sin_t = np.sin(2 * np.pi * hour / 24)
    hour_cos_t = np.cos(2 * np.pi * hour / 24)
    doy_sin_t = np.sin(2 * np.pi * day_of_year / 365)
    doy_cos_t = np.cos(2 * np.pi * day_of_year / 365)

    time_feature_map = {
        'hour_sin': hour_sin_t,
        'hour_cos': hour_cos_t,
        'doy_sin': doy_sin_t,
        'doy_cos': doy_cos_t,
        'month': month,
        'dayofweek': day_of_week,
    }
    time_raw = np.array([[time_feature_map[name] for name in time_features]])  # (1,6)
    time_scaled = time_scaler.transform(time_raw)[0]  # (6,)

    # Prepare inputs the model expects: [sequence_input, time_input]
    seq_input = seq_scaled.reshape(1, seq_scaled.shape[0], seq_scaled.shape[1]).astype(np.float32)  # (1,720,9)
    time_input = time_scaled.reshape(1, -1).astype(np.float32)  # (1,6)

    yhat = model.predict([seq_input, time_input])[0]
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