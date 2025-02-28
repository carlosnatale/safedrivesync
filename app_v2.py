import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit Configuration
st.set_page_config(page_title="SafeDrive Sync", layout="centered")

# Custom CSS for Mobile Optimization
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: black; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .dashboard-container { display: flex; flex-direction: column; align-items: center; gap: 15px; }
        .dashboard-box { width: 95%; padding: 15px; border-radius: 10px; background: #ffffff; border: 2px solid #ced4da; text-align: center; }
        .alert-title { font-weight: bold; font-size: 18px; margin-bottom: 10px; }
        .alert-content { font-size: 16px; }
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

st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()
notification_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        df = pd.DataFrame([fake_data])
        
        # Adjusted for Mobile View: Use Table Instead of DataFrame
        with data_placeholder.container():
            st.table(df)
        
        notifications = {"Stress": [], "Fatigue": [], "Health Crisis": []}
        
        for category, risk_key in zip(["Stress", "Fatigue", "Health Crisis"],
                                      ["Stress Level", "Fatigue Risk", "Health Crisis Risk"]):
            current_level = fake_data[risk_key]
            notifications[category].append(generate_notification(category, current_level))

        with notification_placeholder.container():
            for category, notifs in notifications.items():
                if notifs:
                    st.markdown(f"**{category} Alerts:**")
                    st.markdown("<div class='dashboard-box'>" + "<br>".join(notifs) + "</div>", unsafe_allow_html=True)
        
        time.sleep(3)
