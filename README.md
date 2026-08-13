# 🏍️ Date Finder

Aplicativo que sugere os bares e restaurantes mais próximos de um endereço, pensado para facilitar a escolha do local de um encontro em São Paulo.

## Como funciona

1. **`geocodificador.py`** — lê a lista de bares/restaurantes (`Dados/Bar-Restaurantes.xlsx`), converte os endereços em coordenadas (latitude/longitude) usando o Nominatim (OpenStreetMap) e salva o resultado em `Dados/Bar-Restaurantes-Geocodificado.xlsx`.
2. **`date-project.py`** — versão em linha de comando: calcula a distância de um endereço até os locais da lista e gera um mapa interativo (`mapa_dates.html`).
3. **`dashboard.py`** — versão interativa em [Streamlit](https://streamlit.io/): você digita o endereço, escolhe quantos lugares quer ver e recebe uma tabela + mapa com as sugestões mais próximas.

## Tecnologias

- Python
- Pandas
- Streamlit
- Geopy (geocodificação via Nominatim/OpenStreetMap)
- Folium (mapas interativos)

1. Clone o repositório:

git clone https://github.com/jorgeluis730-rgb/date-finder.git
cd date-finder


2. Instale as dependências:

pip install -r requirements.txt


3. Rode o dashboard:

streamlit run dashboard.py


## Estrutura do projeto

date-finder/
├── dashboard.py
├── date-project.py
├── geocodificador.py
├── requirements.txt
└── Dados/
├── Bar-Restaurantes.xlsx
└── Bar-Restaurantes-Geocodificado.xlsx


Feito por Jorge.
