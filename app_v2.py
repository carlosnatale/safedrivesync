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

# ... (o restante do código permanece igual ao anterior)
# Manter todas as funções e lógica originais

local_css()  # Aplicar o estilo personalizado

# Interface principal (manter igual)
def main():
    # ... (código da interface mantido igual)

if __name__ == "__main__":
    main()
