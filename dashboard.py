import pandas as pd #importa as bibliotecas
import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
from pathlib import Path

# Cria uma variável para o caminho da planilha 
BASE_DIR = Path(__file__).resolve().parent
CAMINHO_PLANILHA = BASE_DIR / "Dados" / "Bar-Restaurantes-Geocodificado.xlsx"

st.set_page_config(page_title="Date Finder", page_icon="🏍️") # usa a biblioteca st para configurar a pagina com o titulo 'date finder e icone'

st.title("🏍️ Date Finder -Jorge") #titulo da pagina
st.write("Digite o endereço do encontro e receba os lugares mais próximos da sua lista.") #A linha st.write exibe um texto na tela do aplicativo web. 
 

@st.cache_data    #Esse bloco de código serve para carregar os dados de uma planilha Excel de forma rápida e eficiente
def carregar_planilha(): #cria uma função chamada carregar planilha 
    return pd.read_excel(CAMINHO_PLANILHA) #retorna a função do panda de abrir a planilha no modo leitura


df = carregar_planilha() #cria uma variável com a função que carrega a planilha 

geolocator = Nominatim(user_agent="date_dashboard_app") # Esta linha configura e inicializa o localizador geográfico (geocodificador) da biblioteca GeoPy

endereco_dela = st.text_input(
    "Endereço do encontro:",
    placeholder="Ex: Avenida Paulista, 1000, São Paulo"
)

qtd_sugestoes = st.slider("Quantos lugares sugerir?", min_value=1, max_value=5, value=3) # aqui cria a variável de quantidade de sugestões

buscar = st.button("Buscar lugares")

# guarda o resultado numa "memória" que sobrevive entre reruns do Streamlit
if "resultado" not in st.session_state:
    st.session_state.resultado = None

if buscar:
    if not endereco_dela:
        st.warning("Digite um endereço antes de buscar.")
    else:
        with st.spinner("Buscando endereço..."):
            localizacao = geolocator.geocode(endereco_dela)

        if not localizacao:
            st.error("Não consegui encontrar esse endereço. Tenta ser mais específico (rua, número, cidade).")
            st.session_state.resultado = None
        else:
            coord_referencia = (localizacao.latitude, localizacao.longitude)

            df_calculado = df.copy()
            df_calculado["distancia_km"] = df_calculado.apply(
                lambda row: geodesic(coord_referencia, (row["latitude"], row["longitude"])).km,
                axis=1
            )

            top_n = df_calculado.sort_values("distancia_km").head(qtd_sugestoes)

            # salva tudo que precisamos mostrar, pra não perder no próximo rerun
            st.session_state.resultado = {
                "endereco": localizacao.address,
                "coord_referencia": coord_referencia,
                "top_n": top_n
            }

# exibe o resultado se ele existir na memória (independente de ter acabado de clicar ou não)
if st.session_state.resultado:
    resultado = st.session_state.resultado

    st.success(f"Endereço encontrado: {resultado['endereco']}")

    st.subheader("Sugestões")
    st.dataframe(
        resultado["top_n"][["Nome", "Tipo", "Bairro", "Endereço", "distancia_km"]].rename(
            columns={"distancia_km": "Distância (km)"}
        ),
        hide_index=True
    )

    mapa = folium.Map(location=resultado["coord_referencia"], zoom_start=14)

    folium.Marker(
        location=resultado["coord_referencia"],
        tooltip="Ponto de encontro",
        icon=folium.Icon(color="red", icon="heart")
    ).add_to(mapa)

    for _, row in resultado["top_n"].iterrows():
        folium.Marker(
            location=(row["latitude"], row["longitude"]),
            tooltip=row["Nome"],
            popup=f"{row['Nome']} - {row['distancia_km']:.2f} km",
            icon=folium.Icon(color="blue", icon="glass")
        ).add_to(mapa)

    st.subheader("Mapa")
    st_folium(mapa, width=700, height=500)

# caminho no CMD: py -m streamlit run "cd C:\Users\joao1\Documentos\DIGITAL-AI-STUDY\Codigos-python.py\projet_dates.py
#py -m streamlit run dashboard.py"