import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements - Improved Dashboard Look
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Improved Readability and Contrast
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; color: black; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; }
        .stDataFrame { background-color: white; color: black; border-radius: 10px; padding: 10px; }
        .stSidebar { background: #e9ecef; }
        .dashboard-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 10px; }
        .dashboard-box { padding: 15px; border-radius: 10px; background: #ffffff; border: 2px solid #ced4da; text-align: left; }
        .action-box { background: #eef6fc; border: 3px solid #007bff; font-size: 18px; }
        .notification-box { background: #fde2e4; border: 3px solid #dc3545; font-size: 18px; }
        .alert-title { font-weight: bold; font-size: 22px; margin-bottom: 15px; text-align: center; }
        .alert-content { font-size: 20px; padding: 10px 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 SafeDrive Sync - Enhanced Dashboard UI")

monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Vehicle Response Settings
st.subheader("🚘 Configure Vehicle Actions")
levels = ['Low', 'Moderate', 'High', 'Critical']
actions = [
    "No Action", "Send Notification", "Reduce Speed", "Play Calming Music", "Turn On Air Conditioning", 
    "Adjust Seat Position", "Activate Horn", "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

def action_dropdown(label, actions):
    return st.selectbox(f"{label}", actions)

with st.expander("🧘 Stress Actions"):
    stress_actions = {level: action_dropdown(f"Stress {level}", actions) for level in levels}

with st.expander("😴 Fatigue Actions"):
    fatigue_actions = {level: action_dropdown(f"Fatigue {level}", actions) for level in levels}

with st.expander("🚑 Health Crisis Actions"):
    health_crisis_actions = {level: action_dropdown(f"Health Crisis {level}", actions) for level in levels}

# Real-Time Data Display with Enhanced Table Formatting
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()

data_columns = ["Heart Rate (bpm)", "HRV (ms)", "SpO2 (%)", "Blood Pressure (mmHg)", "Blood Sugar (mg/dL)", "Motion Intensity", "Stress Level", "Fatigue Risk", "Health Crisis Risk"]

def apply_table_formatting(df):
    df.columns = [f"**{col}**" for col in df.columns]
    return df

if monitoring:
    while True:
        fake_data = {
            'Heart Rate (bpm)': np.random.randint(60, 110),
            'HRV (ms)': np.random.randint(20, 80),
            'SpO2 (%)': np.random.randint(90, 100),
            'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
            'Blood Sugar (mg/dL)': np.random.randint(70, 140),
            'Motion Intensity': np.random.randint(0, 10),
            'Stress Level': np.random.choice(levels),
            'Fatigue Risk': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
            'Health Crisis Risk': np.random.choice(levels, p=[0.57, 0.23, 0.1, 0.1])
        }
        
        df = pd.DataFrame([fake_data])
        data_placeholder.dataframe(apply_table_formatting(df), use_container_width=True)
        time.sleep(3)
