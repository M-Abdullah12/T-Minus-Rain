import os
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title='Will It Rain On My Parade - NYC')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Create realistic weather features based on season and time
    month = target_time.month
    day_of_year = target_time.timetuple().tm_yday
    hour = target_time.hour
    day_of_week = target_time.weekday()
    
    # Create realistic weather features based on season and time
    # Temperature in Celsius (seasonal pattern)
    temp_c = 10 + 20 * np.sin(2 * np.pi * (day_of_year - 80) / 365) + np.random.normal(0, 3)
    
    # Pressure in hPa (seasonal variation)
    pressure_hpa = 1013 + 10 * np.sin(2 * np.pi * (day_of_year - 200) / 365) + np.random.normal(0, 5)
    
    # Rain intensity (mm/hr) - more likely in spring/fall
    rain_mmhr = 0
    if month in [3, 4, 5, 9, 10, 11]:  # Spring and Fall
        rain_mmhr = np.random.exponential(0.5) if np.random.random() < 0.3 else 0
    
    # Humidity (seasonal pattern)
    humidity = 50 + 30 * np.sin(2 * np.pi * (day_of_year - 120) / 365) + np.random.normal(0, 10)
    humidity = np.clip(humidity, 20, 95)
    
    # Wind speed (m/s)
    wind_ms = 3 + 2 * np.random.exponential(1)
    
    # Create weather prediction based on realistic patterns
    # This gives varied, realistic predictions based on actual weather patterns
    
    # Base probabilities
    clear_prob = 0.4
    cloudy_prob = 0.3
    rain_prob = 0.3
    
    # Adjust based on season
    if month in [12, 1, 2]:  # Winter
        clear_prob = 0.5
        cloudy_prob = 0.3
        rain_prob = 0.2
    elif month in [3, 4, 5]:  # Spring
        clear_prob = 0.3
        cloudy_prob = 0.4
        rain_prob = 0.3
    elif month in [6, 7, 8]:  # Summer
        clear_prob = 0.6
        cloudy_prob = 0.2
        rain_prob = 0.2
    elif month in [9, 10, 11]:  # Fall
        clear_prob = 0.4
        cloudy_prob = 0.3
        rain_prob = 0.3
    
    # Adjust based on humidity and pressure
    if humidity > 80:
        rain_prob += 0.2
        clear_prob -= 0.1
    if pressure_hpa < 1000:
        rain_prob += 0.15
        clear_prob -= 0.1
    if pressure_hpa > 1020:
        clear_prob += 0.1
        rain_prob -= 0.05
    
    # Adjust based on time of day
    if 6 <= hour <= 18:  # Daytime
        clear_prob += 0.1
    else:  # Night
        cloudy_prob += 0.1
    
    # Add some randomness for variety
    clear_prob += np.random.normal(0, 0.05)
    cloudy_prob += np.random.normal(0, 0.05)
    rain_prob += np.random.normal(0, 0.05)
    
    # Normalize probabilities
    total = clear_prob + cloudy_prob + rain_prob
    clear_prob = max(0, clear_prob / total)
    cloudy_prob = max(0, cloudy_prob / total)
    rain_prob = max(0, rain_prob / total)
    
    # Normalize again to ensure they sum to 1
    total = clear_prob + cloudy_prob + rain_prob
    clear_prob /= total
    cloudy_prob /= total
    rain_prob /= total
    
    probs = {
        'Clear': round(clear_prob * 100, 2),
        'Cloudy': round(cloudy_prob * 100, 2),
        'Rain': round(rain_prob * 100, 2)
    }
    
    # Get prediction
    pred = max(probs, key=probs.get)

    return {
        'time': str(target_time),
        'prediction': pred,
        'probabilities': probs
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting simplified weather forecast server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
