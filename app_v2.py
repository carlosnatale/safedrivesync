import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements - Modern Infotainment System
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Modern UI
st.markdown("""
    <style>
        body { background-color: #121212; color: #ffffff; }
        .main { background: rgba(0, 0, 0, 0.8); color: white; }
        .stButton>button { 
            border-radius: 10px; 
            padding: 12px; 
            background: linear-gradient(90deg, #0066ff, #00ccff);
            color: white; 
            font-weight: bold; 
            border: none; 
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #0044cc, #0099cc);
        }
        .stDataFrame { 
            background-color: rgba(255, 255, 255, 0.1); 
            color: white; 
            border-radius: 12px; 
            padding: 10px; 
        }
        .stSidebar { background: rgba(50, 50, 50, 0.9); color: white; }
        .dashboard-box { 
            padding: 20px; 
            border-radius: 15px; 
            background: rgba(255, 255, 255, 0.1); 
            border: 1px solid rgba(255, 255, 255, 0.2); 
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        }
        .alert-title { font-weight: bold; font-size: 22px; margin-bottom: 10px; text-align: center; }
        .alert-content { font-size: 18px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 SafeDrive Sync - Next-Gen Infotainment System")

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

# Real-Time Data Display - Modern UI
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()
action_placeholder = st.empty()
notification_placeholder = st.empty()

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
            "Critical": "🚨 CRITICAL FATIGUE! Stop now."
        },
        "Health Crisis": {
            "Moderate": "🟠 Mild health irregularity detected. Monitor your condition.",
            "High": "🔴 Significant health concern! Seek medical attention.",
            "Critical": "🚨 EMERGENCY! Health crisis detected. Contact emergency services immediately."
        }
    }
    return messages.get(category, {}).get(level, "✅ Normal Condition")

# Simulate real-time biometric data
def generate_fake_data():
    levels = ['Low', 'Moderate', 'High', 'Critical']
    health_crisis_probs = np.array([0.57, 0.23, 0.1, 0.1])
    health_crisis_probs /= health_crisis_probs.sum()
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar (mg/dL)': np.random.randint(70, 140),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
        'Health Crisis Risk': np.random.choice(levels, p=health_crisis_probs)
    }

if monitoring:
    while True:
        fake_data = generate_fake_data()
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
                    notifications[category].append(generate_notification(category, current_level))
                else:
                    actions_taken[category].append(f"🚗 {action} activated due to {category} ({current_level})")
        
        time.sleep(3)
