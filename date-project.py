import pandas as pd # importa a bibliotéca pandas
from geopy.geocoders import Nominatim # de geopy importa o Nominatim
from geopy.distance import geodesic # de geopy importa o geodesic
import folium #importa a bibliotéca folium
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CAMINHO_PLANILHA = BASE_DIR / "Dados" / "Bar-Restaurantes-Geocodificado.xlsx"
df = pd.read_excel(CAMINHO_PLANILHA)
# acima cria uma variável que usando o pandas ele abre no modo leitura a planilha do excel que está nesse diretório
geolocator = Nominatim(user_agent="date_dashboard_app") #Essa linha está criando um objeto de geolocalização usando a classe Nominatim da biblioteca GeoPy, identificando o aplicativo com um nome único no parâmetro user_agent

endereco_dela = "Avenida Paulista, 1000, São Paulo" # Define uma variável de texto contendo o endereço que você deseja buscar.
localizacao_dela = geolocator.geocode(endereco_dela) # envia esse endereço para um serviço de mapas online (da biblioteca geopy).
# Guarda o objeto de resposta. Se o endereço for encontrado, esse objeto conterá a latitude, a longitude e o endereço formatado.
if localizacao_dela: #Essa linha está verificando se a busca anterior por um endereço funcionou e,  #se sim, extraindo as coordenadas geográficas
    coord_dela = (localizacao_dela.latitude, localizacao_dela.longitude)  # (latitude e longitude) para salvá-las juntas em uma tupla.
    print(f"Coordenadas: {coord_dela}") #mostra na tela o endereço e informa que o endereço foi encontrado
    print(f"Endereço encontrado: {localizacao_dela.address}") 
else:
    print("Não consegui localizar esse endereço.") #caso contrário diz que não conseguiu localizar

def calcular_distancia(row, coord_referencia):
    coord_lugar = (row["latitude"], row["longitude"]) #Essa função calcula a distância em quilômetros entre dois pontos geográficos 
    return geodesic(coord_referencia, coord_lugar).km #usando o modelo de alta precisão da Terra (fórmula geodésica).

df["distancia_km"] = df.apply(lambda row: calcular_distancia(row, coord_dela), axis=1) # Esta linha cria uma nova coluna chamada distancia_km em um DataFrame (df) contendo a distância calculada para cada linha.

QTD_SUGESTOES = 3 #Esta linha está filtrando a tabela do Pandas para encontrar e salvar as 3 opções de lugares mais próximas 
top3 = df.sort_values("distancia_km").head(QTD_SUGESTOES) #do seu ponto de referência.

print(top3[["Nome", "Bairro", "Endereço", "distancia_km"]]) # mostra na tela os top 3 lugares mais próximos
#----------- gerador de mapa

mapa = folium.Map(location=coord_dela, zoom_start=14) #Esta linha está criando o mapa interativo básico usando Folium

# marcador do endereço dela (vermelho, pra destacar)
folium.Marker(
    location=coord_dela, #aqui está adicionando os emoticons do mapa, a localização dela é um balãozinho vermelho
    tooltip="Ponto de encontro",
    icon=folium.Icon(color="red", icon="heart")
).add_to(mapa)

# marcadores dos lugares sugeridos (azul)
for _, row in top3.iterrows(): #Essa linha de código inicia um loop para percorrer linha por linha um conjunto de dados do Pandas chamado top3
    folium.Marker(
        location=(row["latitude"], row["longitude"]),
        tooltip=row["Nome"],
        popup=f"{row['Nome']} - {row['distancia_km']:.2f} km",
        icon=folium.Icon(color="blue", icon="glass")
    ).add_to(mapa)

mapa.save("mapa_dates.html")
print("Mapa salvo como mapa_dates.html")