import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import os

# Function to load and preprocess the data
def load_data(file_path="data/energy_data.csv"):
    df = pd.read_csv(file_path, parse_dates=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day
    df['total_energy'] = df.groupby('timestamp')['energy_kwh'].transform('sum')
    df = df.drop_duplicates('timestamp')
    return df

# Function to train a linear regression model
def train_forecasting_model(df):
    X = df[['hour', 'day']]
    y = df['total_energy']
    model = LinearRegression()
    model.fit(X, y)
    return model

# Function to save the model
def save_model(model, path="models/energy_forecast_model.pkl"):
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, path)

# Function to load the model (optional for reuse)
def load_model(path="models/energy_forecast_model.pkl"):
    return joblib.load(path)

# When run directly, train and save the model
if __name__ == "__main__":
    data = load_data()
    model = train_forecasting_model(data)
    save_model(model)
    print("✅ Model trained and saved.")

def optimize_energy(hour, day, predicted_usage):
    recommendations = []
    if predicted_usage > 5:
        recommendations.append("⚠️ High predicted usage. Consider reducing load or shifting appliances.")
    if 18 <= hour <= 22:
        recommendations.append("🔌 Peak hours detected. Try using heavy appliances during daytime.")
    if day in ['Saturday', 'Sunday']:
        recommendations.append("📆 Weekend usage. Check if idle appliances are still drawing power.")
    if not recommendations:
        recommendations.append("✅ Usage pattern is optimal.")
    return recommendations
def generate_tips(hour, day_index, prediction):
    tips = []
    if prediction > 5:
        tips.append("Consider turning off unused appliances during peak hours.")
    if 18 <= hour <= 22:
        tips.append("Peak hours detected — try running heavy appliances earlier.")
    if day_index in [5, 6]:
        tips.append("It's the weekend — review weekly energy usage for patterns.")
    return tips
