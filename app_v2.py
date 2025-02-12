import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go

# Streamlit UI Configurations
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Sporty Dashboard Look
st.markdown("""
    <style>
        .main { background-color: #121212; color: white; }
        .stButton>button { border-radius: 10px; padding: 12px; background: #ff0000; color: white; border: none; font-weight: bold; }
        .stDataFrame { background-color: black; color: white; border-radius: 10px; padding: 10px; }
        .dashboard-box { flex: 1; padding: 15px; border-radius: 10px; background: #1e1e1e; margin: 10px; border: 2px solid #ff0000; text-align: center; color: white; }
    </style>
""", unsafe_allow_html=True)

# Function to generate fake telemetry data
def generate_fake_data():
    return {
        'Speed (km/h)': np.random.randint(60, 240),
        'RPM': np.random.randint(1000, 8000),
        'Power (%)': np.random.randint(10, 100),
        'Torque (%)': np.random.randint(10, 100),
        'Lap Time': round(np.random.uniform(1.20, 1.45), 3),
        'Best Lap': 1.268,
        'Difference': round(np.random.uniform(-0.05, 0.05), 3)
    }

st.title("🏎️ SafeDrive Sync - Performance Dashboard")

# Layout for Speedometer and Performance Data
col1, col2 = st.columns([2, 1])

with col1:
    data_placeholder = st.empty()

    # Live Data Updates
    while True:
        fake_data = generate_fake_data()
        
        # Speedometer Gauge
        speedometer = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fake_data['Speed (km/h)'],
            title={'text': "Speed (km/h)", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 250]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 100], 'color': "gray"},
                    {'range': [100, 180], 'color': "yellow"},
                    {'range': [180, 250], 'color': "red"}
                ],
            }
        ))
        
        # RPM Gauge
        rpm_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fake_data['RPM'],
            title={'text': "RPM", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 8000]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [0, 3000], 'color': "gray"},
                    {'range': [3000, 6000], 'color': "yellow"},
                    {'range': [6000, 8000], 'color': "red"}
                ],
            }
        ))
        
        st.plotly_chart(speedometer, use_container_width=True)
        st.plotly_chart(rpm_gauge, use_container_width=True)
        
        time.sleep(2)

with col2:
    st.subheader("Performance Metrics")
    
    power = go.Figure(go.Indicator(
        mode="gauge+number",
        value=fake_data['Power (%)'],
        title={'text': "Power (%)", 'font': {'size': 20}},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "red"}}
    ))
    
    torque = go.Figure(go.Indicator(
        mode="gauge+number",
        value=fake_data['Torque (%)'],
        title={'text': "Torque (%)", 'font': {'size': 20}},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "red"}}
    ))
    
    st.plotly_chart(power, use_container_width=True)
    st.plotly_chart(torque, use_container_width=True)
    
    st.subheader("Lap Timing")
    st.markdown(f"**Best Lap:** {fake_data['Best Lap']}s")
    st.markdown(f"**Current Lap:** {fake_data['Lap Time']}s")
    st.markdown(f"**Difference:** {fake_data['Difference']}s")
    
    time.sleep(2)
