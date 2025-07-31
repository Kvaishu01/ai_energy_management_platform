from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

# Load the trained model
model_path = "models/energy_forecast_model.pkl"
if not os.path.exists(model_path):
    raise Exception("Model not found! Run model.py first.")
model = joblib.load(model_path)

# Day name to index mapping
day_mapping = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}

# Define the request format
class PredictionRequest(BaseModel):
    hour: int
    day: str  # Human-readable day string

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "⚡ Energy Management API is running!"}

@app.post("/predict")
def predict_energy(req: PredictionRequest):
    day_index = day_mapping.get(req.day, 0)
    features = [[req.hour, day_index]]
    prediction = model.predict(features)[0]

    # ✅ Optimization tips
    tips = []
    if prediction > 5:
        tips.append("Consider turning off unused appliances during peak hours.")
    if 18 <= req.hour <= 22:
        tips.append("Peak hours detected — try running heavy appliances earlier.")
    if day_index in [5, 6]:  # Saturday or Sunday
        tips.append("It's the weekend — review weekly energy usage for patterns.")

    return {
        "predicted_energy_kwh": round(prediction, 2),
        "tips": tips
    }

