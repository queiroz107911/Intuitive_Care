## 🧠 Decisões Técnicas e Trade-offs - Etapa 01

O projeto pedia para buscar dados na ```API pública da ANS``` e consolidar os últimos 3 trimestres (em formato de planilha) em um único arquivo. Enfrentei o trade-off entre:

1. Processar todos os arquivos em memória de uma vez
2. Processar os arquivos incrementalmente

**Decisão tomada:** Processar as 3 planilhas de uma vez
- Justificativa: Minha máquina suporta o volume de dados e o cliente está interessado apenas no produto final 
- Benefício: Aplicar filtros em todas as planilhas simultaneamente agilizou o trabalho e gerou uma planilha consolidada para uso nas etapas seguintes

> ⚠️ Observação: Embora processar tudo junto não seja a prática mais eficiente, neste contexto foi a abordagem mais prática e rápida para atingir o objetivo !

**Tratamento de inconsistências:**

- Valores zerados ou negativos permaneceram na coluna para serem tratados na Etapa 02. 
- Formatos de data inconsistentes foram padronizados; quando não foi possível, utilizei `NaN` ou `NaT`
- Para reduzir erros em cada coluna, utilizei métodos do Pandas como `astype(str)` e `.str.strip()`
- Esta abordagem garantiu que os dados fossem consistentes o suficiente para as próximas operações, sem comprometer a análise final