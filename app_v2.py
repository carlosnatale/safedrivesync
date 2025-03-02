import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit 
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Modern Dashboard Look
st.markdown("""
    <style>
        .dashboard-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .dashboard-card { width: 260px; height: 200px; padding: 20px; border-radius: 14px; background: #ffffff; text-align: center; border: 3px solid #ced4da; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); }
        .card-title { font-weight: bold; font-size: 20px; margin-bottom: 12px; }
        .card-value { font-size: 32px; font-weight: bold; }
        .risk-low { color: green; font-weight: bold; }
        .risk-moderate { color: orange; font-weight: bold; }
        .risk-high { color: red; font-weight: bold; }
        .risk-critical { color: darkred; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Simulate real-time biometric data generation
def generate_fake_data():
    levels = ['Low', 'Moderate', 'High', 'Critical']
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar (mg/dL)': np.random.randint(70, 140),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels),
        'Health Crisis Risk': np.random.choice(levels)
    }

st.title("🚗 SafeDrive Sync - Health Dashboard")
monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Real-Time Data Display - Modern Card-Based UI
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        
        # Define risk level colors
        risk_colors = {
            'Low': "risk-low",
            'Moderate': "risk-moderate",
            'High': "risk-high",
            'Critical': "risk-critical"
        }
        
        with data_placeholder:
            st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)
            for key, value in fake_data.items():
                risk_class = risk_colors.get(value, "") if key in ["Stress Level", "Fatigue Risk", "Health Crisis Risk"] else ""
                st.markdown(
                    f"""
                    <div class='dashboard-card'>
                        <div class='card-title'>{key}</div>
                        <div class='card-value {risk_class}'>{value}</div>
                    </div>
                    """, unsafe_allow_html=True
                )
            st.markdown("</div>", unsafe_allow_html=True)

        time.sleep(3)
