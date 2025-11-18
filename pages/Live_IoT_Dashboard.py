import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests

# Auto-refresh every 2 minutes
st.markdown(
    "<meta http-equiv='refresh' content='120'>",
    unsafe_allow_html=True
)

st.title("📡 Live IoT-Based Predictive Maintenance Dashboard")

# --------------------------
# Load ML model + Scaler
# --------------------------
try:
    with open("predictive_maintenance.pkl", "rb") as f:
        model = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
except:
    st.error("❌ Could not load model or scaler. Check file paths.")
    st.stop()

# --------------------------
# ThingSpeak Setup
# --------------------------
CHANNEL_ID = "YOUR_CHANNEL_ID"
READ_API_KEY = "YOUR_READ_API_KEY"

URL = f"https://api.thingspeak.com/channels/3170362/feeds.json?api_key=E2DI968IF3X66INN&results=1"

# --------------------------
# Fetch IoT Data
# --------------------------
try:
    response = requests.get(URL).json()
    if "feeds" not in response or len(response["feeds"]) == 0:
        st.error("❌ No feed data available from ThingSpeak.")
        st.stop()

    feed = response["feeds"][0]

    temperature = float(feed["field1"])   # °C
    humidity = float(feed["field2"])      # %

    # Display live values
    st.subheader("🌡️ Latest Sensor Readings")
    c1, c2 = st.columns(2)
    c1.metric("Temperature", f"{temperature} °C")
    c2.metric("Humidity", f"{humidity} %")

except Exception as e:
    st.error(f"❌ Error fetching IoT data: {e}")
    st.stop()

# --------------------------
# Convert to ML model features
# --------------------------
try:
    # Model requires 6 features
    air_temp = temperature + 273.15
    process_temp = humidity + 273.15   # Placeholder
    speed = 1500
    torque = 40
    wear = 20
    type_val = "M"

    # encode type
    def encode_type(val):
        return {"L": 0, "M": 1, "H": 2}.get(val, 1)

    type_encoded = encode_type(type_val)

    # DataFrame for scaler
    numeric_df = pd.DataFrame([{
        "Air temperature [K]": air_temp,
        "Process temperature [K]": process_temp,
        "Rotational speed [rpm]": speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": wear
    }])

    # Scale numeric inputs
    scaled_numeric = scaler.transform(numeric_df)

    # Combine final input
    final_input = np.hstack(([type_encoded], scaled_numeric[0]))

    columns = [
        "Type",
        "Air temperature [K]",
        "Process temperature [K]",
        "Rotational speed [rpm]",
        "Torque [Nm]",
        "Tool wear [min]"
    ]

    input_df = pd.DataFrame([final_input], columns=columns)

    # Debug:
    st.write("🔍 DEBUG: Model Input DataFrame")
    st.dataframe(input_df)

except Exception as e:
    st.error(f"❌ Error preparing ML input: {e}")
    st.stop()

# --------------------------
# ML Prediction
# --------------------------
try:
    prediction = model.predict(input_df)[0]

    st.subheader("🔮 ML Failure Prediction")
    st.success(f"Predicted Failure Type: **{prediction}**")

except Exception as e:
    st.error(f"❌ Prediction Error: {e}")
