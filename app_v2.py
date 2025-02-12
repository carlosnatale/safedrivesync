import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements - Classic Dashboard Look
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Enhanced Dashboard Look
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; color: black; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .stDataFrame { background-color: white; color: black; border-radius: 10px; padding: 10px; }
        .stSidebar { background: #e9ecef; }
        .dashboard-container { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 10px; }
        .dashboard-box { padding: 15px; border-radius: 10px; background: #ffffff; border: 2px solid #ced4da; text-align: left; }
        .action-box { background: #d1ecf1; border: 3px solid #004085; font-size: 18px; }
        .notification-box { background: #f8d7da; border: 3px solid #dc3545; font-size: 18px; }
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

def action_multiselect(label, actions):
    return st.multiselect(f"{label}", actions, default=["Send Notification"])

st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)

with st.container():
    st.subheader("🧘 Stress Actions")
    stress_actions = {level: action_multiselect(f"Stress {level}", actions) for level in levels}

with st.container():
    st.subheader("😴 Fatigue Actions")
    fatigue_actions = {level: action_multiselect(f"Fatigue {level}", actions) for level in levels}

with st.container():
    st.subheader("🚑 Health Crisis Actions")
    health_crisis_actions = {level: action_multiselect(f"Health Crisis {level}", actions) for level in levels}

st.markdown("</div>", unsafe_allow_html=True)

# Real-Time Data Display
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()
action_placeholder = st.empty()
notification_placeholder = st.empty()

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
        data_placeholder.dataframe(df, use_container_width=True)
        actions_taken = {"Stress": [], "Fatigue": [], "Health Crisis": []}
        notifications = {"Stress": [], "Fatigue": [], "Health Crisis": []}

        for category, risk_key, action_dict in zip(
            ["Stress", "Fatigue", "Health Crisis"],
            ["Stress Level", "Fatigue Risk", "Health Crisis Risk"],
            [stress_actions, fatigue_actions, health_crisis_actions]
        ):
            current_level = fake_data[risk_key]
            selected_actions = action_dict.get(current_level, [])
            
            for action in selected_actions:
                if action == "Send Notification":
                    notifications[category].append(f"📢 {category} {current_level} alert!")
                else:
                    actions_taken[category].append(f"🚗 {action} activated due to {category} ({current_level})")

        action_placeholder.markdown(
            "<div class='dashboard-box action-box'><div class='alert-title'>🚗 Vehicle Actions</div>" +
            "<br>".join([f"<strong>{category}:</strong> {'<br>'.join(actions) if actions else '✅ No actions taken.'}" for category, actions in actions_taken.items()]) +
            "</div>", unsafe_allow_html=True)

        notification_placeholder.markdown(
            "<div class='dashboard-box notification-box'><div class='alert-title'>📢 Car's Infotainment System Notifications</div>" +
            "<br>".join([f"<strong>{category}:</strong> {'<br>'.join(notifs) if notifs else '✅ No notifications sent.'}" for category, notifs in notifications.items()]) +
            "</div>", unsafe_allow_html=True)
        
        time.sleep(3)
