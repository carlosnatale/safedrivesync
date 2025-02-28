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

# Function to generate personalized notifications
def generate_notification(category, level):
    messages = {
        "Stress": {
            "Moderate": "🟠 Moderate stress detected. Consider taking deep breaths.",
            "High": "🔴 High stress detected! Reduce distractions and focus on the road.",
            "Critical": "🚨 CRITICAL STRESS! Pull over safely and take a break."
        },
        "Fatigue": {
            "Moderate": "🟠 Moderate fatigue detected. Consider stretching or stopping soon.",
            "High": "🔴 High fatigue detected! Take a break immediately.",
            "Critical": "🚨 CRITICAL FATIGUE! Your reaction time is dangerously low. Stop now."
        },
        "Health Crisis": {
            "Moderate": "🟠 Mild health irregularity detected. Monitor your condition.",
            "High": "🔴 Significant health concern! Consider seeking medical attention.",
            "Critical": "🚨 EMERGENCY! Health crisis detected. Contact emergency services immediately."
        }
    }
    return messages.get(category, {}).get(level, "✅ Normal Condition")

# Simulate real-time biometric data generation
def generate_fake_data():
    levels = ['Low', 'Moderate', 'High', 'Critical']
    health_crisis_probs = np.array([0.57, 0.23, 0.1, 0.1])
    health_crisis_probs /= health_crisis_probs.sum()

    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar (mg/dL)': np.random.randint(70, 140),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
        'Health Crisis Risk': np.random.choice(levels, p=health_crisis_probs)
    }

st.title("🚗 SafeDrive Sync - Health Dashboard")
monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Vehicle Response Settings
st.subheader("🚘 Configure Vehicle Actions")
levels = ['Low', 'Moderate', 'High', 'Critical']
actions = [
    "No Action", "Send Notification", "Reduce Speed", "Play Calming Music", "Turn On Air Conditioning", 
    "Adjust Seat Position", "Activate Horn", "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

def action_multiselect(label, actions):
    return st.multiselect(f"{label}", actions, default=["Send Notification"])

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🧘 Stress Actions")
    stress_actions = {level: action_multiselect(f"Stress {level}", actions) for level in levels}

with col2:
    st.subheader("😴 Fatigue Actions")
    fatigue_actions = {level: action_multiselect(f"Fatigue {level}", actions) for level in levels}

with col3:
    st.subheader("🚑 Health Crisis Actions")
    health_crisis_actions = {level: action_multiselect(f"Health Crisis {level}", actions) for level in levels}

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
