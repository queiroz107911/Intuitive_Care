# esta parte pega o arquivo filtrado em 'filtrar_&_juntar.csv' e faz um merge com o arquivo 'Relatorio_cadop'
# encontrado na API publica, para trazer os dados do CNPJ e RazaoSocial para atender a demanda do teste

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" 


df_planilha_filtrada_sinistros = pd.read_csv( DATA_DIR / 'Planilhas_tratadas' / "planilha_filtrada_sinistros.csv", sep=';', encoding='utf-8-sig')
df_relatorio_cadop = pd.read_csv(DATA_DIR / 'Planilhas_tratadas' / "Relatorio_cadop.csv", sep=';', encoding='utf-8-sig', 
    dtype={
        'REG_ANS': int,
        'CNPJ': str
    })

df_relatorio_cadop['CNPJ'] = (
    df_relatorio_cadop['CNPJ']
    .str.replace('.0', '', regex=False)
    .str.zfill(14)
)

# cada REG_ANS corresponde a umCNPJ e RazaoSocial, ambos arquivos possuem REG_ANS
# logo, o código irá trazer o CNPJ e RazaoSocial de relatorio_cadop para planilha_filtrada correlacionando com o respectivo REG_ANS
planilha_final = df_planilha_filtrada_sinistros.merge(df_relatorio_cadop[['REG_ANS', 'CNPJ', 'Razao_Social', 'Modalidade', 'UF']], on='REG_ANS', how='left')

planilha_final.to_csv('planilha_final.csv', sep=';', encoding='utf-8-sig', index=False)

