import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements - Classic Dashboard Look
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Classic Dashboard Look
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; color: black; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .stDataFrame { background-color: white; color: black; border-radius: 10px; padding: 10px; }
        .stSidebar { background: #e9ecef; }
        .dashboard-container { display: flex; justify-content: space-between; padding: 10px; gap: 20px; }
        .dashboard-box { flex: 1; padding: 15px; border-radius: 10px; background: #ffffff; margin: 10px; border: 2px solid #ced4da; text-align: left; }
        .alert-box { padding: 20px; border-radius: 10px; background: #ffeeba; border: 3px solid #ff851b; text-align: left; font-size: 18px; }
        .action-box { padding: 20px; border-radius: 10px; background: #d1ecf1; border: 3px solid #004085; text-align: left; font-size: 18px; }
        .notification-box { padding: 20px; border-radius: 10px; background: #f8d7da; border: 3px solid #dc3545; text-align: left; font-size: 18px; }
        .alert-title { font-weight: bold; font-size: 22px; margin-bottom: 15px; text-align: center; }
        .alert-content { font-size: 20px; padding: 10px 15px; }
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
    
    # Ensuring the probability array matches the number of levels
    health_crisis_probs = np.array([0.57, 0.23, 0.1, 0.1])
    health_crisis_probs /= health_crisis_probs.sum()  # Normalize to ensure exact sum of 1.0

    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar (mg/dL)': np.random.randint(70, 140),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
        'Health Crisis Risk': np.random.choice(levels, p=health_crisis_probs)  # Ensures matching array sizes
    }

st.title("🚗 SafeDrive Sync - Classic Dashboard UI")

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

# Real-Time Data Display - Classic Dashboard Look
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()

st.subheader("🚦 Alert System")
alert_placeholder = st.empty()
action_placeholder = st.empty()
notification_placeholder = st.empty()

if monitoring:
    fake_data = generate_fake_data()
    df = pd.DataFrame([fake_data])
    data_placeholder.dataframe(df, use_container_width=True)
    alerts = []
    actions_taken = []
    notifications = []

    for category, risk_key, action_dict in zip(
        ["Stress", "Fatigue", "Health Crisis"],
        ["Stress Level", "Fatigue Risk", "Health Crisis Risk"],
        [stress_actions, fatigue_actions, health_crisis_actions]
    ):
        current_level = fake_data[risk_key]
        alert_message = f"⚠️ {category} Level: {current_level}" if current_level != "Low" else "✅ Normal Condition"
        selected_actions = "<br>".join(action_dict.get(current_level, ["No Action Required"]))
        alerts.append(f"<div class='alert-content'>{alert_message}</div>")
        actions_taken.append(f"<div class='alert-content'><strong>{category}:</strong> {selected_actions}</div>")
        
        if "Send Notification" in action_dict.get(current_level, []):
            notifications.append(f"<div class='alert-content'>{generate_notification(category, current_level)}</div>")
    
    alert_placeholder.markdown("\n".join(alerts), unsafe_allow_html=True)
    action_placeholder.markdown("\n".join(actions_taken), unsafe_allow_html=True)
    notification_placeholder.markdown("\n".join(notifications) if notifications else "✅ No notifications sent.", unsafe_allow_html=True)
