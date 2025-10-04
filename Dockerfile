FROM python:3.10-slim
WORKDIR /app
COPY backend/ ./backend/
COPY models/ ./models/
RUN pip install fastapi uvicorn tensorflow joblib scikit-learn pandas numpy
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

