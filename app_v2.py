import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: black; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .stDataFrame { background-color: white; color: black; border-radius: 10px; padding: 10px; }
        .stSidebar { background: #e9ecef; }
        .dashboard-container { display: flex; justify-content: space-between; padding: 10px; gap: 20px; }
        .dashboard-box { 
            flex: 1; 
            padding: 20px; 
            border-radius: 10px; 
            background: #ffffff; 
            margin: 10px; 
            border: 2px solid #ced4da; 
            text-align: left;
            transition: transform 0.2s ease;
        }
        .dashboard-box:hover { transform: translateY(-3px); }
        .action-box { border-left: 4px solid #004085; }
        .notification-box { border-left: 4px solid #dc3545; }
        .alert-title { 
            font-weight: bold; 
            font-size: 22px; 
            margin-bottom: 15px; 
            text-align: left;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .status-item { margin-bottom: 15px; }
        .status-indicator { font-size: 18px; margin-right: 8px; }
        .metric-header { 
            font-size: 18px !important; 
            margin: 0 0 12px 0 !important; 
            color: #2c3e50; 
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .status-text { margin-left: 28px; }
    </style>
""", unsafe_allow_html=True)

# Restored function
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

# Restored critical function
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

# Vehicle Response Settings (unchanged)
# ... [Keep the existing action configuration code] ...

# Real-Time Data Display (updated visualization)
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()
action_placeholder = st.empty()
notification_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        
        # Health Data Visualization (existing implementation)
        # ... [Keep the health data visualization code] ...

        # Updated Vehicle Actions Display
        actions_taken = {"Stress": [], "Fatigue": [], "Health Crisis": []}
        notifications = {"Stress": [], "Fatigue": [], "Health Crisis": []}

        # Action processing logic (unchanged)
        # ... [Keep existing action processing code] ...

        # Enhanced Vehicle Actions Display
        action_placeholder.markdown(f"""
        <div class='dashboard-container'>
            <div class='dashboard-box action-box'>
                <div class='alert-title'>
                    <div style='font-size: 24px;'>🚗</div>
                    <h3>Vehicle Actions</h3>
                </div>
                {"".join([
                    f"""<div class='status-item'>
                        <div class='metric-header'>
                            <span class='status-indicator'>{
                                "🟢" if not actions else "🔴"
                            }</span>
                            <strong>{category}</strong>
                        </div>
                        <div class='status-text' style='color: {
                            '#2ecc71' if not actions else '#e74c3c'
                        };'>
                            {', '.join(actions) if actions else 'No actions taken'}
                        </div>
                    </div>"""
                    for category, actions in actions_taken.items()
                ])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced Notifications Display
        notification_placeholder.markdown(f"""
        <div class='dashboard-container'>
            <div class='dashboard-box notification-box'>
                <div class='alert-title'>
                    <div style='font-size: 24px;'>📢</div>
                    <h3>Infotainment Notifications</h3>
                </div>
                {"".join([
                    f"""<div class='status-item'>
                        <div class='metric-header'>
                            <span class='status-indicator'>{
                                "🟢" if not notifs else 
                                "🟠" if "Moderate" in str(notifs) else 
                                "🔴"
                            }</span>
                            <strong>{category}</strong>
                        </div>
                        <div class='status-text' style='color: {
                            '#2ecc71' if not notifs else 
                            '#e67e22' if "Moderate" in str(notifs) else 
                            '#e74c3c'
                        };'>
                            {', '.join(notifs) if notifs else 'Normal condition'}
                        </div>
                    </div>"""
                    for category, notifs in notifications.items()
                ])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(3)
