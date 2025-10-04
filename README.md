# Will It Rain On My Parade — NYC 🌦️

**Team:** T-Minus Rain  
**Challenge:** NASA Space Apps 2025 — Will It Rain On My Parade?  

## Overview
A personalized web app answering if it will rain at a chosen date & time in **New York City only**. Powered by an LSTM model trained on NASA open data.

## Features
- Input any future date+time (hours to years ahead).
- Returns forecast label + class probabilities.
- Context panel shows typical seasonal conditions.
- Mobile-friendly React UI with clear icons.

## Run locally
```bash
git clone <repo>
cd project
# Backend
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
# Frontend
cd frontend
npm install && npm run dev
```

## Model Files
Place the following into `/models/`:
- nyc_lstm_model.h5
- nyc_scaler.gz
- nyc_label_encoder.gz

## Limitations
- Forecasting available only for **NYC**.
- Long-range forecasts have uncertainty. Probabilities are model outputs, not guarantees.

## NASA Challenge Mapping
- Personalized dashboard ✅
- Uses NASA open data ✅
- Clear UI/UX ✅
- Accessible results with context ✅
