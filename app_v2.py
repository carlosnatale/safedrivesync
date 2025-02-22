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
        background-size: 60%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .content-area {{
        position: absolute;
        top: 30%;
        left: 20%;
        width: 60%;
        height: 40%;
        background: none;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
    }}
    .indicator {{
        padding: 10px;
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        border-radius: 5px;
        margin: 5px;
        font-size: 12px;
        text-align: center;
    }}
    .normal-indicator {{
        padding: 10px;
        background-color: rgba(0, 128, 0, 0.6);
        color: white;
        border-radius: 5px;
        margin: 5px;
        font-size: 12px;
        text-align: center;
    }}
    .alert-box {{
        position: absolute;
        bottom: 5%;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(255, 0, 0, 0.9);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        width: 40%;
        text-align: center;
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

# Real-time data simulation loop
placeholder = st.empty()

for _ in range(100):  # Simulates 100 updates
    biometric_data = generate_biometric_data()
    
    with placeholder.container():
        st.markdown('<div class="content-area">', unsafe_allow_html=True)
        # Display biometric data
        for key, value in biometric_data.items():
            status = classify_risk(value) if key in ["Stress Level", "Fatigue Risk", "Health Crisis Risk"] else "Normal"
            style_class = "normal-indicator" if status == "Normal" else "indicator"
            st.markdown(f'<div class="{style_class}">{key}: {value}</div>', unsafe_allow_html=True)
        
        # Assess situations
        stress_status = classify_risk(biometric_data["Stress Level"])
        fatigue_status = classify_risk(biometric_data["Fatigue Risk"])
        health_crisis_status = classify_risk(biometric_data["Health Crisis Risk"])
        
        # Trigger responses
        handle_responses(stress_status, stress_responses, "Stress")
        handle_responses(fatigue_status, fatigue_responses, "Fatigue")
        handle_responses(health_crisis_status, health_crisis_responses, "Health Crisis")
        st.markdown('</div>', unsafe_allow_html=True)
    
    time.sleep(2)  # Update every 2 seconds

# Footer
st.markdown("---")
st.markdown("**SafeDrive Sync - Real-Time Driver Health Monitoring**")
