# esta parte organiza as colunas de acordo com as demandas do teste
# analisa as incosistências, organiza as colunas e gera o arquivo final

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

df = pd.read_csv(DATA_DIR / 'Resultado' / 'planilha_final.csv', sep=';', encoding='utf-8-sig')

# pega uma coluna e:
# .astype(str) --> tranforma em string
# .str.replace(',', '') --> remove vírgulas
# .str.strip() --> remove espaços no começo e fim
# pd.to_numeric(..., errors='coerce') --> converte de volta para número tratando erros colocando-os como NaN
for coluna in ['VL_SALDO_INICIAL', 'VL_SALDO_FINAL']:
    df[coluna] = ( df[coluna].astype(str).str.replace(',', '').str.strip())
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

# Calculo das despesas
df['ValorDespesas'] = df['VL_SALDO_FINAL'] - df['VL_SALDO_INICIAL']

# converte a coluna 'DATA' para datetime e tratando erros e formatos inválidos como NaN ou NaT
# vão ter trimestres e anos com formatos que resultarão em NaN ou NaT, irei ignorá-los e seguir adiante
df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
df['Ano'] = df['DATA'].dt.year
df['Trimestre'] = df['DATA'].dt.quarter

# Excluir linhas não necessarias
del df['VL_SALDO_FINAL']
del df['VL_SALDO_INICIAL']
del df['CD_CONTA_CONTABIL']
del df['DESCRICAO']
del df['DATA']


# index=False --> identificador interno das linhas
# sep=';' --> separador entre colunas no arquivo
# encoding='encoding='utf-8-sig'' --> garante que os caracteres sejam lidos corretament
# salvar na planilha final

df.to_csv(DATA_DIR / 'ResultadoFinal' / "consolidado_despesas.csv", index=False, sep=';', encoding='utf-8-sig')

