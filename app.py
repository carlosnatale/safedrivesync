import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements - Tesla-Style UI
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Tesla-style UI
st.markdown("""
    <style>
        .main { background-color: #1e1e1e; color: white; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 10px; padding: 12px; background: #222; color: white; border: 1px solid white; }
        .stDataFrame { background-color: black; color: white; border-radius: 10px; padding: 10px; }
        .stSidebar { background: #181818; }
        .dashboard-container { display: flex; justify-content: space-around; text-align: center; }
        .dashboard-section { padding: 20px; border-radius: 10px; background: #2a2a2a; margin: 10px; }
    </style>
""", unsafe_allow_html=True)

# Simulate real-time biometric data generation
def generate_fake_data():
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(['Low', 'Moderate', 'High', 'Critical']),
        'Fatigue Risk': np.random.choice(['Low', 'Moderate', 'High', 'Critical'], p=[0.5, 0.3, 0.15, 0.05]),
        'Health Crisis Risk': np.random.choice(['Normal', 'Warning', 'Critical'], p=[0.7, 0.2, 0.1])
    }

st.title("🚗 SafeDrive Sync - Tesla-Style UI")

monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Vehicle Response Settings in Grid-Style Layout
st.subheader("🚘 Vehicle Response Settings")
levels = ['Low', 'Moderate', 'High', 'Critical']
actions = [
    "No Action", "Send Notification", "Reduce Speed", "Play Calming Music", "Turn On Air Conditioning", 
    "Adjust Seat Position", "Activate Horn", "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

def action_checkboxes(label, actions):
    return {action: st.checkbox(f"{label}: {action}", value=(action == "Send Notification")) for action in actions}

st.subheader("🧘 Stress Actions")
stress_actions = {level: action_checkboxes(f"Stress {level}", actions) for level in levels}

st.subheader("😴 Fatigue Actions")
fatigue_actions = {level: action_checkboxes(f"Fatigue {level}", actions) for level in levels}

st.subheader("🚑 Health Crisis Actions")
health_crisis_actions = {level: action_checkboxes(f"Health Crisis {level}", actions) for level in levels}

# Real-Time Data Display - Tesla-Style Grid
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()

st.subheader("🚦 Alert System")
alert_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        df = pd.DataFrame([fake_data])
        data_placeholder.dataframe(df, use_container_width=True)
        alerts = []

        for level in levels:
            selected_fatigue_actions = [action for action, selected in fatigue_actions[level].items() if selected]
            selected_stress_actions = [action for action, selected in stress_actions[level].items() if selected]
            selected_health_actions = [action for action, selected in health_crisis_actions[level].items() if selected]
            
            if fake_data['Fatigue Risk'] == level:
                alerts.append(f"⚠️ Fatigue Risk {level}: {', '.join(selected_fatigue_actions)}")
            if fake_data['Stress Level'] == level:
                alerts.append(f"💆‍♂️ Stress Level {level}: {', '.join(selected_stress_actions)}")
            if fake_data['Health Crisis Risk'] == level:
                alerts.append(f"🚑 Health Crisis {level}: {', '.join(selected_health_actions)}")

        alert_placeholder.warning("\n".join(alerts) if alerts else "✅ No critical alerts detected.")
        time.sleep(3)
else:
    st.write("Monitoring is disabled. Enable it from the sidebar.")

# Post-trip Summary Button
if st.button("📉 Generate Trip Summary", use_container_width=True):
    summary_data = {
        'Average Heart Rate': np.random.randint(70, 100),
        'Average HRV': np.random.randint(30, 70),
        'Average SpO2': np.random.randint(92, 99),
        'Fatigue Events Detected': np.random.randint(0, 5),
        'Stress Events Detected': np.random.randint(0, 5),
        'Health Alerts Triggered': np.random.randint(0, 3)
    }
    st.subheader("🔍 Trip Summary")
    st.json(summary_data)
    
    if summary_data['Fatigue Events Detected'] > 3:
        st.error("🚨 Fatigue detected multiple times! Reduce driving hours.")
    elif summary_data['Fatigue Events Detected'] > 0:
        st.warning("⚠️ Fatigue incidents occurred. Consider reviewing sleep patterns.")
    else:
        st.success("✅ No fatigue events detected. Safe driving!")
    
    if summary_data['Health Alerts Triggered'] > 0:
        st.warning("⚠️ Health alerts were triggered during the trip. Review details.")
