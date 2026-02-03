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

O projeto foi desenvolvido utilizando diferentes tecnologias a fim de facilitar o trajeto até o objetivo final

### Python

Responsável por grande parte de processamento das 4 etapas do projeto incluindo:

- Leitura e escrita de arquivos CSV
- Padronização, validação, filtragem, organização e análise de dados
- Integração de bases por meio de merge/join
- Tratamento de inconsistências
- Geração de relatórios finais após os tratamentos necessários

### Bibliotecas utilizadas:

- pandas → manipulação e análise de dados
- pathlib → organização e portabilidade dos caminhos do projeto (padrão do python)
- re → tratamento de strings e normalização de campos (padrão do python)

---
### MySQL

Utilizado somente na Etapa 03 para estruturar e organizar os dados importados dos arquivos CSV. Suas principais funções nesta etapa foram:

- Armazenamento estruturado das bases consolidadas
- Execução de consultas analíticas diretamente no banco
- Importação e manipulação de dados via arquivos CSV
- Criação de queries DDL para estruturar as tabelas
- Queries de importação para inserir dados de arquivo CSV nas tabelas
- Queries analíticas para análise e geração de relatórios

---
### Vue.js

Planejado para a camada de visualização do projeto e utilizando somente na Etapa 04

- Criação de dashboards e tabelas interativas
- Consumo dos dados já processados pelo backend
- Facilitação da análise dos resultados por usuários finais
- (Não utilizado diretamente na Etapa 02, mas definido como parte da arquitetura futura do sistema)

--- 


# 📂 Organização dos Arquivos

A estrutura do projeto foi organizada de forma modular para facilitar manutenção, leitura e evolução:

### Intuitive_Care/Etapa01/
- ```src/``` -> scripts Python responsáveis pelo processamento
- ```data/``` -> subpastas com arquivos CSV relativos ao nome de cada planilha
- ```Planilhas_originais/``` -> arquivos baixado da API pública com dados relativos de 3 trimestres
- ```Planilhas_tratadas/``` -> arquivos pós primeira modificação da Etapa 01 **("planilha_filtrada_sinistros.csv")** e para merge **("Relatorio_cadop.csv")**
- ```Resultado/``` -> arquivo pós-merge **("planilha_filtrada_sinistros.csv" e "Relatorio_cadop.csv")**
- ```ResultadoFinal/``` -> arquivo final organizado para ser usado na Etapa 02 **("consolidado_despesas.csv")**
- ```README.md``` -> documentar decisões técnicas e trade-offs da Etapa 01

### Intuitive_care02/Etapa02/ 
- ```consolidado_Etapa01/``` -> arquivo **"consolidado_despesas.csv"** da Etapa01 para realizar operações
- ```dados_cadastrais/``` -> arquivo **"Relatorio_cadop.csv"** para merge/join
- ```pos_merge/``` → arquivos gerados após a integração das bases 
- ```planilha_final/``` → resultado dos arquivos agregados, ordenados, verificados e tratados
- ```src/``` -> scripts Python responsáveis pelo processamento
- ```README.md``` -> documentar decisões técnicas e trade-offs da Etapa02

### Intuitive_care03/Etapa03/
- ```data/``` -> arquivos CSV utilizados
- ```src``` -> arquivos SQL para criação das diferentes queries 
- ```README.md``` -> documentar decisões técnicas e trade-offs da Etapa03

> ⚠️ Observação: Testei diferentes arquiteturas de modularização e a estratégia usada na Etapa 03 foi a melhor. A organização com apenas data/ e src/ deixa o projeto mais objetivo e limpo, sem poluição visual de múltiplas pastas e arquivos desnecessários 
---


## 🎯 Descrição das Etapas

  - **Etapa 01 – Integração com API Pública**

-> Processamento e Consolidação de dados

-> Buscar e baixar os arquivos de Demonstrações Contábeis dos últimos 3 trimestres disponíveis na API Pública: https://dadosabertos.ans.gov.br/FTP/PDA/ 

-> Juntar os dados dos 3 trimestres em um único arquivo e filtrar apenas os dados que contenham ```Despesas com Eventos/Sinistros```

-> Criar e adicionar colunas específicas e tratar inconsistências

-> Gerar o arquivo final ```consolidado_despesas.csv``` após todo tratamento

---

  - **Etapa 02 - Transformação e Validação de Dados**

-> Validação, enriquecimento e agregação de dados

-> Validar CNPJ, Razão Social e valores numéricos positivos no ```consolidado_despesas.csv```

-> Baixar arquivo ```Relatorio_cadop.csv``` de Dados Cadastrais das Operadoras Ativas em: https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/ 

-> Realizar merge entre ```consolidado_despesas.csv``` e ```Relatorio_cadop.csv``` usando CNPJ como chave

-> Criar e adicionar colunas adicionais, agrupar dados por colunas específicas

-> Executar cálculos, ordenar e organizar os dados

-> Gerar arquivo final ```despesas_agregadas.csv``` após todas as operações

---

  - **Etapa 03 - Banco de Dados e Análise**

-> Utilizar os arquivos ```consolidado_despesas.csv```, ```despesas_agregadas.csv``` e ```Relatorio_cadop.csv```

-> Criar queries DDL para estruturar tabelas necessárias para cada arquivo CSV

-> Aplicar normalizações e padronizações nos dados

-> Criar queries de importação para inserir dados nas tabelas, atentando-se ao encoding e tratamento de inconsistências

-> Desenvolver queries analíticas para responder perguntas de negócios







