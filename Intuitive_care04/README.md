## 🧠 Decisões Técnicas e Trade-offs - Etapa 04

Nesta etapa, o objetivo foi desenvolver uma API REST em Python que deveria ser construída a partir dos dados já persistidos no banco de dados criado na Etapa 03. Seu consumo deveria ser por uma interface web utilizando Vue.js. Durante o desenvolvimento, surgiram alguns pontos importantes de decisão técnica

    1. Qual framework Python utilizar para a API?
    2. Qual estratégia de paginação adotar para listagem de operadoras?
    3. Qual estrutura de resposta retornar para facilitar o consumo no frontend?

**1. Decisão tomada:** FastAPI
- Justificativa: Oferece alta performance por ser baseado em ASGI, além de suporte nativo a tipagem com Pydantic, validação automática de dados e geração de documentação interativa via Swagger
- Benefício: Melhor performance comparado ao Flask, documentação automática das rotas (/docs) e facilidade para evolução futura da API

**2. Decisão tomada:** Offset-based pagination
- Justificativa: O volume de dados esperado é moderado e a paginação por OFFSET e LIMIT é simples de implementar, fácil de entender e suficiente para o escopo do projeto
- Benefício: Implementação direta em SQL, facilidade de uso no frontend

**3. Decisão tomada:** Dados + metadados 
- Justificativa: Retornar metadados junto com os dados facilita significativamente o controle de paginação no frontend
- Benefício: Melhor experiência no consumo da API e facilidade para implementar paginação e contadores no frontend
