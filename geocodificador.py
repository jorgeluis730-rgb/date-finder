import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
CAMINHO_ENTRADA = BASE_DIR / "Dados" / "Bar-Restaurantes.xlsx"
df = pd.read_excel(CAMINHO_ENTRADA)
df.columns = df.columns.str.strip()
df["endereco_completo"] = df["Endereço"] + ", " + df["Bairro"] + ", São Paulo, SP, Brasil"
print(df["endereco_completo"].head())

# --- teste de geocodificação ---

geolocator = Nominatim(user_agent="date_dashboard_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

df["location"] = df["endereco_completo"].apply(geocode)
def geocodificar_com_fallback(row):
    endereco_completo = row["endereco_completo"]
    resultado = geocode(endereco_completo)
    
    if resultado is None:
        # tenta de novo só com rua + bairro + cidade (sem número, sem "andar", etc)
        endereco_simples = f'{row["Bairro"]}, São Paulo, SP, Brasil'
        resultado = geocode(endereco_simples)
    
    return resultado

df["location"] = df.apply(geocodificar_com_fallback, axis=1)
df["latitude"] = df["location"].apply(lambda loc: loc.latitude if loc else None)
df["longitude"] = df["location"].apply(lambda loc: loc.longitude if loc else None)

print(df.loc[df["latitude"].isna(), ["Nome", "endereco_completo"]])
df["latitude"] = df["location"].apply(lambda loc: loc.latitude if loc else None)
df["longitude"] = df["location"].apply(lambda loc: loc.longitude if loc else None)

print(df[["Nome", "latitude", "longitude"]])
print(df.loc[df["latitude"].isna(), ["Nome", "endereco_completo"]])

# correção manual: geocodificação retornou coordenada errada pro iccarus sp
df.loc[df["Nome"].str.strip() == "iccarus sp", "latitude"] = -23.543689
df.loc[df["Nome"].str.strip() == "iccarus sp", "longitude"] = -46.636220

print(df[df["Nome"].str.strip() == "iccarus sp"][["Nome", "latitude", "longitude"]])

#----------- salvar nova planilha 

CAMINHO_SAIDA = BASE_DIR / "Dados" / "Bar-Restaurantes-Geocodificado.xlsx"
df.to_excel(CAMINHO_SAIDA, index=False)