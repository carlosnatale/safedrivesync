import streamlit as st
import pandas as pd
import numpy as np
import time

# Simulate real-time biometric data generation
def generate_fake_data():
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(['Low', 'Moderate', 'High']),
        'Fatigue Risk': np.random.choice(['Low', 'Moderate', 'High'], p=[0.6, 0.3, 0.1]),
        'Health Crisis Risk': np.random.choice(['Normal', 'Warning', 'Critical'], p=[0.7, 0.2, 0.1])
    }

# Streamlit UI
st.title("🚗 SafeDrive Sync - Driver Safety & Health Monitor")

st.sidebar.header("Settings")
monitoring = st.sidebar.checkbox("Enable Real-Time Monitoring", value=True)

# Vehicle Behavior Customization Based on Thresholds
st.sidebar.subheader("🚘 Vehicle Response Settings")

disable_notifications_fatigue = st.sidebar.checkbox("Disable Fatigue Notifications", value=False)
disable_notifications_stress = st.sidebar.checkbox("Disable Stress Notifications", value=False)
disable_notifications_health = st.sidebar.checkbox("Disable Health Crisis Notifications", value=False)

fatigue_actions_high = st.sidebar.multiselect(
    "Select Actions for High Fatigue Risk:",
    ["Send Notifications Only", "Reduce Speed", "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn"],
    default=["Send Notifications Only"]
)

fatigue_actions_moderate = st.sidebar.multiselect(
    "Select Actions for Moderate Fatigue Risk:",
    ["Send Notifications Only", "Suggest a Short Break", "Play Relaxing Sounds", "Increase Seat Comfort"],
    default=["Send Notifications Only"]
)

health_crisis_actions = st.sidebar.multiselect(
    "Select Actions for Health Crisis:",
    ["Call Emergency Services", "Alert Emergency Contacts", "Activate Autopilot", "Flash Alert Lights", "Rock Seat or Steering Wheel"],
    default=["Call Emergency Services", "Alert Emergency Contacts"]
)

stress_actions_high = st.sidebar.multiselect(
    "Select Actions for High Stress Level:",
    ["Send Notifications Only", "Play Calming Music", "Adjust Seat Position", "Activate Air Conditioning", "Reduce Speed"],
    default=["Send Notifications Only"]
)

stress_actions_moderate = st.sidebar.multiselect(
    "Select Actions for Moderate Stress Level:",
    ["Send Notifications Only", "Suggest Deep Breathing", "Lower Radio Volume", "Adjust Cabin Lighting"],
    default=["Send Notifications Only"]
)

if monitoring:
    st.subheader("📊 Real-Time Driver Health Data")
    placeholder = st.empty()
    
    while True:
        fake_data = generate_fake_data()
        df = pd.DataFrame([fake_data])
        
        # Display data
        placeholder.dataframe(df)
        
        # Fatigue alert
        if not disable_notifications_fatigue:
            if fake_data['Fatigue Risk'] == 'High':
                st.error("🚨 High Fatigue Risk! Take a break immediately.")
                for action in fatigue_actions_high:
                    st.warning(f"🚗 Action Triggered: {action}")
            elif fake_data['Fatigue Risk'] == 'Moderate':
                st.warning("⚠️ Moderate Fatigue Detected. Consider resting soon.")
                for action in fatigue_actions_moderate:
                    st.info(f"📢 Action Triggered: {action}")
        
        # Health crisis alert
        if not disable_notifications_health:
            if fake_data['Health Crisis Risk'] == 'Critical':
                st.error("🚨 Critical Health Warning! Emergency services alerted.")
                for action in health_crisis_actions:
                    st.warning(f"🚑 Action Triggered: {action}")
            elif fake_data['Health Crisis Risk'] == 'Warning':
                st.warning("⚠️ Health anomaly detected. Monitor closely.")
        
        # Stress alert
        if not disable_notifications_stress:
            if fake_data['Stress Level'] == 'High':
                st.warning("⚠️ High Stress Level Detected. Consider relaxation measures.")
                for action in stress_actions_high:
                    st.warning(f"💆‍♂️ Action Triggered: {action}")
            elif fake_data['Stress Level'] == 'Moderate':
                st.info("🧘 Moderate Stress Detected. Take calming measures.")
                for action in stress_actions_moderate:
                    st.info(f"🛠️ Action Triggered: {action}")
        
        time.sleep(3)  # Simulate real-time update

else:
    st.write("Monitoring is disabled. Enable it from the sidebar.")

# Post-trip Summary Button
if st.button("📉 Generate Trip Summary"):
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
    
# User Customization Settings
st.sidebar.subheader("🔧 Personalization Settings")
alert_threshold = st.sidebar.slider("Fatigue Alert Sensitivity", 1, 10, 5)
st.sidebar.write(f"Current Sensitivity Level: {alert_threshold}")

data_privacy = st.sidebar.checkbox("Enable Data Encryption", value=True)
if data_privacy:
    st.sidebar.success("✅ Data encryption enabled for privacy protection.")
