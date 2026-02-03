# join/merge entre "Relatorio_cadop.csv" e "consolidado_despesas.csv" 
# usar CNPJ como chave
# adicionar RegistroANS / Modalidade / UF
# tratar -->  registros sem match no cadastro e CNPJs que aparecem múltiplas vezescom dados diferentes

import pandas as pd
import re
from pathlib import Path

# Base do projeto (ETAPA 02), subindo duas pastas a partir de src
BASE_DIR = Path(__file__).resolve().parent.parent
# Arquivos
ARQ_CONSOLIDADO_DESPESAS = BASE_DIR / "consolidado_Etapa01" / "consolidado_despesas.csv"
ARQ_RELATORIO_CADOP = BASE_DIR / "dados_cadastrais" / "Relatorio_cadop.csv"
# Pasta src (onde estão os scripts)
SRC_DIR = BASE_DIR / "src"
# saida pos merge
OUTPUT_DIR = BASE_DIR / "pos_merge"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "consolidado_cadastrais_merge.csv"

df_consolidado = pd.read_csv(ARQ_CONSOLIDADO_DESPESAS, sep=';', encoding='utf-8-sig', dtype={'CNPJ': str})
df_cadop = pd.read_csv(ARQ_RELATORIO_CADOP, sep=';', encoding='utf-8-sig', dtype={'CNPJ': str})

# renomear colunas
df_consolidado = df_consolidado.rename(columns={'REG_ANS': 'RegistroANS'})
df_cadop = df_cadop.rename(columns={'REG_ANS': 'RegistroANS'})

# padronizarr cnpj para nao dar erro no merge
# usar for, pois precisa aplicar a mesma regra nos dois dataframes
for df in (df_consolidado, df_cadop):
    df['CNPJ'] = (df['CNPJ'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(14))


# merge/join
df_merge = df_consolidado.merge(df_cadop[['CNPJ', 'RegistroANS', 'Modalidade', 'UF']], on='CNPJ', how='left', suffixes=('_consolidado', '_cadop'))

# cria a coluna RegistroANS puxando o valor certo dos REG_ANS e dando prioridade para o consolidado
df_merge['RegistroANS'] = (df_merge['RegistroANS_consolidado'].combine_first(df_merge['RegistroANS_cadop']))

#flag de auditoria para registros sem match no cadastro
df_merge['sem_match_cadastro'] = df_merge['UF_cadop'].isna()

# trata o duplicado
df_tirar_duplicado = df_merge.drop_duplicates(subset=['CNPJ', 'RegistroANS', 'Razao_Social', 'ValorDespesas'], keep='first')

# salva final
df_tirar_duplicado.to_csv(OUTPUT_FILE, sep=';', encoding='utf-8-sig', index=False)
