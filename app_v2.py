import streamlit as st
import time
import random
import numpy as np
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Sistema Anti-Sonolência", layout="wide")

# Função para simular frequência cardíaca e nível de sonolência
def gerar_dados():
    freq_cardiaca = random.randint(60, 100)
    sonolencia = random.uniform(0, 1)  # 0 (alerta) a 1 (muito sonolento)
    return freq_cardiaca, sonolencia

# Layout estilo painel de carro
st.markdown("""
    <style>
    .big-font { font-size: 32px !important; text-align: center; }
    .alerta { color: red; font-weight: bold; }
    .normal { color: green; }
    .atenção { color: orange; }
    </style>
""", unsafe_allow_html=True)

# Colunas para simular o painel
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("<h2 style='text-align: center;'>Frequência Cardíaca</h2>", unsafe_allow_html=True)
    freq_hist = []
    
with col2:
    st.markdown("<h1 style='text-align: center;'>Status do Motorista</h1>", unsafe_allow_html=True)
    status = st.empty()

with col3:
    st.markdown("<h2 style='text-align: center;'>Nível de Sonolência</h2>", unsafe_allow_html=True)

# Simulação em tempo real
freq_hist = []
for _ in range(100):  # Simular 100 ciclos
    freq, sono = gerar_dados()
    freq_hist.append(freq)
    if len(freq_hist) > 30:
        freq_hist.pop(0)  # Manter histórico curto

    # Atualização do status do motorista
    if sono < 0.3:
        status.markdown("<h2 class='normal'>🚗 Alerta</h2>", unsafe_allow_html=True)
        status_color = "green"
    elif 0.3 <= sono < 0.7:
        status.markdown("<h2 class='atenção'>⚠️ Atenção</h2>", unsafe_allow_html=True)
        status_color = "orange"
    else:
        status.markdown("<h2 class='alerta'>🚨 Sonolento!</h2>", unsafe_allow_html=True)
        status_color = "red"

    # Gráfico da frequência cardíaca
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=freq_hist, mode='lines+markers', name='Frequência', line=dict(color=status_color)))
    fig.update_layout(title="Monitoramento Cardíaco", xaxis_title="Tempo", yaxis_title="BPM", height=300)
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    # Indicador de nível de sonolência
    with col3:
        st.progress(sono)
    
    time.sleep(1)
