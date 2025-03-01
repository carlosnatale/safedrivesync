import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit Configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Improved Visualization
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: black; }
        .dashboard-box { flex: 1; padding: 15px; border-radius: 10px; background: #ffffff; margin: 10px; border: 2px solid #ced4da; text-align: left; }
        .health-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            padding: 10px;
        }
        .metric-box {
            background: #1e1e1e;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            color: white;
        }
        .metric-title {
            font-weight: bold;
            font-size: 18px;
            color: #f0f0f0;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 22px;
            font-weight: bold;
            color: #00d4ff;
        }
        .progress-container {
            height: 10px;
            background: #404040;
            border-radius: 5px;
            margin-top: 5px;
            width: 80%;
            margin-left: auto;
            margin-right: auto;
        }
        .progress-bar {
            height: 100%;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Function to generate notifications
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

# Function to generate real-time biometric data
def generate_fake_data():
    levels = ['Low', 'Moderate', 'High', 'Critical']
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar': np.random.randint(70, 140),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels),
        'Health Crisis Risk': np.random.choice(levels)
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

st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()
notification_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        notifications = []
        
        with data_placeholder.container():
            st.markdown('<div class="health-metrics">', unsafe_allow_html=True)
            for key, value in fake_data.items():
                if isinstance(value, int):
                    bar_color = "#00d4ff" if value < 80 else "#ffcc00" if value < 100 else "#ff4444"
                    progress_percentage = value / 150 * 100
                    st.markdown(
                        f'<div class="metric-box">'
                        f'<div class="metric-title">{key}</div>'
                        f'<div class="metric-value">{value}</div>'
                        f'<div class="progress-container">'
                        f'<div class="progress-bar" style="width: {progress_percentage}%; background: {bar_color};"></div>'
                        f'</div>'
                        f'</div>', unsafe_allow_html=True)
                else:
                    notifications.append(generate_notification(key, value))
                    st.markdown(
                        f'<div class="metric-box">'
                        f'<div class="metric-title">{key}</div>'
                        f'<div class="metric-value">{value}</div>'
                        f'</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with notification_placeholder.container():
            if notifications:
                st.markdown("<b>📢 Notifications:</b><br>" + "<br>".join(notifications), unsafe_allow_html=True)
        
        time.sleep(3)
