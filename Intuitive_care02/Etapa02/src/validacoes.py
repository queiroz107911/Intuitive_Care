# validacoes 
# pegar consolidado_despesas e:
# CNPJ válido (formato e dígitos verificadores)
# Valores numéricos positivos
# Razão Social não vazia
# tratar CNPJs inválidos

import pandas as pd
import re
from pathlib import Path

# Base do projeto (ETAPA 02), subindo duas pastas a partir de src
BASE_DIR = Path(__file__).resolve().parent.parent
# Arquivos
ARQ_CONSOLIDADO_DESPESAS = BASE_DIR / "consolidado_Etapa01" / "consolidado_despesas.csv"
# Pasta src (onde estão os scripts)
SRC_DIR = BASE_DIR / "src"


df = pd.read_csv(ARQ_CONSOLIDADO_DESPESAS, sep=';', encoding='utf-8-sig', dtype={'CNPJ': str})


# caso existe, remove '.', '-', '/'
# regex=True --> indica que o padrão passado é uma expressão regular,
# pandas vai interpretar caracteres especiais como expressão regular, e não como texto literal
# trtamento para remover '.0' no final
df['CNPJ'] = (df['CNPJ'].fillna('').astype(str).str.replace(r'\D', '', regex=True))

# validacao do CNPJ para estarem no formato certo e terem digitos válidos
def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', str(cnpj)) # remover caracteres nao numéricos # '\D' -> qualquer caractere que nao seja um dgito
    
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14: 
        return False
    
    return True

df['cnpj_valido'] = df['CNPJ'].apply(validar_cnpj)
# Optamos por não corrigir CNPJs incompletos automaticamente
# para evitar criação de identificadores artificiais. 
# Registros inválidos foram mantidos e marcados para permitir análise posterior e rastreabilidade dos dados.
# O resultado False reflete a realidade do dado, não um erro.



# validacao para razao social nao vazia
# .notna() para verificar se existe algum valor na coluna
# .strip() remove os espaços em branco do começo e do fim da string
# retorna true na coluna 'razao_social_valida' caso nao esteja vaiza
# limpar e padronizar a coluna razao social
df['Razao_Social'] = (df['Razao_Social'].astype(str).str.strip().str.upper().replace({'': pd.NA, 'NAN': pd.NA}))
# criar coluna para validar
df['razao_social_valida'] = df['Razao_Social'].notna()


# faz com que valordespesas nao tenham numero negativo
# faz uma limpa antes para garantir que seja valro numerico e nao string
df['ValorDespesas'] = pd.to_numeric(df['ValorDespesas'], errors='coerce')
df.loc[df['ValorDespesas'] < 0, 'ValorDespesas'] = pd.NA

# transforma ano e trimestre em int e remove o '.0' do final
df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce').astype('Int64')
df['Trimestre'] = pd.to_numeric(df['Trimestre'], errors='coerce').astype('Int64')

