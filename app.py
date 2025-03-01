import streamlit as st
import numpy as np
import time

# Streamlit Configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Mobile Optimization
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: white; }
        .stAlert { font-size: 16px; }
        .stButton>button { border-radius: 8px; padding: 10px; background: #007bff; color: white; border: none; }
        .dashboard-container { display: flex; justify-content: space-between; padding: 10px; gap: 20px; }
        .dashboard-box { flex: 1; padding: 15px; border-radius: 10px; background: #ffffff; margin: 10px; border: 2px solid #ced4da; text-align: left; }
        .health-card {
            background: white;
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .card-title {
            font-size: 14px;
            color: #666;
            margin-bottom: 8px;
        }
        .card-value {
            font-size: 24px;
            font-weight: bold;
            color: #007bff;
        }
        .status-indicator {
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 10px;
            display: inline-block;
        }
        @media (max-width: 600px) {
            .card-value { font-size: 20px; }
            .card-title { font-size: 13px; }
        }
    </style>
""", unsafe_allow_html=True)

# Functions ================================================================

def action_multiselect(label, actions, category, level):
    return st.multiselect(
        f"{label}", 
        actions, 
        default=["Send Notification"], 
        key=f"{category}_{level}"
    )

def generate_notification(category, level):
    messages = {
        "Stress": {
            "Low": "🟢 Low stress detected",
            "Moderate": "🟠 Moderate stress detected. Consider taking deep breaths.",
            "High": "🔴 High stress detected! Reduce distractions and focus on the road.",
            "Critical": "🚨 CRITICAL STRESS! Pull over safely and take a break."
        },
        "Fatigue": {
            "Low": "🟢 Low fatigue detected",
            "Moderate": "🟠 Moderate fatigue detected. Consider stretching or stopping soon.",
            "High": "🔴 High fatigue detected! Take a break immediately.",
            "Critical": "🚨 CRITICAL FATIGUE! Your reaction time is dangerously low. Stop now."
        },
        "Health Crisis": {
            "Low": "🟢 Mild health irregularity detected. Continue monitoring.",
            "Moderate": "🟠 Significant health concern! Consider seeking medical attention.",
            "High": "🔴 Severe health crisis developing! Pull over immediately.",
            "Critical": "🚨 EMERGENCY! Health crisis detected. Contact emergency services now."
        }
    }
    return messages[category][level]

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

# UI Components ============================================================

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

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("🧘 Stress Actions")
    stress_actions = {level: action_multiselect(f"Stress {level}", actions, "stress", level) for level in levels}

with col2:
    st.subheader("😴 Fatigue Actions")
    fatigue_actions = {level: action_multiselect(f"Fatigue {level}", actions, "fatigue", level) for level in levels}

with col3:
    st.subheader("🚑 Health Crisis Actions")
    health_crisis_actions = {level: action_multiselect(f"Health Crisis {level}", actions, "health", level) for level in levels}

# Main Dashboard ===========================================================

st.subheader("📊 Real-Time Driver Health Data")

# Initialize session state
if 'fake_data' not in st.session_state:
    st.session_state.fake_data = generate_fake_data()
    st.session_state.last_update = time.time()

# Update data every 3 seconds if monitoring is enabled
if monitoring and (time.time() - st.session_state.last_update > 3):
    st.session_state.fake_data = generate_fake_data()
    st.session_state.last_update = time.time()
    st.rerun()

fake_data = st.session_state.fake_data

# Display health metrics
with st.container():
    # Vital Signs Row
    cols = st.columns([1,1,1])
    with cols[0]:
        st.markdown(f"""
            <div class='health-card'>
                <div class='card-title'>❤️ Heart Rate</div>
                <div class='card-value'>{fake_data['Heart Rate (bpm)']}</div>
                <div class='status-indicator' style='background: #e8f4ff; color: #007bff;'>bpm</div>
            </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown(f"""
            <div class='health-card'>
                <div class='card-title'>📶 HRV</div>
                <div class='card-value'>{fake_data['HRV (ms)']}</div>
                <div class='status-indicator' style='background: #fff5e6; color: #ff9900;'>ms</div>
            </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown(f"""
            <div class='health-card'>
                <div class='card-title'>🩸 SpO2</div>
                <div class='card-value'>{fake_data['SpO2 (%)']}%</div>
                <div class='status-indicator' style='background: #e6ffe6; color: #00cc00;'>oxygen</div>
            </div>
        """, unsafe_allow_html=True)

    # Blood Pressure & Sugar Row
    bp, sugar = st.columns([2,1])
    with bp:
        st.markdown(f"""
            <div class='health-card'>
                <div class='card-title'>🩺 Blood Pressure</div>
                <div class='card-value' style='font-size: 22px;'>{fake_data['Blood Pressure']}</div>
                <div style='font-size: 12px; color: #666;'>mmHg</div>
            </div>
        """, unsafe_allow_html=True)
    
    with sugar:
        st.markdown(f"""
            <div class='health-card'>
                <div class='card-title'>🍬 Blood Sugar</div>
                <div class='card-value'>{fake_data['Blood Sugar']}</div>
                <div class='status-indicator' style='background: #ffe6e6; color: #ff3333;'>mg/dL</div>
            </div>
        """, unsafe_allow_html=True)

    # Risk Indicators
    stress_color = {"Low": "#00cc00", "Moderate": "#ff9900", "High": "#ff3333", "Critical": "#cc0000"}.get(fake_data['Stress Level'], "#666")
    fatigue_color = {"Low": "#00cc00", "Moderate": "#ff9900", "High": "#ff3333", "Critical": "#cc0000"}.get(fake_data['Fatigue Risk'], "#666")
    
    st.markdown(f"""
        <div class='health-card'>
            <div class='card-title'>⚠️ Risk Indicators</div>
            <div style='display: grid; gap: 12px; margin-top: 10px;'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span>Stress Level</span>
                    <span style='color: {stress_color}; font-weight: bold;'>{fake_data['Stress Level']}</span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span>Fatigue Risk</span>
                    <span style='color: {fatigue_color}; font-weight: bold;'>{fake_data['Fatigue Risk']}</span>
                </div>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span>Health Crisis</span>
                    <span style='color: #cc0000; font-weight: bold;'>{fake_data['Health Crisis Risk']}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Motion Intensity
    st.markdown(f"""
        <div class='health-card'>
            <div class='card-title'>🏃 Motion Intensity</div>
            <div style='display: flex; align-items: center; gap: 10px; margin-top: 8px;'>
                <div style='flex-grow: 1; height: 8px; background: #f0f0f0; border-radius: 4px;'>
                    <div style='width: {fake_data['Motion Intensity']*10}%; height: 100%; background: #007bff; border-radius: 4px;'></div>
                </div>
                <div style='font-size: 16px; font-weight: bold;'>{fake_data['Motion Intensity']}/10</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Handle actions and notifications
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
            notifications.append(generate_notification(category, current_level))
        else:
            actions_taken.append(f"🚗 {action} activated due to {category} ({current_level})")

# Display notifications and actions
with st.container():
    if notifications:
        st.markdown("<div class='dashboard-box'><b>📢 Notifications:</b><br>" + "<br>".join(notifications) + "</div>", unsafe_allow_html=True)
    
    if actions_taken:
        st.markdown("<div class='dashboard-box'><b>🚘 Vehicle Actions Taken:</b><br>" + "<br>".join(actions_taken) + "</div>", unsafe_allow_html=True)
