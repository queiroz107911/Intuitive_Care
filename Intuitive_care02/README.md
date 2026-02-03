## 🧠 Decisões Técnicas e Trade-offs - Etapa 02

A partir da base de dados gerada na Etapa 01 ("consolidado_despesas.csv") foi preciso enriquecer os dados com informações presentes em outro arquivo ("Relatorio_cadop.csv") além de
fazer validações e agregações para criar outro arquivo. Durante esse processo, surgiram alguns desafios principais:

   1. Como tratar CNPJs inválidos?
   2. Como processar os dados no merge/join ? 
   3. Como lidar com registros que não possuem correspondência no cadastro?
   4. Como evitar inconsistências causadas por duplicidades?
   5. Qual estratégia escolher para a ordenação considerando volume de dados e recursos disponíveis? 

**1. Decisão tomada:** Padronização prévia dos CNPJs e função de validação antes do merge/join

- Justificativa: Padronizar os CNPJs antes do merge/join evita falhas e garante que todos os CNPJ estejam no mesmo formato
- Benefício: Aumenta a taxa de correspondência correta entre os arquivos e reduz a perda de informações relevantes no merge/join

**2. Decisão tomada:** Foi utilizado um merge do tipo left join, garantindo que todos os registros do "consolidado_despesas.csv" fossem preservados

- Justificativa: O objetivo é analisar despesas; portanto, perder registros por ausência de cadastro não seria aceitável
- Benefício: 

**3. Decisão tomada:** Após o merge, foi criada uma flag de auditoria para identificar registros que não encontraram correspondência no cadastro

- Justificativa: Facilita a identificação de dados incompletos e possíveis problemas de origem nos cadastros
- Benefício: Transparência no processo de integração e maior controle sobre a qualidade dos dados

**5. Decisão tomada:** Agregação para obter o total de despesas por operadora e UF

- Justificativa: A agregação reduz o volume de dados e facilita análises comparativas entre operadoras e UF
- Benefício: Geração de um dataset final claro, objetivo

**Tratamento de inconsistências:**

- Remoção de caracteres não numéricos (., /, -) e preenchimento com zeros à esquerda para garantir 14 dígitos
- Utilização de left join para preservar todos os registros de despesas
- Uso de sufixos (_consolidado, _cadop) para diferenciar campos com o mesmo nome vindos de fontes distintas
- Remoção de registros duplicados com base em chaves relevantes (CNPJ, RegistroANS, Razao_Social, ValorDespesas).
- A agregação final considera apenas as colunas essenciais (Razao_Social, UF, ValorDespesas), reduzindo o impacto de campos ausentes ou inconsistentes