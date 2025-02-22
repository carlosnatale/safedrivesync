import streamlit as st
import time
import random
import base64

# Configuração inicial
st.set_page_config(layout="wide")

# Função para carregar imagem como Base64
def get_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Carregar CSS personalizado
def local_css():
    bg_image = get_base64("infotainment - Copia.png")
    css = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stAlert, .stMarkdown {{
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }}
    .metric-box {{
        background: rgba(255, 255, 255, 0.85);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

# ... (mantenha aqui as outras funções originais)
# Gerar dados biométricos
def generate_biometrics():
    return {
        "Heart Rate": random.randint(60, 180),
        "HRV": random.randint(20, 200),
        "SpO2": random.randint(85, 100),
        "Blood Pressure": f"{random.randint(90, 180)}/{random.randint(60, 120)}",
        "Blood Sugar": random.randint(70, 300),
        "Motion Intensity": random.choice(["Low", "Moderate", "High"]),
    }

# Determinar status de risco
def calculate_risk(metrics):
    risks = {
        "Stress": "Normal",
        "Fatigue": "Normal",
        "Health Crisis": "Normal"
    }
    
    # Lógica de determinação de risco
    if metrics["Heart Rate"] > 120:
        risks["Stress"] = "High" if random.random() > 0.5 else "Moderate"
    if metrics["Blood Sugar"] > 200:
        risks["Health Crisis"] = "Moderate"
    if metrics["SpO2"] < 92:
        risks["Health Crisis"] = "Critical" if metrics["SpO2"] < 88 else "High"
    
    return risks

# Interface principal
def main():
    local_css()  # Chamada dentro da função main
    st.title("SafeDrive Sync Prototype")
    
    # Colunas para layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Real-time Biometric Monitoring")
        metrics = generate_biometrics()
        
        # Exibir métricas
        metric_style = "padding: 15px; border-radius: 10px; background: rgba(255, 255, 255, 0.9); margin: 10px 0;"
        for k, v in metrics.items():
            st.markdown(f'<div style="{metric_style}"><strong>{k}:</strong> {v}</div>', unsafe_allow_html=True)
        
        # Atualização automática
        time.sleep(1.5)
        st.experimental_rerun()
    
    with col2:
        st.header("Vehicle Response Settings")
        
        # Configurações de resposta
        actions = st.multiselect(
            "Select vehicle responses:",
            ["No Action", "Send Notification", "Reduce Speed", "Play Calming Music",
             "Turn On Air Conditioning", "Adjust Seat Position", "Activate Horn",
             "Call Emergency Services", "Activate Autopilot", "Flash Alert Lights"]
        )
        
        # Determinar riscos
        risks = calculate_risk(metrics)
        
        # Exibir alertas e ações
        for condition, level in risks.items():
            if level != "Normal":
                if "Send Notification" in actions:
                    st.error(MESSAGES[condition][level])
                if "Play Calming Music" in actions:
                    st.success("Playing calming music through vehicle speakers")
                if "Turn On Air Conditioning" in actions:
                    st.info("Adjusting AC to optimal temperature (22°C)")
                if "Activate Autopilot" in actions:
                    st.warning("Activating emergency autopilot system")

if __name__ == "__main__":
    main()  # Tudo dentro do bloco principal
