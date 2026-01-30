# Teste Estagiário - Intuitive Care

## 📌 Visão Geral
### **Projeto-Teste para vaga de estágio**

Este projeto transforma dados brutos da ANS em informações validadas, enriquecidas e agregadas.
Os dados são armazenados em um banco de dados, acessíveis via API e frontend interativo, além de conter
documentação completa e decisões técnicas justificadas

O projeto consiste em 4 etapas:
  -  01 - INTEGRAÇÃO COM API PÚBLICA
  -  02 - TRANSFORMAÇÃO E VALIDAÇÃO DE DADOS
  -  03 - BANCO DE DADOS E ANÁLISE
  -  04 - API E INTERFACE WEB
  
Cada uma das etapas contém subtópicos com instruções específicas e direcionadas para o que fazer

## 🛠️ Estrutura do Projeto
O projeto foi realizado na linguagem Python + MySQL + Vue.js

## 🎯 Descrição das Etapas

  - **Etapa 01 – Processamento e Consolidação**

-> Buscar e baixar os arquivos de Demonstrações Contábeis dos últimos 3 trimestres disponíveis na API Pública: https://dadosabertos.ans.gov.br/FTP/PDA/

-> Juntar os dados dos 3 trimestres em um só e filtrar apenas os arquivos que contenham dados de ```Despesas com Eventos/Sinistros```

-> Criar e adicionar certas colunas e tratar as inconsistências presentes

-> Criar um único arquivo ```consolidado_despesas.csv``` após todo tratamento exigido for cumprido 

---

  - **Etapa 02 - Validação, Enriquecimento e Agregação**

-> Utilizar o ```consolidado_despesas.csv``` criado na etapa 01 e fazer validações no: CNPJ, na Razão Social e para ter Valores numéricos positivos

-> Baixar arquivo ```Relatorio_cadop.csv``` de Dados Cadastrais das Operadoras Ativas em: https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_
saude_ativas/

-> Juntar ```consolidado_despesas.csv``` com ```Relatorio_cadop.csv``` usando CNPJ como chave

-> Criar e adicionar certas colunas, agrupar dados por duas colunas específicas

-> Realizar cálculos específicos, ordenar a planilha 

-> E por fim, criar um arquivo ```despesas_agregadas.csv``` após todas as operações

---





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



