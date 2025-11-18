import streamlit as st

st.set_page_config(page_title="Predictive Maintenance", page_icon="🛠", layout="wide")

st.title("🛠 Predictive Maintenance System")

st.write("""
Welcome to the **IoT + Machine Learning Predictive Maintenance Dashboard**.

Use the sidebar to navigate:

- 📡 **Live IoT Dashboard** – auto-refreshes, pulls data from ThingSpeak, makes ML prediction  
- 📊 **Static Dashboard** – graphs, analytics, historical data  
- ℹ️ **About** – info about the project  
""")
