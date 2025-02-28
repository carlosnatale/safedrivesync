import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit Configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Mobile Optimization
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: black; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .dashboard-container { display: flex; justify-content: space-between; padding: 10px; gap: 20px; }
        .dashboard-box { flex: 1; padding: 15px; border-radius: 10px; background: #ffffff; margin: 10px; border: 2px solid #ced4da; text-align: left; }
        .mobile-metrics {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
        }
        .metric-box {
            background: linear-gradient(135deg, #f0f2f5, #d9e2ec);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #ced4da;
            text-align: center;
            flex: 1 1 calc(50% - 20px);
            min-width: 140px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        }
        .metric-title {
            font-weight: bold;
            font-size: 16px;
            color: #495057;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 20px;
            font-weight: bold;
            color: #007bff;
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

# Generate real-time biometric data
def generate_fake_data():
    levels = ['Low', 'Moderate', 'High', 'Critical']
    health_crisis_probs = np.array([0.57, 0.23, 0.1, 0.1])
    health_crisis_probs /= health_crisis_probs.sum()

    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar': np.random.randint(70, 140),
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

st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()
notification_placeholder = st.empty()
if monitoring:
    while True:
        fake_data = generate_fake_data()
        
        with data_placeholder.container():
            st.markdown('<div class="mobile-metrics">', unsafe_allow_html=True)
            for key, value in fake_data.items():
                st.markdown(
                    f'<div class="metric-box">'
                    f'<div class="metric-title">{key}</div>'
                    f'<div class="metric-value">{value}</div>'
                    f'</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display notifications
        notifications = [
            generate_notification("Stress", fake_data['Stress Level']),
            generate_notification("Fatigue", fake_data['Fatigue Risk']),
            generate_notification("Health Crisis", fake_data['Health Crisis Risk'])
        ]
        with notification_placeholder.container():
            st.markdown("<div class='dashboard-box'><b>📢 Notifications:</b><br>" + "<br>".join(notifications) + "</div>", unsafe_allow_html=True)
        
        time.sleep(3)
