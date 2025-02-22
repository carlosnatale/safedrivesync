import streamlit as st
import random
import time
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

# CSS styling for background and messages
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{background_base64}');
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
    }}
    .title {{
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: white;
    }}
    .indicator {{
        padding: 20px;
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        border-radius: 10px;
        margin-bottom: 10px;
    }}
    .alert-box {{
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(255, 0, 0, 0.8);
        color: white;
        padding: 20px;
        border-radius: 10px;
        font-weight: bold;
        z-index: 1000;
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

# Vehicle response settings
responses = [
    "Send Notification", "Reduce Speed", "Play Calming Music",
    "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn",
    "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

# Sidebar configuration for user response settings
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

# Display title
st.markdown('<div class="title">SafeDrive Sync Real-Time Monitoring</div>', unsafe_allow_html=True)

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
    for response in responses_dict.get(status, []):
        if response == "Send Notification":
            message = dynamic_messages[situation].get(status, "All systems normal.")
            st.markdown(f'<div class="alert-box">{situation} - {status}: {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-box">{response} activated due to {situation} condition: {status}</div>', unsafe_allow_html=True)

# Real-time data simulation loop
placeholder = st.empty()

for _ in range(100):  # Simulates 100 updates
    biometric_data = generate_biometric_data()
    
    with placeholder.container():
        # Display biometric data
        st.markdown("### Biometric Data")
        cols = st.columns(3)
        for i, (key, value) in enumerate(biometric_data.items()):
            cols[i % 3].markdown(f'<div class="indicator">{key}: {value}</div>', unsafe_allow_html=True)
        
        # Assess situations
        stress_status = classify_risk(biometric_data["Stress Level"])
        fatigue_status = classify_risk(biometric_data["Fatigue Risk"])
        health_crisis_status = classify_risk(biometric_data["Health Crisis Risk"])
        
        # Trigger responses
        handle_responses(stress_status, stress_responses, "Stress")
        handle_responses(fatigue_status, fatigue_responses, "Fatigue")
        handle_responses(health_crisis_status, health_crisis_responses, "Health Crisis")
    
    time.sleep(2)  # Update every 2 seconds

# Footer
st.markdown("---")
st.markdown("**SafeDrive Sync - Real-Time Driver Health Monitoring**")
