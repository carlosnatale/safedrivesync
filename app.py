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

# Notification generator
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

# Data generator
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
        'Body Temperature': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
        'Health Crisis Risk': np.random.choice(levels, p=health_crisis_probs)
    }

st.title("🚗 SafeDrive Sync - Health Dashboard")
monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Vehicle Response Settings
st.subheader("🚘 Configure Vehicle Actions")
levels = ['Low', 'Moderate', 'High', 'Critical']
actions = [
    "No Action", "Send Notification", "Reduce Speed", "Play Calming Music", 
    "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn", 
    "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
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

# Real-Time Data Display
st.subheader("📊 Real-Time Driver Health Data")
data_placeholder = st.empty()
action_placeholder = st.empty()
notification_placeholder = st.empty()

if monitoring:
    while True:
        fake_data = generate_fake_data()
        
        # Health Metrics Visualization
        with data_placeholder.container():
            # First row - Vital Signs
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class='dashboard-box' style='border-left: 5px solid #4CAF50;'>
                    <h3 style='margin:0; color: #2c3e50;'>❤️ Heart Rate</h3>
                    <div style='display: flex; align-items: baseline; gap: 10px;'>
                        <span style='font-size: 34px; font-weight: bold; color: #2c3e50;'>{fake_data['Heart Rate (bpm)']}</span>
                        <span style='font-size: 16px; color: #7f8c8d;'>bpm</span>
                    </div>
                    <div style='color: #4CAF50; font-weight: 500;'>Normal</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class='dashboard-box' style='border-left: 5px solid #2196F3;'>
                    <h3 style='margin:0; color: #2c3e50;'>🔄 HRV</h3>
                    <div style='display: flex; align-items: baseline; gap: 10px;'>
                        <span style='font-size: 34px; font-weight: bold; color: #2c3e50;'>{fake_data['HRV (ms)']}</span>
                        <span style='font-size: 16px; color: #7f8c8d;'>ms</span>
                    </div>
                    <div style='color: #2196F3; font-weight: 500;'>Variability</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                st.markdown(f"""
                <div class='dashboard-box' style='border-left: 5px solid #9C27B0;'>
                    <h3 style='margin:0; color: #2c3e50;'>🩸 SpO2</h3>
                    <div style='display: flex; align-items: baseline; gap: 10px;'>
                        <span style='font-size: 34px; font-weight: bold; color: #2c3e50;'>{fake_data['SpO2 (%)']}</span>
                        <span style='font-size: 16px; color: #7f8c8d;'>%</span>
                    </div>
                    <div style='color: #9C27B0; font-weight: 500;'>Oxygenation</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col4:
                st.markdown(f"""
                <div class='dashboard-box' style='border-left: 5px solid #FF9800;'>
                    <h3 style='margin:0; color: #2c3e50;'>🩸 Blood Pressure</h3>
                    <div style='font-size: 34px; font-weight: bold; color: #2c3e50;'>{fake_data['Blood Pressure (mmHg)']}</div>
                    <div style='color: #FF9800; font-weight: 500;'>Continuous Monitoring</div>
                </div>
                """, unsafe_allow_html=True)

            # Second row - Other Metrics
            col5, col6, col7 = st.columns(3)
            with col5:
                st.markdown(f"""
                <div class='dashboard-box'>
                    <h3 style='margin:0; color: #2c3e50;'>🏃 Body Temperature</h3>
                    <div style='display: flex; align-items: center; gap: 15px;'>
                        <div style='font-size: 42px; font-weight: bold; color: #e74c3c;'>{fake_data['Body Temperature']}</div>
                        <div style='width: 100%; background: #eee; height: 10px; border-radius: 5px;'>
                            <div style='width: {fake_data['Body Temperature']*10}%; background: #e74c3c; height: 10px; border-radius: 5px;'></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col6:
                stress_color = {"Low": "#2ecc71", "Moderate": "#f1c40f", "High": "#e67e22", "Critical": "#e74c3c"}[fake_data['Stress Level']]
                st.markdown(f"""
                <div class='dashboard-box'>
                    <h3 style='margin:0; color: #2c3e50;'>🧠 Stress Level</h3>
                    <div style='display: flex; align-items: center; gap: 15px;'>
                        <div style='font-size: 32px; color: {stress_color};'>""" +
                        {"Low": "😊", "Moderate": "😐", "High": "😣", "Critical": "😡"}[fake_data['Stress Level']] +
                        f"""</div>
                        <div style='font-size: 24px; font-weight: bold; color: {stress_color};'>
                            {fake_data['Stress Level']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col7:
                risk_color = {"Low": "#2ecc71", "Moderate": "#f1c40f", "High": "#e67e22", "Critical": "#e74c3c"}[fake_data['Health Crisis Risk']]
                st.markdown(f"""
                <div class='dashboard-box'>
                    <h3 style='margin:0; color: #2c3e50;'>⚕️ Health Crisis Risk</h3>
                    <div style='display: flex; align-items: center; justify-content: space-between;'>
                        <div style='font-size: 32px; color: {risk_color};'>⚠️</div>
                        <div style='font-size: 24px; font-weight: bold; color: {risk_color};'>
                            {fake_data['Health Crisis Risk']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Process actions and notifications
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

        # Display Actions
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

        # Display Notifications
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
        
        time.sleep(5)
