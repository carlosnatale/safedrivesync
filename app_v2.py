import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit Configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Ensure rerun flag is in session state
if "rerun_flag" not in st.session_state:
    st.session_state.rerun_flag = False

# Custom CSS for Mobile Optimization
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: white; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .dashboard-container { display: flex; justify-content: space-between; padding: 10px; gap: 20px; }
        .dashboard-box { flex: 1; padding: 15px; border-radius: 10px; background: #ffffff; margin: 10px; border: 2px solid #ced4da; text-align: left; }
    </style>
""", unsafe_allow_html=True)

# Function to Generate Fake Data
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

# UI Components
st.title("🚗 SafeDrive Sync - Health Dashboard")
monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

data_placeholder = st.empty()

# Define actions
st.subheader("🚘 Configure Vehicle Actions")
levels = ['Low', 'Moderate', 'High', 'Critical']
actions = [
    "No Action", "Send Notification", "Reduce Speed", "Play Calming Music",
    "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn",
    "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

def action_multiselect(label, actions, category, level):
    return st.multiselect(
        f"{label}", 
        actions, 
        default=["Send Notification"], 
        key=f"{category}_{level}"
    )

stress_actions = {level: action_multiselect(f"Stress {level}", actions, "stress", level) for level in levels}
fatigue_actions = {level: action_multiselect(f"Fatigue {level}", actions, "fatigue", level) for level in levels}
health_crisis_actions = {level: action_multiselect(f"Health Crisis {level}", actions, "health", level) for level in levels}

action_placeholder = st.empty()
notification_placeholder = st.empty()

if monitoring:
    if st.session_state.rerun_flag:
        st.session_state.rerun_flag = False
        st.rerun()

    if 'last_update' not in st.session_state or time.time() - st.session_state.last_update > 3:
        st.session_state.last_update = time.time()
        fake_data = generate_fake_data()

        with data_placeholder.container():
            st.markdown("""
                <div class='dashboard-box'><b>📊 Health Data:</b><br>
                ❤️ **Heart Rate:** {fake_data['Heart Rate (bpm)']} bpm<br>
                📶 **HRV:** {fake_data['HRV (ms)']} ms<br>
                🩸 **SpO2:** {fake_data['SpO2 (%)']}%<br>
                🩺 **Blood Pressure:** {fake_data['Blood Pressure']}<br>
                🍬 **Blood Sugar:** {fake_data['Blood Sugar']} mg/dL<br>
                🏃 **Motion Intensity:** {fake_data['Motion Intensity']}<br>
                ⚠️ **Stress Level:** {fake_data['Stress Level']}<br>
                😴 **Fatigue Risk:** {fake_data['Fatigue Risk']}<br>
                🚨 **Health Crisis Risk:** {fake_data['Health Crisis Risk']}<br>
                </div>
            """, unsafe_allow_html=True)
        
        notifications = []
        actions_taken = []
        for category, risk_key, action_dict in zip(
            ["Stress", "Fatigue", "Health Crisis"],
            ["Stress Level", "Fatigue Risk", "Health Crisis Risk"],
            [stress_actions, fatigue_actions, health_crisis_actions]
        ):
            current_level = fake_data[risk_key]
            selected_actions = action_dict.get(current_level, [])
            for action in selected_actions:
                if action == "Send Notification":
                    notifications.append(f"📢 {category} Alert: {current_level}")
                else:
                    actions_taken.append(f"🚗 {action} activated due to {category} ({current_level})")
        
        with notification_placeholder.container():
            if notifications:
                st.markdown("<div class='dashboard-box'><b>📢 Notifications:</b><br>" + "<br>".join(notifications) + "</div>", unsafe_allow_html=True)
        
        with action_placeholder.container():
            if actions_taken:
                st.markdown("<div class='dashboard-box'><b>🚘 Vehicle Actions Taken:</b><br>" + "<br>".join(actions_taken) + "</div>", unsafe_allow_html=True)
        
        st.session_state.rerun_flag = True
