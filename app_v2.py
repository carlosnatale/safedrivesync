import streamlit as st
import random
import time
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Simulador ADAS Veicular", layout="wide")

# Função para simular dados do sistema ADAS
def gerar_dados():
    velocidade = random.randint(30, 120)  # km/h
    distancia_objeto = random.randint(5, 200)  # metros
    angulo_direcao = random.randint(-30, 30)  # graus
    frenagem_automatica = distancia_objeto < 20  # Ativa se objeto estiver a menos de 20m
    alerta_fadiga = random.choice([True, False]) if velocidade > 60 else False
    return velocidade, distancia_objeto, angulo_direcao, frenagem_automatica, alerta_fadiga

# Layout do painel ADAS
st.markdown("""
    <style>
    .big-font { font-size: 28px !important; text-align: center; }
    .alerta { color: red; font-weight: bold; }
    .normal { color: green; }
    .atenção { color: orange; }
    </style>
""", unsafe_allow_html=True)

# Colunas para visualização
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<h2 class='big-font'>Velocidade (km/h)</h2>", unsafe_allow_html=True)
    velocidade_display = st.empty()

with col2:
    st.markdown("<h2 class='big-font'>Distância do Objeto (m)</h2>", unsafe_allow_html=True)
    distancia_display = st.empty()

with col3:
    st.markdown("<h2 class='big-font'>Ângulo de Direção (°)</h2>", unsafe_allow_html=True)
    angulo_display = st.empty()

with col4:
    st.markdown("<h2 class='big-font'>Frenagem Automática</h2>", unsafe_allow_html=True)
    frenagem_display = st.empty()

# Simulação em tempo real
grafico_velocidade = []
grafico_distancia = []
for _ in range(100):
    velocidade, distancia_objeto, angulo_direcao, frenagem_automatica, alerta_fadiga = gerar_dados()
    grafico_velocidade.append(velocidade)
    grafico_distancia.append(distancia_objeto)

    if len(grafico_velocidade) > 30:
        grafico_velocidade.pop(0)
        grafico_distancia.pop(0)
    
    velocidade_display.metric(label="", value=f"{velocidade} km/h")
    distancia_display.metric(label="", value=f"{distancia_objeto} m")
    angulo_display.metric(label="", value=f"{angulo_direcao}°")
    frenagem_display.markdown(
        "<h2 class='alerta'>Ativada 🚨</h2>" if frenagem_automatica else "<h2 class='normal'>Desativada</h2>", 
        unsafe_allow_html=True
    )
    
    # Alerta de fadiga
    if alerta_fadiga:
        st.warning("⚠️ Alerta de fadiga! Recomenda-se uma pausa para descanso.")

    # Gráficos de velocidade e distância do objeto
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=grafico_velocidade, mode='lines+markers', name='Velocidade (km/h)', line=dict(color='blue')))
    fig.add_trace(go.Scatter(y=grafico_distancia, mode='lines+markers', name='Distância do Objeto (m)', line=dict(color='red')))
    fig.update_layout(title="Monitoramento de Velocidade e Distância", xaxis_title="Tempo", yaxis_title="Valores", height=400)
    st.plotly_chart(fig, use_container_width=True)

    time.sleep(1)
