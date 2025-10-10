import numpy as np
import pandas as pd
import pickle
import streamlit as st

# Load model
with open('predictive_maintenance.pkl', 'rb') as f:
    model = pickle.load(f)

# Load scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# List of features
FEATURES = [
    'Type',
    'Air temperature [K]',
    'Process temperature [K]',
    'Rotational speed [rpm]',
    'Torque [Nm]',
    'Tool wear [min]'
]

# Encode product type
def encode_type(type_val):
    mapping = {'L': 0, 'M': 1, 'H': 2}
    return mapping.get(type_val, 0)

# --- Streamlit UI ---
st.set_page_config(page_title="Predictive Maintenance", page_icon="🛠", layout="centered")

st.title("🛠 Predictive Maintenance Failure Type Prediction")

# Input form
with st.form("prediction_form"):
    type_val = st.selectbox("Product Type", ["L", "M", "H"])
    air_temp = st.number_input("Air temperature [K]", min_value=200.0, max_value=400.0, step=0.1)
    process_temp = st.number_input("Process temperature [K]", min_value=200.0, max_value=400.0, step=0.1)
    speed = st.number_input("Rotational speed [rpm]", min_value=500.0, max_value=3000.0, step=1.0)
    torque = st.number_input("Torque [Nm]", min_value=0.0, max_value=100.0, step=0.1)
    wear = st.number_input("Tool wear [min]", min_value=0.0, max_value=300.0, step=1.0)

    submitted = st.form_submit_button("🔮 Predict Failure Type")

if submitted:
    try:
        # Prepare input
        features = [
            encode_type(type_val),
            air_temp,
            process_temp,
            speed,
            torque,
            wear
        ]
        input_df = pd.DataFrame([features], columns=FEATURES)

        # Split type vs numeric
        type_col = input_df[['Type']]
        numeric_cols = input_df.drop(columns=['Type'])

        # Scale only numeric features
        numeric_scaled = scaler.transform(numeric_cols)

        # Combine type with scaled numeric features
        final_input = np.concatenate([type_col.values, numeric_scaled], axis=1)

        # Prediction
        prediction = model.predict(input_df)[0]

        st.success(f"✅ Predicted Failure Type: **{prediction}**")

    except Exception as e:
        st.error(f"❌ Error: {e}")
