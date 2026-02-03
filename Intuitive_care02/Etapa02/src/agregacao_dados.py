# Agrupe os dados por RazaoSocial e UF
# Calcule o total de despesas por operadora/UF
# ordene por valor total (maior para menor)
# salvar em novo csv "despesas_agregadas.csv"

import pandas as pd
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Arquivos
ARQ_CONSOLIDADO_CADASTRAIS = BASE_DIR / "pos_merge" / "consolidado_cadastrais_merge.csv"
# Pasta src (onde estão os scripts)
SRC_DIR = BASE_DIR / "src"

# saida pos agregações, salvar planilha final
OUTPUT_DIR = BASE_DIR / "planilha_final"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "despesas_agregadas.csv"

df = pd.read_csv(ARQ_CONSOLIDADO_CADASTRAIS, sep=';', encoding='utf-8-sig')

# renomear a coluna do "despesas_agregadas.csv"
df = df.rename(columns={'UF_consolidado': 'UF'})


# .groupby --> agrupa linhas que têm valores iguais em uma ou mais colunas / junte todas as linhas da mesma operadora na mesma UF
# .agg --> aplica funções de agregação em cada grupo / para cada grupo, some a coluna ValorDespesas e chame o resultado de Total_Despesas
# as_index=false --> vita que as colunas do groupby virem índice / salvar em csv sempre usar
# index=false --> ão salva o índice como coluna no CSV
# .sort_values --> ordena as linhas pelo valor de uma coluna / Ordena do menor → maior / ascending=false inverte a ordem

# agrupa os dados por RazaoSocial e UF e calcule o total de despesas por operadora/UF / 1 linha = 1 operadora + 1 UF
# coluna nova: Total_Despesas
df_despesas_agregadas = (df.groupby(['Razao_Social', 'UF'], as_index=False).agg(Total_Despesas=('ValorDespesas', 'sum')))

# ordena do maior para o menor a partir da coluna total_despesas
df_despesas_agregadas = df_despesas_agregadas.sort_values(by='Total_Despesas', ascending=False)

df_despesas_agregadas.to_csv(OUTPUT_FILE, sep=';', encoding='utf-8-sig', index=False)