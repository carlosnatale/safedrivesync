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
    </style>
""", unsafe_allow_html=True)

# Function to generate notifications
def generate_notification(category, level):
    messages = {
        "Stress": {
            "Low": "✅ Normal Condition",
            "Moderate": "🟠 Moderate stress detected. Consider taking deep breaths.",
            "High": "🔴 High stress detected! Reduce distractions and focus on the road.",
            "Critical": "🚨 CRITICAL STRESS! Pull over safely and take a break."
        },
        "Fatigue": {
            "Low": "✅ Normal Condition",
            "Moderate": "🟠 Moderate fatigue detected. Consider stretching or stopping soon.",
            "High": "🔴 High fatigue detected! Take a break immediately.",
            "Critical": "🚨 CRITICAL FATIGUE! Your reaction time is dangerously low. Stop now."
        },
        "Health Crisis": {
            "Low": "✅ Normal Condition",
            "Moderate": "🟠 Mild health irregularity detected. Monitor your condition.",
            "High": "🔴 Significant health concern! Consider seeking medical attention.",
            "Critical": "🚨 EMERGENCY! Health crisis detected. Contact emergency services immediately."
        }
    }
    return messages.get(category, {}).get(level, "❌ Error: Unknown Condition")

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
action_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        notifications = []
        actions_taken = []
        
        for category, risk_key, action_dict in zip(
            ["Stress", "Fatigue", "Health Crisis"],
            ["Stress Level", "Fatigue Risk", "Health Crisis Risk"],
            [stress_actions, fatigue_actions, health_crisis_actions]
        ):
            current_level = fake_data[risk_key]
            selected_actions = action_dict.get(current_level, [])
            
            if "Send Notification" in selected_actions:
                notifications.append(generate_notification(category, current_level))
            for action in selected_actions:
                if action != "Send Notification":
                    actions_taken.append(f"🚗 {action} activated due to {category} ({current_level})")
        
        with data_placeholder.container():
            st.write(fake_data)
        
        with notification_placeholder.container():
            if notifications:
                st.markdown("**📢 Notifications:**<br>" + "<br>".join(notifications), unsafe_allow_html=True)
        
        with action_placeholder.container():
            if actions_taken:
                st.markdown("**🚘 Vehicle Actions Taken:**<br>" + "<br>".join(actions_taken), unsafe_allow_html=True)
        
        time.sleep(3)
