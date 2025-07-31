import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Energy Management Dashboard", layout="wide")

st.title("⚡ AI-Powered Energy Usage Dashboard")

# Load and preview data
st.subheader("1️⃣ Sample Energy Data")
df = pd.read_csv("data/energy_data.csv", parse_dates=['timestamp'])
st.dataframe(df.head())

# Show energy usage over time
st.subheader("2️⃣ Energy Usage Over Time")
df.set_index("timestamp", inplace=True)
energy_per_hour = df.resample("H").sum()
st.line_chart(energy_per_hour["energy_kwh"])

# Get prediction from FastAPI
st.subheader("3️⃣ Forecast Energy Usage")
hour = st.slider("Select Hour of the Day (0-23):", 0, 23, 10)
day = st.slider("Select Day of the Month (1-31):", 1, 31, 15)

if st.button("Predict Energy Usage"):
    payload = {"hour": hour, "day": day}
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            predicted = response.json()["predicted_energy_kwh"]
            st.success(f"🔮 Predicted Energy Usage: {predicted} kWh")
            if "tips" in result:
                st.markdown("### 💡 Energy Optimization Tips:")
                for tip in result["tips"]:
                    st.info(tip)

        else:
            st.error("❌ Failed to get prediction from the backend.")
    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI backend is not running. Start it using:")
        st.code("uvicorn backend.main:app --reload", language="bash")