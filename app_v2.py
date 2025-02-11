import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Constants
COLORS = {
    "primary": "#1e88e5",
    "secondary": "#263238",
    "success": "#43a047",
    "warning": "#ffb300",
    "danger": "#e53935",
    "background": "#0d1117",
    "gauge": "#2d3436"
}

# Configure page
st.set_page_config(
    page_title="SafeDrive Dashboard",
    layout="wide",
    page_icon="🚘"
)

# Custom CSS for vehicle dashboard
st.markdown(f"""
    <style>
        body {{ background-color: {COLORS['background']}; color: white; }}
        .main {{ padding: 2rem; }}
        .dashboard-header {{ 
            background: {COLORS['secondary']};
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }}
        .vital-card {{
            background: {COLORS['secondary']};
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem;
            border-left: 5px solid {COLORS['primary']};
        }}
        .critical-alert {{
            background: {COLORS['danger']} !important;
            animation: pulse 1.5s infinite;
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        .metric-label {{ color: #90a4ae; font-size: 1rem; }}
        .metric-value {{ color: white; font-size: 2rem; font-weight: bold; }}
        .progress-bar {{
            height: 10px;
            background: {COLORS['secondary']};
            border-radius: 5px;
            margin: 0.5rem 0;
        }}
        .progress-fill {{ 
            height: 100%;
            border-radius: 5px;
            transition: width 0.5s ease;
        }}
    </style>
""", unsafe_allow_html=True)

# Simulated vehicle data
def generate_vehicle_data():
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "speed": np.random.randint(0, 120),
        "rpm": np.random.randint(1000, 4000),
        "fuel": np.random.uniform(10, 60),
        "engine_temp": np.random.randint(80, 110),
        "driver_heart_rate": np.random.randint(60, 100),
        "driver_stress": np.random.randint(0, 100),
        "driver_fatigue": np.random.randint(0, 100),
        "lane_deviation": np.random.choice([True, False], p=[0.1, 0.9]),
        "forward_collision_warning": np.random.choice([True, False], p=[0.05, 0.95])
    }

# Dashboard Layout
st.title("🚘 SafeDrive Vehicle Dashboard")

# Alert System
alert_container = st.empty()

# Main Dashboard Grid
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    st.markdown("### Driver Status")
    driver_container = st.container()
    
    st.markdown("### Vehicle Health")
    vehicle_container = st.container()

with col2:
    st.markdown("### Critical Metrics")
    with st.container():
        st.markdown('<div class="vital-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Current Speed</div>', unsafe_allow_html=True)
        speed_display = st.markdown('<div class="metric-value">0</div> km/h', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="vital-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Engine RPM</div>', unsafe_allow_html=True)
        rpm_display = st.markdown('<div class="metric-value">0</div> RPM', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown("### Environment")
    env_container = st.container()
    
    st.markdown("### Emergency Protocols")
    emergency_container = st.container()

# Data simulation and update
while True:
    data = generate_vehicle_data()
    
    # Update alerts
    alerts = []
    if data['forward_collision_warning']:
        alerts.append(f"🚨 **Forward Collision Warning**: Maintain safe distance!")
    if data['lane_deviation']:
        alerts.append("⚠️ **Lane Departure**: Correct steering position")
    if data['driver_fatigue'] > 70:
        alerts.append("😴 **Driver Fatigue Detected**: Suggest rest break")
    if data['driver_stress'] > 80:
        alerts.append("💢 **High Stress Level**: Activating comfort systems")
    
    alert_content = ""
    if alerts:
        alert_content = f"""
        <div class="critical-alert">
            {'<br>'.join(alerts)}
        </div>
        """
    alert_container.markdown(alert_content, unsafe_allow_html=True)
    
    # Update driver status
    with driver_container:
        cols = st.columns(2)
        with cols[0]:
            st.markdown(f"""
                <div class="vital-card">
                    <div class="metric-label">Heart Rate</div>
                    <div class="metric-value">{data['driver_heart_rate']} BPM</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {data['driver_heart_rate']/2}%; background: {COLORS['primary']};"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            stress_color = COLORS['warning'] if data['driver_stress'] > 50 else COLORS['success']
            st.markdown(f"""
                <div class="vital-card">
                    <div class="metric-label">Stress Level</div>
                    <div class="metric-value">{data['driver_stress']}%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {data['driver_stress']}%; background: {stress_color};"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Update vehicle metrics
    speed_display.markdown(f'<div class="metric-value">{data["speed"]}</div> km/h', unsafe_allow_html=True)
    rpm_display.markdown(f'<div class="metric-value">{data["rpm"]}</div> RPM', unsafe_allow_html=True)
    
    # Update vehicle health
    with vehicle_container:
        cols = st.columns(2)
        with cols[0]:
            st.markdown(f"""
                <div class="vital-card">
                    <div class="metric-label">Fuel Level</div>
                    <div class="metric-value">{data['fuel']:.1f} L</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {(data['fuel']/60)*100}%; background: {COLORS['success']};"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            temp_color = COLORS['danger'] if data['engine_temp'] > 100 else COLORS['success']
            st.markdown(f"""
                <div class="vital-card">
                    <div class="metric-label">Engine Temp</div>
                    <div class="metric-value">{data['engine_temp']}°C</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {(data['engine_temp']-80)/30*100}%; background: {temp_color};"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Update emergency protocols
    with emergency_container:
        if any([data['forward_collision_warning'], data['driver_fatigue'] > 90]):
            st.button("🆘 EMERGENCY STOP", type="primary", use_container_width=True)
            st.button("🚑 Call Emergency Services", use_container_width=True)
        else:
            st.button("🔊 Sound Horn", use_container_width=True)
            st.button("💡 Flash Lights", use_container_width=True)
    
    time.sleep(1)
