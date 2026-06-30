#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import folium              

#Necessary libraries
import pandas as pd
import streamlit as st
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empresa', page_icon='📈', layout='wide')

# =====================================================
# Funções
# =====================================================
def menos_espaco_topo_grafico():
    st.markdown("""
        <style>
            /* Alvo direto na caixa que carrega o iframe/gráfico do Plotly */
            div[data-testid="stPlotlyChart"] {
                margin-top: -30px !important; /* Puxa o gráfico para cima */
            }
            
            /* Remove espaços internos extras do bloco do Streamlit */
            div[data-testid="stVerticalBlock"] > div {
                padding-bottom: 0px !important;
            }
        </style>
    """, unsafe_allow_html=True)

def country_maps(df1):
    """
        Esta função responde qual a localização central de entrega em cada cidade por tipo de tráfego e retorna um mapa mundial com marcadores nas localizações centrais.
        Parâmetros:
            Input: 
                - df1: Dataframe que deve ser passado para realizar a função.
            Output: 
                - Mapa mundial apresentando marcadores nas localizações centrais de entrega em cada cidade e tipo de tráfego. 
                    Ao selecionar o marcador no mapa, o cliente pode verificar o nome da cidade e a densidade de tráfego do local.
    """
    center_city = (
        df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
        .groupby(['City', 'Road_traffic_density'])
        .median()
        .reset_index()
    )
    
    map = folium.Map()

    for index, location_info in center_city.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],
                    location_info['Delivery_location_longitude']],
                    popup=location_info[['City', 'Road_traffic_density']]).add_to(map)

    maps = folium_static(map, height=500)

    return maps

def order_share_by_week (df1):
    """
        Esta função responde qual a média de número de pedidos entregues por cada entregador por semana, retornando um gráfico para apresentar o resultado.
        Parâmetros:
            Imput: 
                - df1: Dataframe que deve ser passado para realizar a função.
            Output: 
                - Gráfico de linha mostrando no eixo X as semanas do ano e no eixo Y o número de pedidos entregue por entregador.
    """
    orders_by_week = (
        df1.loc[:, ['ID', 'Week_of_year']]
        .groupby('Week_of_year')
        .count()
        .reset_index()
    )

    delivery_person_week = (
        df1.loc[:, ['Delivery_person_ID', 'Week_of_year']]
        .groupby('Week_of_year')
        .nunique()
        .reset_index()
    )

    #Unindo 2 dataframes:
    df1_aux = pd.merge(
        orders_by_week, delivery_person_week, on='Week_of_year', how='inner'
    )

    df1_aux['Order_by_deliver'] = (df1_aux['ID'] / df1_aux['Delivery_person_ID'])
    
    fig = px.line(
        df1_aux, 
        x='Week_of_year', 
        y='Order_by_deliver'
    )
    
    fig.update_traces(
        line=dict(
            color='#6C5CE7',
            width=3 
        )
    )

    fig.update_layout(
        height=500,
        xaxis_title='Week of Year',
        yaxis_title='Order by Delivery Person',
        template='plotly_white'
    )
    
    chart = st.plotly_chart(fig, use_container_width=True)

    return chart

def order_by_week(df1):
    """
        Esta função conta a quantidade de pedidos realizados por semana e retorna um gráfico com o resultado.
        Parâmetros:
            Input:
                - df1: Dataframe que deve ser passado para realizar a função.
            Output: 
                - Gráfico de linha mostrando no eixo X as semanas do ano e no eixo Y o número de entregas realizadas.
    """
    orders_by_week = (
        df1.loc[:, ['ID', 'Week_of_year']]
        .groupby('Week_of_year')
        .count()
        .reset_index()
    )
    
    fig = px.line(
        orders_by_week, 
        x='Week_of_year', 
        y='ID'
    )

    fig.update_traces(
        line=dict(
            color='#6C5CE7',
            width=3  
        )
    )

    fig.update_layout(
        height=500,
        xaxis_title='Week of Year',
        yaxis_title='ID',
        template='plotly_white'
    )
         
    chart = st.plotly_chart(fig, use_container_width=True)

    return chart

def traffic_order(df1, cols):
    """
        Esta função conta a quantidade de pedidos entregues em cada tipo de densidade de tráfego avaliando ou não cada cidade, e retorna um gráfico para apresentar seus resultados.
        Parâmetros:
            Input: 
                - df1: Dataframe que deve ser passado para realizar a função.
                - cols: Coluna(s) a serem avaliadas.
                    ['City', 'Road_traffic_density']: Avalia por cidade
                    'Road_traffic_density': Avalia apenas por tráfego
            Output: 
                - Gráfico de barras empilhadas apresentando no eixo X as cidades e no eixo Y o número de entregas realizadas.
                    As barras tem diferentes cores que representam as densidades de tráfego.
    """
    cols_lista = [cols] if isinstance(cols, str) else cols      #isinstance pergunta se o objeto cols é do tipo string, se for falso é uma lista, se verdadeiro é o nome de uma única coluna.

    orders_by_traffic = (
        df1.loc[:, ['ID'] + cols_lista]
        .groupby(cols_lista)
        .count()
        .reset_index()
    )

    cores_transito = {
        'Low': '#2ECC71',    
        'Medium': '#F1C40F', 
        'High': '#E67E22',    
        'Jam': '#E74C3C'     
    }
    
    if isinstance(cols, str) or len(cols) == 1:
        fig = px.pie(
            orders_by_traffic, 
            values='ID', 
            names='Road_traffic_density',
            color='Road_traffic_density',
            color_discrete_map=cores_transito,
            category_orders={'Road_traffic_density': ['Low', 'Medium', 'High', 'Jam']}
        )

        fig.update_layout(
            height=200,                          # Força o gráfico de pizza a ser pequeno
            margin=dict(t=30, b=0, l=0, r=0),    # Zera as folgas internas que empurram o texto
            legend=dict(
                orientation="v",                # Mantém a legenda vertical
                yanchor="middle", y=0.5         # Centraliza a legenda na altura do gráfico
            )
        )
    
    else:    
        fig = px.bar(
            orders_by_traffic, 
            x='City', 
            y='ID', 
            color='Road_traffic_density',
            barmode='stack',
            text_auto=True,
            color_discrete_map=cores_transito,
            category_orders={'Road_traffic_density': ['Low', 'Medium', 'High', 'Jam']}
        )

        fig.update_layout(
            height=500,                       
            margin=dict(t=25, b=0, l=0, r=0)
        )
    
    chart = st.plotly_chart(fig, use_container_width=True)

    return chart

def orders_by_day(df1):
    """
        Esta função conta a quantidade de pedidos realizados por dia e retorna um gráfico de barras com o resultado.
        Parâmetros:
            Input: 
                - df1: Dataframe que deve ser passado para realizar a função.
            Output: 
                - Gráfico de barras com o eixo X apresentando as datas e o eixo Y apresentando o número de pedidos realizados.
    """
    orders_by_day = (
        df1.loc[:, ['ID', 'Order_Date']]
        .groupby('Order_Date')
        .count()
        .reset_index()
    )
    
    fig = px.bar(
        orders_by_day, 
        x='Order_Date', 
        y='ID'
    )

    fig.update_layout(
        xaxis_title='Order Date',
        yaxis_title='ID',
        template='plotly_white',
        height=300,                        
        margin=dict(t=20, b=50, l=10, r=10)
    )

    # ATUALIZAÇÃO DO EIXO X: É aqui que a correção da sobreposição acontece
    fig.update_xaxes(
        tickangle=-45,           # Rotaciona as datas em 45 graus para facilitar a leitura
        nticks=10,               # Limita para mostrar apenas ~10 datas espaçadas uniformemente no eixo
        tickformat="%d/%m/%Y"    # Formata a data para o padrão brasileiro/europeu (dia/mês/ano)
    )

    fig.update_traces(marker_color='#6C5CE7')
    
    
    chart = st.plotly_chart(fig, use_container_width=True)

    return chart

def clean_code(df1):
    """
        Esta função tem a responsabilidade de limpar o dataframe
    
        Tipos de limpeza:
        1. Remoção dos dados com 'NaN '
        2. Ajuste dos tipos das colunas
        3. Limpeza da coluna de tempo 'Time_taken(min)' (remoção do texto da variável numérica) e transformação em tipo inteiro
        4. Remoção dos espaços das variáveis de texto
        5. Remoção da palavra 'conditions' da coluna 'Weatherconditions'
        6. Criação da coluna 'week_of_year'

        Parâmetros:
            Input: Dataframe.
            Output: Dataframe.
    """
    #Removendo as linhas com 'NaN ':
    df1 = df1.loc[(df['Delivery_person_Age'] != 'NaN '), :]   #seleciona todas as linhas sem o NaN e mostra todas as colunas
    df1 = df1.loc[(df['multiple_deliveries'] != 'NaN '), :]
    df1 = df1.loc[(df['Delivery_person_Ratings'] != 'NaN '), :]
    df1 = df1.loc[(df['City'] != 'NaN '), :]
    df1 = df1.loc[(df['Road_traffic_density'] != 'NaN '), :] 

    #Ajustando os tipos das colunas:
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)     
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'],format = '%d-%m-%Y')
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #Removendo a string '(min)' na coluna 'Time_taken(min)' e transformando coluna em inteiro:
    df1['Time_taken(min)'] = df1['Time_taken(min)'].str.replace(r'[^0-9]', '', regex=True)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    #Removendo espaço após string:
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Delivery_person_ID'] = df1.loc[:, 'Delivery_person_ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()

    #Removendo a palavra 'conditions' da coluna 'Weatherconditions':
    df1['Weatherconditions'] = df1['Weatherconditions'].str.replace('conditions ', '')

    #Criando coluna 'week_of_year':
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U') 
    df1['Week_of_year'] = df1['Week_of_year'].astype(int)

    df1.reset_index()

    return df1

# ------------------------------------------------------------ Início da Estrutura lógica do código ------------------------------------------------------------

# =====================================================
# Import dataset
# =====================================================
df = pd.read_csv('dataset/train.csv') 

# =====================================================
# Limpando os dados
# =====================================================
df1 = clean_code(df)

# =====================================================
# Visão da Empresa
# =====================================================
st.set_page_config(layout="wide")

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

st.markdown('# Marketplace - Company View', text_alignment="center")

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

st.sidebar.markdown( '## Filters:' )

date_slider = st.sidebar.slider( 
    'Deadline date',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)

city_options = st.sidebar.multiselect(
    'City',
    ['Urban', 'Metropolitian', 'Semi-Urban'],
    default = ['Urban', 'Metropolitian', 'Semi-Urban']
)

traffic_options = st.sidebar.multiselect(
    'Traffic density',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam']
)

weather_options = st.sidebar.multiselect(
    'Weather conditions',
    ['Sunny', 'Stormy', 'Sandstorms', 'Cloudy', 'Fog', 'Windy'],
    default = ['Sunny', 'Stormy', 'Sandstorms', 'Cloudy', 'Fog', 'Windy']
)

st.sidebar.markdown('---')
st.sidebar.markdown('#### • Powered by Andressa Melo Mendes')

#Filtro de data:
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de cidade:
linhas_selecionadas = df1['City'].isin(city_options)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de trânsito:
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de condição climática:
linhas_selecionadas = df1['Weatherconditions'].isin(weather_options)
df1 = df1.loc[linhas_selecionadas, :]

# ======================================================
# Layout no Streamlit
# ======================================================
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    st.info("Análise da quantidade de pedidos realizados por data, tráfego e cidade.")
        
    with st.container():
        col1, col2 = st.columns([2, 1])
        menos_espaco_topo_grafico()

        with col1:
            #Responde: Volume de pedidos por cidade e tipo de tráfego
            st.markdown('### Cities with the most orders')
            traffic_order(df1, ['City', 'Road_traffic_density'])

            st.success("""
            💡 Metropolitian tem mais pedidos.""")

            st.warning("""
            🚨 Semi-Urban pouquíssimos pedidos.""")

        with col2:        
            #Responde: Distribuição dos pedidos por tipo de tráfego
            st.markdown('### Orders by Traffic')
            traffic_order(df1, 'Road_traffic_density')

            #Responde: Quantidade de pedidos por dia
            st.markdown('### Number of orders by day')
            orders_by_day(df1)

            st.warning("""
            🚨 Períodos sem pedidos.""")

    st.info("""
        #### 📌 **Conclusão:**
        A análise mostra que a cidade Metropolitian recebe quase 80% de todos os pedidos, enquanto a Semi-Urban não chega a 0.5%.

        O grande volume de pedidos na cidade Metropolitian indica a centralização dos clientes nesta região.

        Semi-Urban com pouquíssimos pedidos.

                Recomenda-se:
                - Incentivos de adoção de novos clientes na região Semi-Urban
                - Expansão da base de parceiros
        """)

with tab2:
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            #Responde: Quantidade de pedidos por semana
            st.markdown('### Orders by Week')  
            order_by_week(df1)

        with col2:
            #Responde: Quantos pedidos cada entregador entrega por semana, em média?
            st.markdown('### Orders delivered by delivery person')
            order_share_by_week(df1)
    
    st.success("""
    💡 A curva de crescimento dos pedidos costuma ser proporcional ao número de pedidos entregue por entregador.
    """)
        
with tab3:
    with st.container():
        #Responde: Localização central de entrega em cada cidade por tipo de tráfego
        st.markdown('### Country Maps')
        country_maps(df1)