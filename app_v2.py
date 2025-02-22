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
        background-size: 65%;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: #3a3a3a;
    }}
    .data-area {{
        position: absolute;
        top: 65%; /* Lowered by additional 10% */
        left: 30%;
        width: 40%;
        height: auto;
        background: rgba(58, 58, 58, 0.9);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }}
    .alert-box {{
        margin-top: 20px; /* Increased spacing below data */
        background-color: rgba(255, 0, 0, 0.9);
        color: white;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        width: 50%;
        text-align: center;
        overflow-wrap: break-word;
        margin-left: auto;
        margin-right: auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
