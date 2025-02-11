import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS to improve UI
st.markdown("""
    <style>
        .main { background-color: #f4f4f4; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 10px; padding: 10px; }
        .stDataFrame { background-color: white; border-radius: 10px; padding: 10px; }
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

st.title("🚗 SafeDrive Sync - Driver Safety & Health Monitor")
st.sidebar.header("⚙️ Settings")
monitoring = st.sidebar.toggle("Enable Real-Time Monitoring", value=True)

st.sidebar.subheader("🚘 Vehicle Response Settings")
levels = ['Low', 'Moderate', 'High', 'Critical']
actions = {
    "Basic": ["No Action", "Send Notification"],
    "Comfort": ["Reduce Speed", "Play Calming Music", "Turn On Air Conditioning", "Adjust Seat Position"],
    "Emergency": ["Activate Horn", "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"]
}

stress_actions = {level: st.sidebar.multiselect(f"Stress - {level}", sum(actions.values(), []), default=["Send Notification"]) for level in levels}
fatigue_actions = {level: st.sidebar.multiselect(f"Fatigue - {level}", sum(actions.values(), []), default=["Send Notification"]) for level in levels}
health_crisis_actions = {level: st.sidebar.multiselect(f"Health Crisis - {level}", sum(actions.values(), []), default=["Send Notification"]) for level in levels}

# Dynamic Data Display
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Real-Time Driver Health Data")
    data_placeholder = st.empty()

with col2:
    st.subheader("🚦 Alert System")
    alert_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        df = pd.DataFrame([fake_data])
        data_placeholder.dataframe(df, use_container_width=True)
        alerts = []

        for level in levels:
            if fake_data['Fatigue Risk'] == level:
                alerts.append(f"⚠️ Fatigue Risk {level}: {', '.join(fatigue_actions[level])}")
            if fake_data['Stress Level'] == level:
                alerts.append(f"💆‍♂️ Stress Level {level}: {', '.join(stress_actions[level])}")
            if fake_data['Health Crisis Risk'] == level:
                alerts.append(f"🚑 Health Crisis {level}: {', '.join(health_crisis_actions[level])}")

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
    
st.sidebar.subheader("🔧 Personalization Settings")
alert_threshold = st.sidebar.slider("Fatigue Alert Sensitivity", 1, 10, 5)
st.sidebar.write(f"Current Sensitivity Level: {alert_threshold}")

data_privacy = st.sidebar.checkbox("Enable Data Encryption", value=True)
if data_privacy:
    st.sidebar.success("✅ Data encryption enabled for privacy protection.")
