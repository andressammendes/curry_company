import streamlit as st
from PIL import Image

st.set_page_config(page_title='Home', page_icon='📓')

# ======================================================
# Barra lateral
# ======================================================
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            gap: 0.2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

image = Image.open('logo.jpg')
st.sidebar.image(image, width=100)

st.sidebar.markdown('# Curry Company')   
st.sidebar.markdown('## Fastest Delivery in Town')  
st.sidebar.markdown( "---" )
st.sidebar.markdown('#### • Powered by Andressa Melo Mendes')

# ======================================================
# Layout no Streamlit
# ======================================================
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div[data-testid="stMainBlockContainer"] {
                padding-top: 0rem; 
                padding-bottom: 0rem;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.write('# Curry Company Growth Dashboard')

st.markdown('#### 🎯 Problema de negócio: Quais fatores mais impactam o tempo de entrega e onde estão os principais gargalos operacionais?', text_alignment="center")

st.markdown('---')
st.markdown(
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.

    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Visão Gerencial: Métricas gerais dos entregadores.
        - Visão Tática: Métricas das avaliações.
    - Visão Restaurantes:
        - Indicadores de tempo de entrega dos pedidos.
        
    ### Ask for Help
    - e-mail: andressamendes.mv@gmail.com
    """
)