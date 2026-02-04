-- query 1 -> Top 5 operadoras com maior crescimento percentual entre o primeiro e o último trimestre


-- Durante a validação dos dados utilizados na Query 1 (crescimento percentual entre o primeiro e o último trimestre analisado), 
-- identifiquei um erro cometido nas etapas anteriores de extração e carga dos dados

-- Após o saneamento da base, foi constatado que a tabela despesas_consolidadas contém apenas um trimestre válido (2025/1). 
-- Registros com Ano = 0 e Trimestre = 0 foram identificados como artefatos do processo de transformação e removidos

-- Como o cálculo de crescimento percentual exige pelo menos dois trimestres distintos, decidi não implementar a Query 1, 
-- uma vez que o resultado não seria tecnicamente válido com os dados atualmente disponíveis

-- Esse problema não está relacionado à lógica SQL da query, mas sim à inconsistência gerada nas etapas anteriores do pipeline, que foi identificada e documentada durante a análise


-- query 2 -> Top 5 UFs com maiores despesas totais + média de despesas por operadora em cada UF

SELECT UF, 
    SUM(ValorDespesas) AS total_despesas, 
    -- desafio adicional
    -- DISTINCT CNPJ --> nao contar a mesma operadora duas vezes
    ROUND(SUM(ValorDespesas) / COUNT(DISTINCT CNPJ), 2) AS media_por_operadora
FROM despesas_consolidadas
WHERE Trimestre IN (1,2,3)
  AND UF IS NOT NULL
  AND UF <> ''
-- agrupa todas as linhas por uf
GROUP BY UF
-- maior para o menor e pega os 5 primeiros resultados
ORDER BY total_despesas DESC
LIMIT 5;


-- query 3 -> Operadoras com despesas acima da média geral em pelo menos 2 trimestres

SELECT
    COUNT(*) AS quantidade_operadoras
-- a subquery (o bloco debaixo) vai gerar uma lista de CNPJs que atendem a condição / COUNT(*) --> conta quantos CNPJs passaram
-- t é só o apelido obrigatório da subquery
-- cada linha representa uma operadora, o resultado final é a quantidade de operadoras
FROM (
    SELECT CNPJ,
        SUM(
            CASE
                WHEN ValorDespesas > (SELECT AVG(ValorDespesas) FROM despesas_consolidadas WHERE Trimestre IN (1,2,3)) THEN 1 ELSE 0 
            END
            -- CASE --> devolve 1 se a condiçao for verdadeira(acima da média) e 0 se for falsa 
            -- somar(SUM) 1 e 0 dá exatamente o número de vezes que a condição aconteceu
            -- a media geral vem de SELECT AVG(ValorDespesas)... -> calcula a média de ValorDespesas considerando todas as linhas dos trimestres 1,2,3. É a media global
        ) AS trimestres_acima_media
    FROM despesas_consolidadas
    WHERE Trimestre IN (1,2,3) -- garante a analise somente dos 3 trimestres
    GROUP BY CNPJ
    HAVING trimestres_acima_media >= 2
    -- mantém apenas os CNPJs que ficaram acima da média em 2 ou 3 trimestres
) t; -- apelido para a subquery
