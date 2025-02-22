import streamlit as st
import random
import time
from PIL import Image

# Load background image
background = Image.open('/mnt/data/infotainment - Copia.png')

# Set page configuration
st.set_page_config(page_title="SafeDrive Sync Simulator", layout="wide")

# CSS styling for background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('data:image/png;base64,{st.image(background, use_column_width=True)}');
        background-size: cover;
        background-position: center;
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
    "No Action", "Send Notification", "Reduce Speed", "Play Calming Music",
    "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn",
    "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

# Sidebar configuration for user response settings
st.sidebar.title("Vehicle Response Settings")
stress_response = st.sidebar.selectbox("Stress Response", responses)
fatigue_response = st.sidebar.selectbox("Fatigue Response", responses)
health_crisis_response = st.sidebar.selectbox("Health Crisis Response", responses)

# Display title
st.markdown('<div class="title">SafeDrive Sync Real-Time Monitoring</div>', unsafe_allow_html=True)

# Real-time data simulation loop
biometric_data = generate_biometric_data()

# Display biometric data
st.markdown("### Biometric Data")
cols = st.columns(3)
for i, (key, value) in enumerate(biometric_data.items()):
    cols[i % 3].markdown(f'<div class="indicator">{key}: {value}</div>', unsafe_allow_html=True)

# Assess situations
stress_status = classify_risk(biometric_data["Stress Level"])
fatigue_status = classify_risk(biometric_data["Fatigue Risk"])
health_crisis_status = classify_risk(biometric_data["Health Crisis Risk"])

# Function to handle vehicle responses
def handle_response(status, response, situation):
    if response == "No Action":
        return
    elif response == "Send Notification":
        messages = {
            "Stress": {
                "Moderate": "Moderate stress detected. Consider taking deep breaths.",
                "High": "High stress detected! Reduce distractions and focus on the road.",
                "Critical": "CRITICAL STRESS! Pull over safely and take a break."
            },
            "Fatigue": {
                "Moderate": "Moderate fatigue detected. Consider stretching or stopping soon.",
                "High": "High fatigue detected! Take a break immediately.",
                "Critical": "CRITICAL FATIGUE! Your reaction time is dangerously low. Stop now."
            },
            "Health Crisis": {
                "Moderate": "Mild health irregularity detected. Monitor your condition.",
                "High": "Significant health concern! Consider seeking medical attention.",
                "Critical": "EMERGENCY! Health crisis detected. Contact emergency services immediately."
            }
        }
        st.warning(messages[situation].get(status, "All normal."))
    else:
        st.info(f"{response} activated due to {situation} condition: {status}")

# Trigger responses
handle_response(stress_status, stress_response, "Stress")
handle_response(fatigue_status, fatigue_response, "Fatigue")
handle_response(health_crisis_status, health_crisis_response, "Health Crisis")

# Footer
st.markdown("---")
st.markdown("**SafeDrive Sync - Real-Time Driver Health Monitoring**")
