import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit 
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Mobile-Friendly Display
st.markdown("""
    <style>
        .dashboard-box { 
            padding: 10px; 
            border-radius: 10px; 
            background: #ffffff; 
            margin-bottom: 10px; 
            border: 2px solid #ced4da; 
            text-align: center; 
            font-size: 18px; 
        }
        .metric-title { font-weight: bold; font-size: 20px; color: #004085; }
        .metric-value { font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Simulate real-time biometric data generation
def generate_fake_data():
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar (mg/dL)': np.random.randint(70, 140),
        'Motion Intensity': np.random.randint(0, 10),
    }

st.title("🚗 SafeDrive Sync - Health Dashboard")
monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Real-Time Data Display - Mobile Optimized
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()

        with data_placeholder.container():
            st.subheader("🚦 Driver Health Metrics")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class='dashboard-box'>
                        <div class='metric-title'>💓 Heart Rate</div>
                        <div class='metric-value'>{fake_data['Heart Rate (bpm)']} bpm</div>
                    </div>
                    <div class='dashboard-box'>
                        <div class='metric-title'>🫀 HRV</div>
                        <div class='metric-value'>{fake_data['HRV (ms)']} ms</div>
                    </div>
                    <div class='dashboard-box'>
                        <div class='metric-title'>🔵 SpO2</div>
                        <div class='metric-value'>{fake_data['SpO2 (%)']}%</div>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class='dashboard-box'>
                        <div class='metric-title'>💉 Blood Pressure</div>
                        <div class='metric-value'>{fake_data['Blood Pressure (mmHg)']}</div>
                    </div>
                    <div class='dashboard-box'>
                        <div class='metric-title'>🩸 Blood Sugar</div>
                        <div class='metric-value'>{fake_data['Blood Sugar (mg/dL)']} mg/dL</div>
                    </div>
                    <div class='dashboard-box'>
                        <div class='metric-title'>⚡ Motion Intensity</div>
                        <div class='metric-value'>{fake_data['Motion Intensity']}</div>
                    </div>
                """, unsafe_allow_html=True)
        
        time.sleep(3)
