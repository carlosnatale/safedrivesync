import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements - Futuristic Car Dashboard
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Modern Dashboard Look
st.markdown("""
    <style>
        body { background-color: #000; color: #eaeaea; }
        .main { background: #0f0f0f; color: white; padding: 20px; }
        .dashboard-container {
            border-radius: 20px;
            padding: 30px;
            background: linear-gradient(135deg, #001f3f, #005f73);
            box-shadow: 0px 4px 15px rgba(0, 255, 255, 0.5);
            text-align: center;
            color: white;
        }
        .speedometer {
            font-size: 60px;
            font-weight: bold;
            color: #00ffff;
        }
        .battery {
            font-size: 40px;
            font-weight: bold;
            color: #00ff00;
        }
        .info-box {
            font-size: 22px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 SafeDrive Sync - Futuristic Car Dashboard")

monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)

# Main Dashboard UI
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    st.markdown("<div class='info-box'><span class='battery'>🔋 97%</span><br>Battery Charge</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='info-box'><span class='speedometer'>🚗 68 MPH</span><br>Current Speed</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='info-box'>📏 188 km<br>Distance</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Real-Time Data
st.subheader("📊 Driver Health Metrics")
data_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = {
            'Heart Rate (bpm)': np.random.randint(60, 110),
            'HRV (ms)': np.random.randint(20, 80),
            'SpO2 (%)': np.random.randint(90, 100),
            'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
            'Blood Sugar (mg/dL)': np.random.randint(70, 140),
            'Motion Intensity': np.random.randint(0, 10),
        }
        df = pd.DataFrame([fake_data])
        data_placeholder.dataframe(df, use_container_width=True)
        time.sleep(3)
