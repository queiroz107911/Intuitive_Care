## 🧠 Decisões Técnicas e Trade-offs - Etapa 03

A partir dos arquivos ```consolidado_despesas.csv``` , ``` despesas_agregadas.csv``` e ```Relatorio_cadop.csv``` foi necessário criar três querries DDL(definir ou alterar a estrutura do banco de dados) para estruturar tabelas. Além disso, foi necessário importar os arquivos ```.csv``` para as tabelas criadas e, no final, desenvolver três querries analíticas para responder perguntas específicas sobre despesas e operadoras. Durante esse processo, certos desafios surgiram:

1. Como normalizar as tabelas? Desnormalizada com todos os dados ou normalizadas separadas?
2. Escolha dos tipos de dados
    - **DECIMAL vs FLOAT vs INTEGER** (centavos) - para valores monetários?
    - **DATE vs VARCHAR vs TIMESTAMP** - para datas ?
3. Tratamento de inconsistências nos dados

**1. Decisão tomada:** Tabelas normalizadas e separadas
- Justificativa: Devido a um alto volume de dados, separar as tabelas é uma solução melhor evitando redundância e inconsistência nos dados
- Benefício: Performance melhor em análises, manutenção mais fácil, redução de erros

**2. Decisão tomada:** Valores monetários: DECIMAL(14,2) e Data: Date
- Justificativa: **Decimal** permite garantia de precisão exata para valores financeiros elevados
- Benefício: Melhor que FLOAT ou INTEGER para cálculos financeiros complexos

- Justificativa: **Date** permite operações nativas de datas
- Benefício: VARCHAR não permite cálculos e validações de forma nativa e TIMESTAMP não é necessário, pois não há hora/minuto nos arquivos


**Tratamento de inconsistências:**

- **CNPJ:** Removidos pontos, barras e hífens para normalização
- **Valores inválidos em campos numéricos:** Substituídos por 0 para manter consistência.
- **Ano inválido:** Apenas anos com 4 dígitos são aceitos; outros viram NULL
- **Trimestre inválido:** Apenas valores entre 1 e 4 são aceitos; outros viram NULL
- **UF:** Normalizadas para letras maiúsculas
- **CEP:** Removido hífen
- **Data de registro:** Convertida de DD/MM/YYYY para YYYY-MM-DD usando STR_TO_DATE
- **Região de comercialização:** Apenas valores entre 1 e 9 são aceitos; outros viram NULL