# Curry Company: Ecossistema de Inteligência Logística e DataViz / Logistics Intelligence & DataViz Ecosystem

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Dynamic%20Charts-3F4F75.svg)](https://plotly.com/)

> 🌐 **Live Dashboard:** [Access the Streamlit App Here / Acesse o Dashboard Aqui](https://amendes-curry-company.streamlit.app)

---

## 📌 Language Selection / Seleção de Idioma
*   [Versão em Português](#-versão-em-português)
*   [English Version](#-english-version)

---

## 🇧🇷 Versão em Português

### 1. O Problema de Negócio
A **Curry Company** é um marketplace de delivery que opera em escala multi-regional. O principal desafio da diretoria operacional era a dependência de métricas agregadas simples (como o tempo médio de entrega global), que mascaravam gargalos estruturais, variabilidades climáticas e comportamentos críticos de clientes e entregadores.

O objetivo deste projeto foi construir um pipeline de dados *end-to-end* e um ecossistema interativo de dashboards dividido em três pilares estratégicos (**Empresa, Restaurantes e Entregadores**) para transformar dados brutos em decisões operacionais de alta fidelidade.

### 2. Decisões Técnicas e Trade-offs de Engenharia
*   **Tratamento de Dados Nulos (Drop Consciente):** Em vez de adotar técnicas comuns de imputação estatística (como preenchimento por média ou mediana), optei pelo descarte direcionado das linhas com valores faltantes nos KPIs de tempo. **A justificativa:** Como o núcleo (*core*) do negócio depende da precisão milimétrica dos tempos de entrega, qualquer imputação arbitrária adicionaria ruído estatístico e enviesaria a análise operacional.
*   **Performance do Pipeline:** O processamento e a engenharia de recursos (*feature engineering*) foram otimizados em Python para garantir que a renderização dos gráficos dinâmicos no Streamlit operasse de forma fluida.

### 3. Arquitetura das Visões Estratégicas
O ecossistema foi projetado para segmentar a complexidade operacional em três painéis interdependentes:
*   **📊 Visão Empresa (Estratégico):** Focada no monitoramento de volume de pedidos, densidade de tráfego e distribuição geográfica das vendas.
*   **🍕 Visão Restaurantes (Operacional):** Desenvolvida para avaliar o tempo médio de entrega sob a ótica de distância, tipos de pedido e impacto de eventos.
*   **🛵 Visão Entregadores (Tático/Qualidade):** Voltada para a análise de performance individual, idade dos veículos, condições climáticas e distribuição de avaliações.

### 4. Principais Insights de Negócio 💡
*   **Concentração de Demanda e Oportunidade de Expansão:** O mapeamento geográfico provou que **80% de toda a demanda de pedidos está concentrada na região Metropolitana**. Isso gerou um direcionamento duplo para o negócio: a necessidade de otimização severa na alocação da frota existente para a região de maior criticidade e um estudo analítico de viabilidade para expansão de parceiros nas áreas Semi-Urbana e Urbana, que atualmente operam muito abaixo da capacidade. 
*   **Diagnóstico de Sobrecarga em Festivais:** Durante períodos de "Festivais", o tempo médio de entrega sofre um salto drástico de 26 para 45 minutos. A aplicação de **barras de erro estatístico** demonstrou que o desvio padrão cai significativamente durante esses eventos. Do ponto de vista de negócios, isso comprova que o atraso não é uma oscilação casual ou isolada, mas sim um **gargalo sistêmico de capacidade da frota** e de processos de preparação sob estresse.
*   **Fator de Rigidez na Avaliação dos Clientes:** A análise de distribuição por **Boxplots** revelou que cenários com **tráfego fluido (Low) e clima limpo (Sunny)** possuem uma dispersão de notas significativamente maior e alta concentração de *outliers* de avaliações baixas. Isso evidencia empiricamente que, sob condições ideais de trânsito e clima, a régua de exigência do cliente final se torna muito mais rígida, fazendo com que erros pontuais de atendimento se sobressaiam.

---

## 🇺🇸 English Version

### 1. The Business Problem
**Curry Company** is a delivery marketplace operating on a multi-regional scale. The operational board's main challenge was its reliance on simple aggregated metrics (such as global average delivery time), which masked structural bottlenecks, weather variability, and critical driver/customer behaviors.

The goal of this project was to build an end-to-end data pipeline and an interactive dashboard ecosystem divided into three strategic pillars (**Company, Restaurants, and Delivery Persons**) to transform raw data into high-fidelity operational decisions.

### 2. Technical Decisions & Engineering Trade-offs
*   **Handling Missing Data (Conscious Drop):** Instead of adopting common statistical imputation techniques (such as mean or median filling), I opted for the targeted removal of rows with missing values in the time KPIs. **The rationale:** Since the core of the business relies on pinpoint accuracy of delivery times, any arbitrary imputation would introduce statistical noise and bias the operational analysis.
*   **Pipeline Performance:** Data processing and feature engineering were optimized in Python to ensure that the rendering of dynamic charts in Streamlit operated seamlessly.

### 3. Strategic Views Architecture
The ecosystem was designed to segment operational complexity into three interdependent panels:
*   **📊 Company View (Strategic):** Focused on monitoring order volume, traffic density, and geographic sales distribution.
*   **🍕 Restaurant View (Operational):** Developed to evaluate average delivery times from the perspective of distance, order types, and event impacts.
*   **🛵 Delivery Persons View (Tactical/Quality):** Geared toward parsing individual performance, vehicle age, weather profiles, and rating distributions.

### 4. Key Business Insights  💡
*   **Demand Concentration & Expansion Opportunities:** Geographic mapping proved that **80% of total order demand is concentrated in the Metropolitan region**. This generated two clear business strategies: a pressing need for severe optimization of fleet allocation within the highest-criticality area, and an analytical feasibility study for partner expansion in Semi-Urban and Urban areas, which currently operate far below capacity.
*   **Overload Diagnosis During Festivals:** During "Festival" periods, the average delivery time experiences a dramatic spike from 26 to 45 minutes. Implementing **statistical error bars** demonstrated that the standard deviation drops significantly during these events. From a business perspective, this proves that the delay is not a casual or isolated fluctuation, but a **systemic fleet capacity bottleneck** and workflow breakdown under stress.
*   **Customer Expectation Tightness Factor:** Distribution analysis via **Boxplots** revealed that scenarios with **fluid traffic (Low) and clear weather (Sunny)** exhibit a significantly higher dispersion of ratings and a heavy concentration of low-rating outliers. This empirically demonstrates that under ideal traffic and weather conditions, the end-customer's expectation bar becomes much stricter, making isolated service mistakes stand out sharply.
---

## 🛠️ Stack / Technologies
*   **Language:** Python 3.9+
*   **Data Manipulation:** Pandas / NumPy
*   **Data Visualization:** Plotly Express (Dynamic & interactive charts)
*   **Deploy & Interface:** Streamlit Framework
*   **Version Control:** Git & GitHub

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/andressammendes/curry_company.git](https://github.com/andressammendes/curry_company.git)
   cd curry_company

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    
3. Run the Streamlit application:
      ```bash
      streamlit run Home.py

---
## 📈 Roadmap & Next Steps

Implement a Machine Learning module to predict delivery times in real-time based on the engineered variables.

Evolve the missing data strategy by testing advanced imputation algorithms (such as K-NN Imputer) in a staging environment to measure deviation in operational KPIs.

---
**Developed by Andressa Melo Mendes**

Connect with me on [LinkedIn](https://www.linkedin.com/in/andressa-melo-mendes/) to discuss data solutions and business intelligence.
