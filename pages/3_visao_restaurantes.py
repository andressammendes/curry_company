#Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import folium        
import numpy as np
from datetime import datetime
from PIL import Image
from streamlit_folium import folium_static      

#Necessary libraries
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Visão Restaurantes', page_icon='​🍽️​​', layout='wide')

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

def avg_std_city(df1, col):
    """
        Esta função calcula o tempo médio e o desvio padrão em cada cidade por tipo de pedido ou por densidade de tráfego e retorna um gráfico com os valores obtidos.
        Parâmetros:
            Input:
                - df1: Dataframe que deve ser passado para realizar a função.
                - col: coluna que será avaliada.
                    'Road_traffic_density': Calcula pela densidade de tráfego
                    'Type_of_order': Calcula pelo tipo de pedido
                - category_orders: passa a order das categorias apresentadas no gráfico
                    ordem_traffic
                    ordem_types
                - color_sequence: para uma sequência de cores para ser utilizado no gráfico
                    color_traffic
                    color_types
            Output:
                - Gráfico de barras com barras de erro. No eixo X temos as cidades e no eixo Y o tempo médio, já as barras de erro mostram o desvio padrão.
    """
    avg_std_time_city_order = (
        df1.loc[:, ['Time_taken(min)', 'City', col]]
        .groupby(['City', col])
        .agg({'Time_taken(min)': ['mean', 'std']})
    )

    avg_std_time_city_order.columns = ['avg_time', 'std_time']
    avg_std_time_city_order = avg_std_time_city_order.reset_index()

    ordens = {'Road_traffic_density': ['Low', 'Medium', 'High', 'Jam'],
             'Type_of_order': ['Drinks', 'Snack', 'Meal', 'Buffet']
    }

    colors = {
        'Road_traffic_density': {
        'Low': '#2ECC71',    
        'Medium': '#F1C40F', 
        'High': '#E67E22',    
        'Jam': '#E74C3C'     
        },
        'Type_of_order': {
        'Drinks': '#5BC0DE ',    
        'Snack': '#F0AD4E ', 
        'Meal': '#D9534F ',    
        'Buffet': '#8A6D3B '     
        }
    }

    fig = px.bar(
        avg_std_time_city_order,
        x='City',
        y='avg_time',
        color=col,
        barmode='group',
        error_y='std_time',
        color_discrete_map=colors[col],
        category_orders={col: ordens[col]}
    )

    fig.update_layout(                     
        margin=dict(t=25, b=20, l=10, r=10),
        xaxis_title='City',
        yaxis_title='Time',
        template='plotly_white'
    )

    if col=='Type_of_order':
        fig.update_layout(
            height=350
        )

    chart = st.plotly_chart(fig, use_container_width=True)
    
    return chart

def avg_std_time_city(df1,):
    """
        Esta função calcula e responde o tempo médio e o desvio padrão das entregas por cidade e retorna um gráfico apresentando os resultados.
        Parâmetros:
            Input:
                - df1: Dataframe que deve ser passado para realizar a função.
            Output:
                - Gráfico de barras com barras de erro, onde o eixo X representa as cidades, o Y representa o tempo médio e as barras de erro apresentam o desvio padrão.
    """
    avg_std_time_city = (
        df1.loc[:, ['Time_taken(min)', 'City']]
        .groupby('City')
        .agg({'Time_taken(min)': ['mean', 'std']})
    )
    
    avg_std_time_city.columns = ['time_mean', 'time_std']
    avg_std_time_city = avg_std_time_city.sort_values(by='time_mean', ascending=True).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=avg_std_time_city['City'],
        x=avg_std_time_city['time_mean'],
        error_x=dict(
            type='data',
            array=avg_std_time_city['time_std'],
            visible=True
        ),
        orientation='h',
        width=0.4,
        name='Tempo de entrega por cidade (mean ± std)'
    ))

    fig.update_layout(                      
        height=200,
        margin=dict(t=20, b=0, l=10, r=10),
        yaxis_title='City',
        xaxis_title='Time',
        template='plotly_white'
    )
    
    chart = st.plotly_chart(fig, use_container_width=True)

    return chart

def avg_std_time_delivery(df1, festival, op):
    """
        Esta função calcula o tempo médio e o desvio padrão do tempo de entrega e retorna o resultado obtido.
        Parâmetros:
            Input:
                - df1: Dataframe que deve ser passado para realizar a função.
                - festival: Filtra as linhas pela coluna Festival.
                    'Yes': houve festival
                    'No': não houve festival
                - op: Tipo de operação que precisa ser calculado.
                    'avg': Calcula o tempo médio
                    'std':  Calcula o desvio padrão
            Ouput:
                - Retorna o resultado do cálculo realizado.
    """
    linhas_selecionadas = df1['Festival'] == festival
    
    if op=='avg':
        return np.round(df1.loc[linhas_selecionadas, 'Time_taken(min)'].mean(), 2)

    elif op=='std':
        return np.round(df1.loc[linhas_selecionadas, 'Time_taken(min)'].std(), 2)

def distance(df1):    
    """
        Esta função calcula a distância média entre os restaurantes e os locais de entrega e retorna o valor encontrado.
        Parâmetros:
            Input:
                - df1: Dataframe que deve ser passado para realizar a função.
            Output:
                - Número apresentando a distância média com duas casas decimais.
    """
    df1['distance'] = (
        df1.loc[:, ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']]
        .apply(lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']), 
            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])
            ), axis=1)
    )

    avg_distance = np.round(df1['distance'].mean(), 2) #operação utilizando numpy para arredondar para 2 casas após a vírgula
    
    return avg_distance

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
# Visão dos Restaurantes
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

st.markdown('# Marketplace - Restaurant View', text_alignment="center")

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
st.info("Análise do tempo de entrega quando há ou não Festival e tempo médio de entregas por cidade, por tipo de pedido e por densidade de tráfego.")
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.subheader('Overall Metrics')
            col01, col02 = st.columns(2)

            with col01:
                #Responde: Quantos entregadores únicos
                delivery_person_unique = df1.loc[:, 'Delivery_person_ID'].nunique()
                col01.metric('Number of delivery persons', delivery_person_unique)

            with col02:
                #Responde: Distância média dos restaurantes e dos locais de entrega
                col02.metric('Avg distance traveled', distance(df1))

    with col2:
        with st.container(border=True):
            st.subheader('🎆 Festival')
            col01, col02 = st.columns(2)

            with col01:
                #Responde: Tempo médio de entrega quando há festival
                col01.metric('Avg time', avg_std_time_delivery(df1, 'Yes', op='avg'))

            with col02:    
                #Responde: Desvio padrão de entrega quando há festival
                col02.metric('Std time', avg_std_time_delivery(df1, 'Yes', op='std'))

    with col3:
        with st.container(border=True):
            st.subheader('🎆 No Festival')
            col03, col04 = st.columns(2)

            with col03:
                #Responde: Desvio padrão de entrega quando NÃO há festival
                col03.metric('Avg time', avg_std_time_delivery(df1, 'No', op='avg'))

            with col04:
                #Responde: Desvio padrão de entrega quando NÃO há festival
                col04.metric('Std time', avg_std_time_delivery(df1, 'No', op='std'))

st.warning("""
🚨 **Atenção:** Durante festivais, o tempo médio aumenta mais de 70%,
indicando sobrecarga na operação ou tráfego mais intenso.""")

menos_espaco_topo_grafico()
#Responde: Tempo médio e desvio padrão de entrega por cidade
with st.container():
    col1, col2 = st.columns([2, 1])

    with col1:
        #Responde: Tempo médio e desvio padrão de entrega por cidade e tipo de tráfego
        st.subheader('Impact of traffic on delivery time')
        avg_std_city(df1, 'Road_traffic_density')

        st.warning("""
        🚨 **Insight:** Tráfego aumenta o tempo em até 25%
        """)

        st.warning("""
        🚨 **Insight:** Semi-Urban maior demora em todos os cenários.
        """)

    with col2:
        #Responde: Tempo médio e desvio padrão de entrega por cidade e tipo de pedido
        st.subheader('Order type and delivery delay')
        avg_std_city(df1, 'Type_of_order')

        #Responde cidade com entrega mais demorada
        st.subheader('Cities with slow delivery')
        avg_std_time_city(df1)

st.info("""
    #### 📌 **Conclusão:**
    A análise mostra que o tempo de entrega é fortemente impactado pela densidade de tráfego e pela ocorrência de eventos (festivais).

    Durante períodos de alto tráfego e eventos, há aumento significativo tanto no tempo médio quanto na variabilidade das entregas, indicando perda de eficiência operacional.

    Isso sugere que a operação atual não está preparada para lidar com picos de demanda e condições adversas.

            Recomenda-se:
            - Reforço de entregadores em períodos críticos
            - Ajuste dinâmico de rotas
            - Estratégias específicas para eventos
    """)