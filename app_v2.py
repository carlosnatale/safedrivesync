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

# Define response options
responses = [
    "Send Notification", "Reduce Speed", "Play Calming Music",
    "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn",
    "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

# Sidebar response configuration
st.sidebar.title("Vehicle Response Settings")
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
        background-size: 50%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: #3a3a3a;
    }}
    .data-area {{
        position: absolute;
        top: 50%;
        left: 20%;
        width: 60%;
        height: auto;
        background: rgba(58, 58, 58, 0.9);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }}
    .alert-box {{
        margin-top: 10px;
        background-color: rgba(255, 0, 0, 0.9);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        width: 70%;
        text-align: center;
        overflow-wrap: break-word;
        margin-left: auto;
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
        "Blood Pressure (mmHg)": f"{random.randint(90, 140)}/{random.randint(60, 90)}",
        "Blood Sugar (mg/dL)": random.randint(70, 180),
        "Motion Intensity": random.randint(0, 10),
        "Stress Level": random.randint(0, 100),
        "Fatigue Risk": random.randint(0, 100),
        "Health Crisis Risk": random.randint(0, 100)
    }

# Function to classify conditions
def classify_risk(value):
    if value < 25:
        return "Normal"
    elif value < 50:
        return "Moderate"
    elif value < 75:
        return "High"
    else:
        return "Critical"

# Function to handle vehicle responses
def handle_responses(status, responses_dict, situation):
    dynamic_messages = {
        "Stress": {
            "Moderate": "You seem a bit tense. Take a deep breath and stay focused.",
            "High": "High stress detected! It's time to minimize distractions.",
            "Critical": "WARNING! Extreme stress detected. Please stop safely and relax."
        },
        "Fatigue": {
            "Moderate": "Feeling a bit tired? Stretch when possible.",
            "High": "High fatigue detected! A break is necessary.",
            "Critical": "CRITICAL FATIGUE! You must stop immediately for safety."
        },
        "Health Crisis": {
            "Moderate": "Minor irregularities detected. Stay cautious.",
            "High": "Health concern detected! Seek attention soon.",
            "Critical": "EMERGENCY! Contacting emergency services now."
        }
    }
    if status != "Normal":
        for response in responses_dict.get(status, []):
            if response == "Send Notification":
                message = dynamic_messages[situation].get(status, "All systems normal.")
                st.markdown(f'<div class="alert-box">{situation} - {status}: {message}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-box">{response} activated due to {situation} condition: {status}</div>', unsafe_allow_html=True)

# Main loop for real-time simulation
placeholder = st.empty()

for _ in range(100):  # Simulate 100 updates
    biometric_data = generate_biometric_data()
    numeric_data = {k: v for k, v in biometric_data.items() if isinstance(v, (int, float))}
    data_table = pd.DataFrame([numeric_data])
    with placeholder.container():
        st.markdown('<div class="data-area">', unsafe_allow_html=True)
        st.subheader("Real-Time Driver Health Data")
        st.dataframe(data_table.style.highlight_max(axis=1, color='red').highlight_min(axis=1, color='green'))
        # Check and handle alerts
        stress_status = classify_risk(biometric_data["Stress Level"])
        fatigue_status = classify_risk(biometric_data["Fatigue Risk"])
        health_crisis_status = classify_risk(biometric_data["Health Crisis Risk"])
        handle_responses(stress_status, stress_responses, "Stress")
        handle_responses(fatigue_status, fatigue_responses, "Fatigue")
        handle_responses(health_crisis_status, health_crisis_responses, "Health Crisis")
        st.markdown('</div>', unsafe_allow_html=True)
    time.sleep(2)  # Update every 2 seconds
