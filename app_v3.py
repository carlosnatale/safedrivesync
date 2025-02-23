import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for the classic dashboard look with updated background color
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: white; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .stDataFrame { background-color: white; color: black; border-radius: 10px; padding: 10px; }
        .stSidebar { background: #e9ecef; }
        .dashboard-container { display: flex; justify-content: space-between; padding: 10px; gap: 20px; }
        .dashboard-box { flex: 1; padding: 15px; border-radius: 10px; background: #ffffff; margin: 10px; border: 2px solid #ced4da; text-align: left; }
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

st.title("🚗 SafeDrive Sync - Health Dashboard")
monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Real-Time Data Display
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()

# Display infotainment image at the end
st.subheader("🖼️ Infotainment System Display")
st.image("infotainment - Copia.png", use_column_width=True)

# Display notifications
if monitoring:
    while True:
        fake_data = generate_fake_data()
        df = pd.DataFrame([fake_data])
        data_placeholder.dataframe(df, use_container_width=True)

        notifications = {"Stress": [], "Fatigue": [], "Health Crisis": []}
        for category, risk_key in zip(
            ["Stress", "Fatigue", "Health Crisis"],
            ["Stress Level", "Fatigue Risk", "Health Crisis Risk"]
        ):
            current_level = fake_data[risk_key]
            notification = generate_notification(category, current_level)
            if notification != "✅ Normal Condition":
                notifications[category].append(notification)

        st.markdown(
            """
            <div class='dashboard-box notification-box'>
                <div class='alert-title'>📢 Car's Infotainment System Notifications</div>
                {}
            </div>
            """.format(
                "<br>".join(
                    [f"<strong>{category}:</strong> {'<br>'.join(notifs) if notifs else '✅ No notifications sent.'}"
                     for category, notifs in notifications.items()]
                )
            ),
            unsafe_allow_html=True
        )
        time.sleep(3)
