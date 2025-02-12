import streamlit as st
import pandas as pd
import numpy as np
import time

# Streamlit UI Enhancements - Modern Infotainment System
st.set_page_config(page_title="SafeDrive Sync", layout="wide")

# Custom CSS for Modern UI
st.markdown("""
    <style>
        body { background-color: #1a1a2e; color: #eaeaea; }
        .main { background: #16213e; color: white; padding: 20px; }
        .stButton>button { 
            border-radius: 8px; 
            padding: 12px 20px;
            background: linear-gradient(45deg, #0066ff, #00ccff);
            color: white; 
            font-weight: bold; 
            border: none; 
            transition: 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.1);
            background: linear-gradient(45deg, #0044cc, #0099cc);
        }
        .stDataFrame { 
            background-color: rgba(255, 255, 255, 0.1); 
            color: white; 
            border-radius: 12px; 
            padding: 10px; 
        }
        .stSidebar { background: #0f3460; color: white; }
        .dashboard-box { 
            padding: 20px; 
            border-radius: 15px; 
            background: rgba(255, 255, 255, 0.1); 
            border: 1px solid rgba(255, 255, 255, 0.2); 
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        }
        .stMultiSelect > div { border-radius: 8px; background: rgba(255, 255, 255, 0.1); padding: 5px; }
        .stDataFrame tbody tr { background: rgba(255, 255, 255, 0.1); color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 SafeDrive Sync - Next-Gen Infotainment System")

monitoring = st.toggle("Enable Real-Time Monitoring", value=True)

# Vehicle Response Settings
st.subheader("🚘 Configure Vehicle Actions")
levels = ['Low', 'Moderate', 'High', 'Critical']
actions = [
    "No Action", "Send Notification", "Reduce Speed", "Play Calming Music", "Turn On Air Conditioning", 
    "Adjust Seat Position", "Activate Horn", "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"
]

def action_multiselect(label, actions):
    return st.multiselect(f"{label}", actions, default=["Send Notification"], help="Select actions based on severity.")

col1, col2, col3 = st.columns(3)

for col, category, icon in zip([col1, col2, col3], ["Stress", "Fatigue", "Health Crisis"], ["🧘", "😴", "🚑"]):
    with col:
        st.subheader(f"{icon} {category} Actions")
        actions_dict = {level: action_multiselect(f"{category} {level}", actions) for level in levels}

data_placeholder = st.empty()
if monitoring:
    while True:
        fake_data = {
            'Heart Rate (bpm)': np.random.randint(60, 110),
            'HRV (ms)': np.random.randint(20, 80),
            'SpO2 (%)': np.random.randint(90, 100),
            'Blood Pressure (mmHg)': f"{np.random.randint(90, 140)}/{np.random.randint(60, 90)}",
            'Blood Sugar (mg/dL)': np.random.randint(70, 140),
            'Motion Intensity': np.random.randint(0, 10),
            'Stress Level': np.random.choice(levels),
            'Fatigue Risk': np.random.choice(levels),
            'Health Crisis Risk': np.random.choice(levels)
        }
        df = pd.DataFrame([fake_data])
        data_placeholder.dataframe(df, use_container_width=True)
        time.sleep(3)
