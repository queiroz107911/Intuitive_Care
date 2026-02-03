# Esta parte filtra buscando "Despesas com Eventos/Sinistros " e junta os 3 arquivos.csv disponibilizados em um só

from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

arquivos = ["1T2025.csv", "2T2025.csv", "3T2025.csv"]

# armazenar os DataFrames filtrados
dfs_filtrados = []
# (?i) para filtrar maiúsculas eminúsculas e variações de singular e plural
filtro = re.compile(r'(?i)despesa|despesas|evento|eventos|sinistro|sinistros')

for arquivo in arquivos:
    caminho = DATA_DIR / "Planilhas_originais" / arquivo
    df = pd.read_csv(caminho, sep=";", encoding='utf-8-sig')
    
    # filtragem de linhas
    df_filtrado = df[df['DESCRICAO'].str.contains(filtro, na=False)]
    dfs_filtrados.append(df_filtrado)

# concatenar arquivos filtrados
df_eventos_sinistros = pd.concat(dfs_filtrados, ignore_index=True)

# cria planinha filtrada
df_eventos_sinistros.to_csv("planilha_filtrada_sinistros.csv", index=False, sep=';', encoding='utf-8-sig')

