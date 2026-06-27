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

st.set_page_config(page_title='Visão Entregadores', page_icon='🏍️​', layout='wide')

# =====================================================
# Funções
# =====================================================
def avg_ratings_delivery_person(df1):
    """
        Esta função calcula a média das avaliações que cada entregador recebeu e retorna um dataframe com as informações obtidas.
        Parâmetros:
            Input:
                - df1: Dataframe que deve ser passado para realizar a função.
            Output: 
                - Dataframe com duas colunas (ID dos entregadores e média das avaliações), onde o número de linhas é igual ao número de entregadores.
    """
    avg_ratings_delivery_person = (
        df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
        .groupby('Delivery_person_ID')
        .mean()
        .reset_index()
    )
    
    df1_aux = st.dataframe(
        avg_ratings_delivery_person, 
        height=500,
        use_container_width=True
    )

    return df1_aux

def get_avg_std_ratings(df1, col):
    """
        Esta função calcula a média das avaliações recebidas de acordo com a densidade de tráfego ou as condições climáticas e retorna um dataframe com o resultado.
        Parâmetros:
            Input: 
                - df1: Dataframe que deve ser passado para realizar a função.
                - col: coluna a ser avaliada ('Road_traffic_density' ou 'Weatherconditions').
            Output: 
                - Dataframe com três colunas (densidade de tráfego ou condição climática, média das avaliações e desvio padrão das avaliações).
                    No caso do dataframe que avalia a densidade de tráfego há 4 linhas ('Low', 'Medium', 'High', 'Jam').
                    No dataframe que avalia as condições climáticas há 6 linhas ('Sunny', 'Stormy', 'Sandstorms', 'Cloudy', 'Fog', 'Windy')
    """
    avg_std_ratings = (
        df1.loc[:, ['Delivery_person_Ratings', col]]
        .groupby(col)
        .agg({'Delivery_person_Ratings': ['mean', 'std']})
    )

    avg_std_ratings.columns = ['avg_delivery', 'std_delivery']
    avg_std_ratings = avg_std_ratings.reset_index().set_index(col)

    df1_aux = st.dataframe(avg_std_ratings, use_container_width=True)
    
    return df1_aux

def top_delivers(df1, top_asc):
    """
        Esta função analisa os top 10 entregadores mais rápidos ou mais lentos e retorna um gráfico de barras horizontais com os resultados.
        Parâmetros:
            Input: 
                - df1: Dataframe que deve ser passado para realizar a função.
                - top_asc: ordenação da coluna de tempo.
                    top_asc=False: Fastest. O 'False' ordena o gráfico do plotly do maior ao menor (gráfico de barras horizontais desenhado de baixo (primeira linha) para cima (última linha)).
                    top_asc=True: Slowest. O 'True' ordena o gráfico do plotly do menor ao maior (gráfico de barras horizontais desenhado de baixo (primeira linha) para cima (última linha)). 
            Output: 
                - Gráfico de barras horizontais apresentando no eixo X a velocidade de entrega e no eixo Y o ID de cada entregador.
    """
    df1_aux = (
        df1.loc[:, ['Time_taken(min)', 'Delivery_person_ID', 'City']]
        .groupby(['City', 'Delivery_person_ID'])
        .agg({'Time_taken(min)': 'mean'})
        .sort_values(['City', 'Time_taken(min)'])
        .reset_index()
    )

    if top_asc==False: #mais rápidos
        df1_aux = (
            df1_aux.loc[:, :]
            .nsmallest(10, 'Time_taken(min)')   #nsmallest os 10 menores números.
            .sort_values('Time_taken(min)', ascending=top_asc)
        )

    elif top_asc==True: #mais lentos
        df1_aux = (
            df1_aux.loc[:, :]
            .nlargest(10, 'Time_taken(min)')   #nlargest garante que está pegando os 10 maiores números. 
            .sort_values('Time_taken(min)', ascending=top_asc) 
        )
    
    fig = px.bar(
        df1_aux, 
        x='Time_taken(min)', 
        y='Delivery_person_ID', 
        orientation='h'
    )
    
    fig.update_layout(
        xaxis_title='Delivery Time',
        yaxis_title='Delivery person ID',
        template='plotly_white'
    )
    
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
            Input: Dataframe
            Output: Dataframe
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
# Visão dos Entregadores
# =====================================================
st.set_page_config(layout="wide")
st.markdown('# Marketplace - Delivery Person View', text_alignment="center")

# ======================================================
# Barra lateral
# ======================================================
image = Image.open('logo.jpg')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Curry Company')   
st.sidebar.markdown('## Fastest Delivery in Town')  
st.sidebar.markdown( "---" )

st.sidebar.markdown( '## Select the deadline date' )

date_slider = st.sidebar.slider( 
    'Deadline date',
    value=datetime(2022, 4, 13),
    min_value=datetime(2022, 2, 11),
    max_value=datetime(2022, 4, 6),
    format='DD-MM-YYYY'
)

st.sidebar.markdown("---")

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

st.sidebar.markdown("---")
st.sidebar.markdown('### Powered by Andressa Melo Mendes')

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
st.markdown('---')
st.title('Overall Metrics')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        #Delivery person metric
        #Responde: Idade dos entregadores (maior e menor)
        st.markdown('### • Delivery person age')
            
        with st.container():
            col01, col02 = st.columns(2)

            with col01:
                older = df1.loc[:, 'Delivery_person_Age'].max()
                col01.metric('Older', older)

            with col02:
                younger = df1.loc[:, 'Delivery_person_Age'].min()
                col02.metric('Younger', younger)           

    with col2:
        #Responde: Condição dos veículos (melhor e pior)
        st.markdown('### • Vehicle condition')

        with st.container():
            col01, col02 = st.columns(2)

            with col01:
                best = df1.loc[:, 'Vehicle_condition'].max()
                col01.metric('Best', best)

            with col02:
                worst = df1.loc[:, 'Vehicle_condition'].min()
                col02.metric('Worst', worst)

st.markdown('---')
st.title('Ratings:')

with st.container():
    col1, col2 = st.columns(2)

    with col1:  
        #Responde: Avaliações médias por entregador
        st.markdown('##### Avg Ratings by Delivery Person')
        avg_ratings_delivery_person(df1)

    with col2:
        #Responde: Avaliações médias por trânsito
        st.markdown('##### Avg Ratings by Traffic Density')
        get_avg_std_ratings(df1, 'Road_traffic_density')

        #Responde: Avaliações médias por condições climáticas
        st.markdown('##### Avg Ratings by Weather Conditions')
        get_avg_std_ratings(df1, 'Weatherconditions')

st.markdown('---')
st.title('Delivery Speed:')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        #Responde: 10 entregadores mais rápidos
        st.markdown('##### Top 10 Fastest Delivery Person')
        top_delivers(df1, top_asc=False)

    with col2:
        #Responde: 10 entregadores mais lentos
        st.markdown('##### Top 10 Slowest Delivery Person')
        top_delivers(df1, top_asc=True)