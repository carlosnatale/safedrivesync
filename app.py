import streamlit as st
import pandas as pd
import numpy as np
import time

# Simulate real-time biometric data generation
def generate_fake_data():
    return {
        'Heart Rate (bpm)': np.random.randint(60, 110),
        'HRV (ms)': np.random.randint(20, 80),
        'SpO2 (%)': np.random.randint(90, 100),
        'Motion Intensity': np.random.randint(0, 10),
        'Fatigue Risk': np.random.choice(['Low', 'Moderate', 'High'], p=[0.6, 0.3, 0.1])
    }

# Streamlit UI
st.title("🚗 SafeDrive Sync - Driver Fatigue Monitor")

st.sidebar.header("Settings")
monitoring = st.sidebar.checkbox("Enable Real-Time Monitoring", value=True)

if monitoring:
    st.subheader("📊 Real-Time Driver Health Data")
    placeholder = st.empty()
    
    while True:
        fake_data = generate_fake_data()
        df = pd.DataFrame([fake_data])
        
        # Display data
        placeholder.dataframe(df)
        
        # Fatigue alert
        if fake_data['Fatigue Risk'] == 'High':
            st.error("🚨 High Fatigue Risk! Take a break immediately.")
        elif fake_data['Fatigue Risk'] == 'Moderate':
            st.warning("⚠️ Moderate Fatigue Detected. Consider resting soon.")
        
        time.sleep(3)  # Simulate real-time update

else:
    st.write("Monitoring is disabled. Enable it from the sidebar.")

# Post-trip Summary Button
if st.button("📉 Generate Trip Summary"):
    summary_data = {
        'Average Heart Rate': np.random.randint(70, 100),
        'Average HRV': np.random.randint(30, 70),
        'Average SpO2': np.random.randint(92, 99),
        'Fatigue Events Detected': np.random.randint(0, 5)
    }
    st.subheader("🔍 Trip Summary")
    st.json(summary_data)
    
    if summary_data['Fatigue Events Detected'] > 3:
        st.error("🚨 Fatigue detected multiple times! Reduce driving hours.")
    elif summary_data['Fatigue Events Detected'] > 0:
        st.warning("⚠️ Fatigue incidents occurred. Consider reviewing sleep patterns.")
    else:
        st.success("✅ No fatigue events detected. Safe driving!")
