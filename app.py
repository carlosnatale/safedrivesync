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
        .dashboard-container { display: flex; justify-content: space-around; text-align: center; }
        .dashboard-section { padding: 15px; border-radius: 10px; background: #ffffff; margin: 10px; border: 1px solid #ced4da; }
        .alert-container { display: flex; flex-direction: column; gap: 10px; }
        .alert-box { padding: 10px; border-radius: 5px; background: #ffebcc; border: 1px solid #ffa500; }
        .action-box { padding: 10px; border-radius: 5px; background: #cce5ff; border: 1px solid #004085; }
    </style>
""", unsafe_allow_html=True)

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
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
        'Health Crisis Risk': np.random.choice(levels, p=health_crisis_probs)  # Ensures matching array sizes
    }

st.title("🚗 SafeDrive Sync - Classic Dashboard UI")

monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Vehicle Response Settings in a Classic Dashboard Layout
st.subheader("🚘 Vehicle Response Settings")
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

if monitoring:
    while True:
        fake_data = generate_fake_data()
        df = pd.DataFrame([fake_data])
        data_placeholder.dataframe(df, use_container_width=True)
        alerts = []
        actions_taken = []

        for category, risk_key, action_dict in zip(
            ["Stress", "Fatigue", "Health Crisis"],
            ["Stress Level", "Fatigue Risk", "Health Crisis Risk"],
            [stress_actions, fatigue_actions, health_crisis_actions]
        ):
            current_level = fake_data[risk_key]
            alert_message = f"{category} Level: {current_level}" if current_level != "Low" else "Normal Condition"
            selected_actions = ", ".join(action_dict.get(current_level, ["No Action Required"]))
            alerts.append(f"{category}: {alert_message}")
            actions_taken.append(f"{category}: {selected_actions}")
        
        alert_placeholder.markdown(f"""<div class='alert-container'>
            <div class='alert-box'><strong>Notifications:</strong><br>{'<br>'.join(alerts)}</div>
        </div>""", unsafe_allow_html=True)
        
        action_placeholder.markdown(f"""<div class='alert-container'>
            <div class='action-box'><strong>Vehicle Actions:</strong><br>{'<br>'.join(actions_taken)}</div>
        </div>""", unsafe_allow_html=True)
        
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
