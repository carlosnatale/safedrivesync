import streamlit as st
import random
import time
import pandas as pd
from PIL import Image
import base64

# Function to load and encode the background image
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Load and encode background image
background_base64 = get_base64_image('infotainment - Copia.png')

# Set page configuration
st.set_page_config(page_title="SafeDrive Sync Simulator", layout="wide")

# Vehicle Response Settings
st.sidebar.title("Vehicle Response Settings")
responses = [
    "Send Notification", "Reduce Speed", "Play Calming Music",
    "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn",
    "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

stress_responses = {
    "Moderate": st.sidebar.multiselect("Stress Response - Moderate", responses),
    "High": st.sidebar.multiselect("Stress Response - High", responses),
    "Critical": st.sidebar.multiselect("Stress Response - Critical", responses)
}
fatigue_responses = {
    "Moderate": st.sidebar.multiselect("Fatigue Response - Moderate", responses),
    "High": st.sidebar.multiselect("Fatigue Response - High", responses),
    "Critical": st.sidebar.multiselect("Fatigue Response - Critical", responses)
}
health_crisis_responses = {
    "Moderate": st.sidebar.multiselect("Health Crisis Response - Moderate", responses),
    "High": st.sidebar.multiselect("Health Crisis Response - High", responses),
    "Critical": st.sidebar.multiselect("Health Crisis Response - Critical", responses)
}

# CSS styling for background and table display
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{background_base64}');
        background-size: 65%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: #3a3a3a;
    }}
    .alert-box {{
        margin-top: 70px;
        background-color: rgba(255, 0, 0, 0.9);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        width: 50%;
        text-align: center;
        overflow-wrap: break-word;
        margin-left: calc(1cm);
        margin-right: auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Function to generate simulated biometric data
def generate_biometric_data():
    return {
        "Heart Rate (bpm)": random.randint(60, 140),
        "HRV (ms)": random.randint(20, 100),
        "SpO2 (%)": random.randint(85, 100),
        "Blood Sugar (mg/dL)": random.randint(70, 180),
        "Motion Intensity": random.randint(0, 10),
        "Stress Level": random.randint(30, 100),
        "Fatigue Risk": random.randint(30, 100),
        "Health Crisis Risk": random.randint(30, 100)
    }

# Function to classify conditions
def classify_risk(value, metric):
    if metric in ["Stress Level", "Fatigue Risk", "Health Crisis Risk"]:
        if value <= 39:
            return "Normal"
        elif value <= 59:
            return "Moderate"
        elif value <= 79:
            return "High"
        else:
            return "Critical"
    elif metric == "Heart Rate (bpm)":
        if value <= 100:
            return "Normal"
        elif value <= 120:
            return "Moderate"
        elif value <= 140:
            return "High"
        else:
            return "Critical"
    elif metric == "HRV (ms)":
        if value > 50:
            return "Normal"
        elif value > 35:
            return "Moderate"
        elif value > 20:
            return "High"
        else:
            return "Critical"
    elif metric == "SpO2 (%)":
        if value >= 95:
            return "Normal"
        elif value >= 90:
            return "Moderate"
        elif value >= 85:
            return "High"
        else:
            return "Critical"
    elif metric == "Blood Sugar (mg/dL)":
        if value <= 140:
            return "Normal"
        elif value <= 180:
            return "Moderate"
        elif value <= 250:
            return "High"
        else:
            return "Critical"
    elif metric == "Motion Intensity":
        if value <= 3:
            return "Normal"
        elif value <= 6:
            return "Moderate"
        elif value <= 8:
            return "High"
        else:
            return "Critical"
    else:
        return "Normal"

# Function to handle vehicle responses
def handle_responses(situation, status, response_dict):
    dynamic_messages = {
        "Moderate": "Moderate level detected. Please be cautious.",
        "High": "High level detected! Take action immediately.",
        "Critical": "CRITICAL! Immediate intervention required."
    }
    if status != "Normal" and response_dict.get(status, []):
        st.markdown(f'<div class="alert-box">Notification: {situation} - {status}: {dynamic_messages[status]}</div>', unsafe_allow_html=True)
        for response in response_dict.get(status, []):
            if response != "Send Notification":
                st.markdown(f'<div class="alert-box">Action Triggered: {response}</div>', unsafe_allow_html=True)

# Main simulation loop
placeholder = st.empty()
for _ in range(100):  # Simulate 100 updates
    biometric_data = generate_biometric_data()
    data_table = pd.DataFrame([biometric_data])
    with placeholder.container():
        st.markdown('<div style="margin-top: 1cm;"><h2>Real-Time Driver Health Data</h2></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top: 1cm;">', unsafe_allow_html=True)
        st.dataframe(data_table.style.set_properties(**{
            'background-color': '#3a3a3a',
            'color': '#d3d3d3',
            'border-color': '#3a3a3a'
        }).set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#3a3a3a'), ('color', '#d3d3d3')]},
            {'selector': 'thead th', 'props': [('background-color', '#3a3a3a'), ('color', '#d3d3d3')]}
        ]).highlight_max(axis=1, color='red').highlight_min(axis=1, color='green'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Classify biometric data and prioritize notifications
        stress_status = classify_risk(biometric_data["Stress Level"], "Stress Level")
        fatigue_status = classify_risk(biometric_data["Fatigue Risk"], "Fatigue Risk")
        health_crisis_status = classify_risk(biometric_data["Health Crisis Risk"], "Health Crisis Risk")
        
        # Prioritize: Health Crisis > Fatigue > Stress
        if health_crisis_status != "Normal":
            handle_responses("Health Crisis", health_crisis_status, health_crisis_responses)
        elif fatigue_status != "Normal":
            handle_responses("Fatigue", fatigue_status, fatigue_responses)
        elif stress_status != "Normal":
            handle_responses("Stress", stress_status, stress_responses)
        else:
            st.markdown('<div class="alert-box" style="background-color: rgba(0, 128, 0, 0.9);">Normal Condition</div>', unsafe_allow_html=True)
    time.sleep(10)  # Update every 10 seconds
