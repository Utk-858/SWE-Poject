import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Static Dashboard", page_icon="📊", layout="wide")

# Custom CSS for Beautiful Metric Cards
st.markdown("""
<style>
.metric-card {
    padding: 20px;
    border-radius: 16px;
    background: linear-gradient(145deg, #1f2937, #111827);
    box-shadow: 4px 4px 10px #0d1117, -4px -4px 10px #243447;
    text-align: center;
    color: white;
}
.metric-title {
    font-size: 18px;
    font-weight: 600;
    color: #9CA3AF;
}
.metric-value {
    font-size: 42px;
    font-weight: 700;
    margin-top: -10px;
    color: #FBBF24;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Static IoT Dashboard")

# ThingSpeak config
CHANNEL_ID = "YOUR_CHANNEL_ID"
READ_API_KEY = "YOUR_READ_API_KEY"
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=100"

try:
    data = requests.get(URL).json()
    feeds = data["feeds"]

    df = pd.DataFrame(feeds)
    df["temperature"] = df["field1"].astype(float)
    df["humidity"] = df["field2"].astype(float)
    df["time"] = pd.to_datetime(df["created_at"])
    df = df.sort_values("time")

    latest_temp = df["temperature"].iloc[-1]
    latest_hum = df["humidity"].iloc[-1]

    # Metric cards
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">TEMPERATURE</div>
            <div class="metric-value">{latest_temp} °C</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">HUMIDITY</div>
            <div class="metric-value">{latest_hum} %</div>
        </div>
        """, unsafe_allow_html=True)

    # Gauge charts
    g1, g2 = st.columns(2)

    with g1:
        fig_t = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest_temp,
            title={'text': "Temperature (°C)"},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig_t, use_container_width=True)

    with g2:
        fig_h = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest_hum,
            title={'text': "Humidity (%)"},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig_h, use_container_width=True)

    # Temperature trend
    st.subheader("📈 Temperature Trend")
    st.plotly_chart(px.line(df, x="time", y="temperature", markers=True), use_container_width=True)

    # Humidity trend
    st.subheader("📈 Humidity Trend")
    st.plotly_chart(px.line(df, x="time", y="humidity", markers=True), use_container_width=True)

    # Raw data
    st.subheader("📁 Raw Sensor Data")
    st.dataframe(df[["time", "temperature", "humidity"]])

except Exception as e:
    st.error(f"Failed to load data: {e}")
