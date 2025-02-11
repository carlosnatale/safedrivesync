import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# Constants
CONFIG = {
    "page_title": "SafeDrive Sync",
    "layout": "wide",
    "metrics_update_interval": 3,
    "data_history_length": 20,
    "colors": {
        "primary": "#007bff",
        "secondary": "#6c757d",
        "success": "#28a745",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "info": "#17a2b8"
    }
}

# Initialize session state
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = pd.DataFrame()

# Custom CSS
def load_css():
    st.markdown(f"""
        <style>
            .main {{ background-color: #f8f9fa; }}
            .metric-card {{ 
                background: white; 
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .critical-alert {{ 
                animation: pulse 1.5s infinite;
                border: 2px solid {CONFIG['colors']['danger']};
            }}
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
                100% {{ opacity: 1; }}
            }}
            @media (max-width: 768px) {{
                .dashboard-container {{ flex-direction: column; }}
            }}
        </style>
    """, unsafe_allow_html=True)

class DataGenerator:
    @staticmethod
    def generate_biometrics():
        levels = ['Low', 'Moderate', 'High', 'Critical']
        return {
            'timestamp': datetime.now(),
            'heart_rate': np.random.randint(60, 110),
            'hrv': np.random.randint(20, 80),
            'spO2': np.random.randint(90, 100),
            'motion': np.random.randint(0, 10),
            'stress': np.random.choice(levels, p=[0.6, 0.25, 0.1, 0.05]),
            'fatigue': np.random.choice(levels, p=[0.5, 0.3, 0.15, 0.05]),
            'health_risk': np.random.choice(levels, p=[0.55, 0.25, 0.15, 0.05])
        }
    
    @classmethod
    def generate_historical_data(cls, length=20):
        return pd.DataFrame([cls.generate_biometrics() for _ in range(length)])

class DashboardComponents:
    @staticmethod
    def create_gauge(value, title, min_val, max_val, color):
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            gauge = {
                'axis': {'range': [min_val, max_val]},
                'bar': {'color': color},
                'steps': [
                    {'range': [min_val, max_val*0.6], 'color': CONFIG['colors']['success']},
                    {'range': [max_val*0.6, max_val*0.8], 'color': CONFIG['colors']['warning']},
                    {'range': [max_val*0.8, max_val], 'color': CONFIG['colors']['danger']}
                ]
            }
        ))
        fig.update_layout(margin=dict(t=0, b=0))
        return fig

    @staticmethod
    def risk_level_badge(level):
        color_map = {
            'Low': CONFIG['colors']['success'],
            'Moderate': CONFIG['colors']['warning'],
            'High': CONFIG['colors']['danger'],
            'Critical': CONFIG['colors']['danger']
        }
        return f"<span style='color: white; background: {color_map[level]}; padding: 2px 10px; border-radius: 15px;'>{level}</span>"

def main():
    # Page setup
    st.set_page_config(
        page_title=CONFIG['page_title'],
        layout=CONFIG['layout'],
        page_icon="🚗"
    )
    load_css()

    # Sidebar controls
    with st.sidebar:
        st.header("Monitoring Controls")
        st.session_state.monitoring = st.toggle(
            "Real-time Monitoring", 
            value=st.session_state.monitoring,
            help="Enable continuous biometric monitoring"
        )
        update_freq = st.select_slider(
            "Update Frequency (seconds)",
            options=[1, 2, 3, 5, 10],
            value=CONFIG['metrics_update_interval']
        )

    # Main dashboard layout
    st.title("🚗 SafeDrive Sync - Driver Monitoring System")
    
    # Real-time metrics
    metrics_container = st.container()
    alerts_container = st.container()
    charts_container = st.container()

    with metrics_container:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### ❤️ Cardiovascular Health")
        with col2:
            st.markdown("### 🧠 Cognitive State")
        with col3:
            st.markdown("### 🚗 Vehicle Status")

    # Data generation and display
    if st.session_state.monitoring:
        try:
            while st.session_state.monitoring:
                new_data = DataGenerator.generate_biometrics()
                
                # Update historical data
                st.session_state.historical_data = pd.concat([
                    st.session_state.historical_data,
                    pd.DataFrame([new_data])
                ]).tail(CONFIG['data_history_length'])

                # Update metrics
                with metrics_container:
                    col1, col2, col3 = st.columns(3)
                    
                    # Cardiovascular Health
                    with col1:
                        st.plotly_chart(DashboardComponents.create_gauge(
                            new_data['heart_rate'], "Heart Rate", 60, 110, CONFIG['colors']['primary']
                        ), use_container_width=True)
                        
                        cols = st.columns(2)
                        with cols[0]:
                            st.metric("HRV", f"{new_data['hrv']} ms")
                        with cols[1]:
                            st.metric("SpO2", f"{new_data['spO2']}%")

                    # Cognitive State
                    with col2:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <h4>Stress Level</h4>
                                {DashboardComponents.risk_level_badge(new_data['stress'])}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            <div class='metric-card'>
                                <h4>Fatigue Risk</h4>
                                {DashboardComponents.risk_level_badge(new_data['fatigue'])}
                            </div>
                        """, unsafe_allow_html=True)

                    # Vehicle Status
                    with col3:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <h4>Health Crisis Risk</h4>
                                {DashboardComponents.risk_level_badge(new_data['health_risk'])}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.metric("Motion Intensity", f"{new_data['motion']}/10")

                # Alerts system
                with alerts_container:
                    if new_data['health_risk'] in ['High', 'Critical']:
                        st.error("🚨 CRITICAL HEALTH RISK DETECTED! Initiate emergency protocols!", icon="⚠️")
                    
                    if new_data['fatigue'] == 'Critical':
                        st.warning("😴 CRITICAL FATIGUE LEVEL! Recommend immediate rest break", icon="⚠️")

                # Historical charts
                with charts_container:
                    st.line_chart(
                        st.session_state.historical_data.set_index('timestamp')[['heart_rate', 'hrv', 'spO2']],
                        use_container_width=True
                    )

                time.sleep(update_freq)
        
        except Exception as e:
            st.error(f"Monitoring interrupted: {str(e)}")
            st.session_state.monitoring = False

if __name__ == "__main__":
    main()
