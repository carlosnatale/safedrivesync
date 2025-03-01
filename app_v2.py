import streamlit as st
import numpy as np
import time

# Streamlit Configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Mobile Optimization
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: white; }
        .health-card {
            background: white;
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            color: black;
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

# Session State Initialization
if 'health_data' not in st.session_state:
    st.session_state.health_data = None
    st.session_state.last_update = 0

def generate_health_data():
    """Generate fresh random health metrics"""
    levels = ['Low', 'Moderate', 'High', 'Critical']
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Blood Pressure': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'Blood Sugar': np.random.randint(70, 140),
        'Motion Intensity': np.random.randint(0, 10),
        'Stress Level': np.random.choice(levels),
        'Fatigue Risk': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
        'Health Crisis Risk': np.random.choice(levels, p=[0.57, 0.23, 0.1, 0.1])
    }

def update_metrics():
    """Force UI refresh with new data"""
    st.session_state.health_data = generate_health_data()
    st.session_state.last_update = time.time()

# Main App Interface
st.title("🚗 SafeDrive Sync - Health Dashboard")

# Auto-refresh control
monitoring_enabled = st.toggle("Enable Real-Time Monitoring", value=True)

# Update data every 5 seconds
if monitoring_enabled and (time.time() - st.session_state.last_update > 5):
    update_metrics()
    st.rerun()

# Initialize data if not exists
if st.session_state.health_data is None:
    update_metrics()

# Get current metrics
current_data = st.session_state.health_data

# Dashboard Layout
cols = st.columns(3)
with cols[0]:
    st.markdown(f"""
        <div class='health-card'>
            <div class='card-title'>❤️ Heart Rate</div>
            <div class='card-value'>{current_data['Heart Rate (bpm)']}</div>
            <div class='status-indicator' style='background: #e8f4ff; color: #007bff;'>bpm</div>
        </div>
    """, unsafe_allow_html=True, key=f"hr_{current_data['Heart Rate (bpm)']}")

with cols[1]:
    st.markdown(f"""
        <div class='health-card'>
            <div class='card-title'>📶 HRV</div>
            <div class='card-value'>{current_data['HRV (ms)']}</div>
            <div class='status-indicator' style='background: #fff5e6; color: #ff9900;'>ms</div>
        </div>
    """, unsafe_allow_html=True, key=f"hrv_{current_data['HRV (ms)']}")

with cols[2]:
    st.markdown(f"""
        <div class='health-card'>
            <div class='card-title'>🩸 SpO2</div>
            <div class='card-value'>{current_data['SpO2 (%)']}%</div>
            <div class='status-indicator' style='background: #e6ffe6; color: #00cc00;'>oxygen</div>
        </div>
    """, unsafe_allow_html=True, key=f"spo2_{current_data['SpO2 (%)']}")

# Second Row
cols2 = st.columns(2)
with cols2[0]:
    st.markdown(f"""
        <div class='health-card'>
            <div class='card-title'>🩺 Blood Pressure</div>
            <div class='card-value' style='font-size: 22px;'>{current_data['Blood Pressure']}</div>
            <div style='font-size: 12px; color: #666;'>mmHg</div>
        </div>
    """, unsafe_allow_html=True, key=f"bp_{current_data['Blood Pressure']}")

with cols2[1]:
    st.markdown(f"""
        <div class='health-card'>
            <div class='card-title'>🍬 Blood Sugar</div>
            <div class='card-value'>{current_data['Blood Sugar']}</div>
            <div class='status-indicator' style='background: #ffe6e6; color: #ff3333;'>mg/dL</div>
        </div>
    """, unsafe_allow_html=True, key=f"sugar_{current_data['Blood Sugar']}")

# Risk Indicators
risk_colors = {
    'Low': '#00cc00',
    'Moderate': '#ff9900',
    'High': '#ff3333',
    'Critical': '#cc0000'
}

st.markdown(f"""
    <div class='health-card'>
        <div class='card-title'>⚠️ Risk Indicators</div>
        <div style='display: grid; gap: 12px; margin-top: 10px;'>
            <div style='display: flex; justify-content: space-between;'>
                <span>Stress Level</span>
                <span style='color: {risk_colors[current_data['Stress Level']]};'>
                    {current_data['Stress Level']}
                </span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>Fatigue Risk</span>
                <span style='color: {risk_colors[current_data['Fatigue Risk']]};'>
                    {current_data['Fatigue Risk']}
                </span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>Health Crisis</span>
                <span style='color: {risk_colors[current_data['Health Crisis Risk']]};'>
                    {current_data['Health Crisis Risk']}
                </span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True, key=f"risks_{current_data['Stress Level']}{current_data['Fatigue Risk']}{current_data['Health Crisis Risk']}")

# Motion Intensity
st.markdown(f"""
    <div class='health-card'>
        <div class='card-title'>🏃 Motion Intensity</div>
        <div style='display: flex; align-items: center; gap: 10px; margin-top: 8px;'>
            <div style='flex-grow: 1; height: 8px; background: #f0f0f0; border-radius: 4px;'>
                <div style='width: {current_data['Motion Intensity']*10}%; 
                    height: 100%; 
                    background: #007bff; 
                    border-radius: 4px;'>
                </div>
            </div>
            <div style='font-size: 16px; font-weight: bold;'>
                {current_data['Motion Intensity']}/10
            </div>
        </div>
    </div>
""", unsafe_allow_html=True, key=f"motion_{current_data['Motion Intensity']}")

# Update timestamp
st.caption(f"Last update: {time.strftime('%H:%M:%S', time.localtime(st.session_state.last_update))}")
