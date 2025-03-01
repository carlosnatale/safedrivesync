import streamlit as st
import numpy as np
import time

# Streamlit Configuration
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Mobile Optimization
st.markdown("""
    <style>
        .main { background-color: #3a3a3a; color: white; }
        .health-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            padding: 10px;
        }
        .health-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            color: black;
        }
        .card-title {
            font-size: 16px;
            color: #666;
            margin-bottom: 12px;
        }
        .card-value {
            font-size: 28px;
            font-weight: bold;
            color: #007bff;
        }
        .status-indicator {
            font-size: 14px;
            padding: 6px 12px;
            border-radius: 20px;
            display: inline-block;
        }
        @media (max-width: 600px) {
            .health-grid { grid-template-columns: 1fr; }
            .card-value { font-size: 24px; }
            .card-title { font-size: 14px; }
        }
    </style>
""", unsafe_allow_html=True)

# Session State Management
if 'health_data' not in st.session_state:
    st.session_state.health_data = None
    st.session_state.last_update = 0

def generate_health_data():
    """Generate fresh random health metrics with realistic distributions"""
    levels = ['Low', 'Moderate', 'High', 'Critical']
    return {
        'heart_rate': np.random.randint(60, 110),
        'hrv': np.random.randint(20, 80),
        'spo2': np.random.randint(90, 100),
        'blood_pressure': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
        'blood_sugar': np.random.randint(70, 140),
        'motion': np.random.randint(0, 10),
        'stress': np.random.choice(levels, p=[0.4, 0.3, 0.2, 0.1]),
        'fatigue': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
        'health_risk': np.random.choice(levels, p=[0.6, 0.25, 0.1, 0.05])
    }

def create_metric_card(title, value, unit, color):
    """Helper function to create consistent metric cards"""
    return f"""
        <div class="health-card">
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            <div class="status-indicator" style="background: {color[0]}; color: {color[1]};">{unit}</div>
        </div>
    """

# Main App Interface
st.title("🚗 SafeDrive Sync - Real-time Health Dashboard")

# Control Panel
with st.sidebar:
    st.header("Settings")
    monitoring_enabled = st.toggle("Enable Monitoring", True)
    update_btn = st.button("Force Refresh")

# Data Management
if update_btn or (monitoring_enabled and (time.time() - st.session_state.last_update > 5)):
    st.session_state.health_data = generate_health_data()
    st.session_state.last_update = time.time()
    if monitoring_enabled:
        st.rerun()

if st.session_state.health_data is None:
    st.session_state.health_data = generate_health_data()

# Get current data
data = st.session_state.health_data

# Main Dashboard Grid
with st.container():
    st.markdown('<div class="health-grid">', unsafe_allow_html=True)
    
    # Vital Signs
    st.markdown(create_metric_card(
        "❤️ Heart Rate", 
        data['heart_rate'], 
        "bpm", 
        ("#e8f4ff", "#007bff")
    ), unsafe_allow_html=True)
    
    st.markdown(create_metric_card(
        "📶 HRV", 
        data['hrv'], 
        "ms", 
        ("#fff5e6", "#ff9900")
    ), unsafe_allow_html=True)
    
    st.markdown(create_metric_card(
        "🩸 SpO2", 
        f"{data['spo2']}%", 
        "oxygen", 
        ("#e6ffe6", "#00cc00")
    ), unsafe_allow_html=True)
    
    # Blood Metrics
    st.markdown(create_metric_card(
        "🩺 Blood Pressure", 
        data['blood_pressure'], 
        "mmHg", 
        ("#f8f9fa", "#6c757d")
    ), unsafe_allow_html=True)
    
    st.markdown(create_metric_card(
        "🍬 Blood Sugar", 
        data['blood_sugar'], 
        "mg/dL", 
        ("#ffe6e6", "#ff3333")
    ), unsafe_allow_html=True)
    
    # Risk Indicators
    risk_colors = {
        'Low': ("#e6ffe6", "#00cc00"),
        'Moderate': ("#fff5e6", "#ff9900"),
        'High': ("#ffe6e6", "#ff3333"),
        'Critical': ("#ffebee", "#cc0000")
    }
    
    st.markdown(f"""
        <div class="health-card">
            <div class="card-title">⚠️ Risk Analysis</div>
            <div style="display: grid; gap: 15px; margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Stress Level</span>
                    <div style="background: {risk_colors[data['stress']][0]}; 
                        color: {risk_colors[data['stress']][1]};
                        padding: 6px 12px;
                        border-radius: 20px;">
                        {data['stress']}
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Fatigue Risk</span>
                    <div style="background: {risk_colors[data['fatigue']][0]}; 
                        color: {risk_colors[data['fatigue']][1]};
                        padding: 6px 12px;
                        border-radius: 20px;">
                        {data['fatigue']}
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Health Crisis</span>
                    <div style="background: {risk_colors[data['health_risk']][0]}; 
                        color: {risk_colors[data['health_risk']][1]};
                        padding: 6px 12px;
                        border-radius: 20px;">
                        {data['health_risk']}
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Motion Intensity
    st.markdown(f"""
        <div class="health-card">
            <div class="card-title">🏃 Motion Intensity</div>
            <div style="margin-top: 15px;">
                <div style="height: 10px; background: #f0f0f0; border-radius: 5px;">
                    <div style="width: {data['motion']*10}%; 
                        height: 100%; 
                        background: #007bff; 
                        border-radius: 5px;
                        transition: width 0.5s ease;">
                    </div>
                </div>
                <div style="text-align: center; margin-top: 10px; font-weight: bold;">
                    {data['motion']}/10
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Status Footer
st.caption(f"Last update: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st.session_state.last_update))}")
