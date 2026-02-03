-- importacao conmsolidado_despesas
LOAD DATA LOCAL INFILE 'C:/Users/jpque/OneDrive/Desktop/Intuitive_Care_Teste/Intuitive_Care03/Etapa03/data/consolidado_despesas.csv'
INTO TABLE despesas_consolidadas 
CHARACTER SET utf8mb4 -- encoding (UTF-8)
FIELDS TERMINATED BY ';' -- colunas no CSV são separadas por ';'
LINES TERMINATED BY '\n' -- cada linha termina com quebra de linha
IGNORE 1 LINES -- ignora o cabeçalho do CSV
(REG_ANS, CNPJ, ValorDespesas, Ano, Trimestre)

SET -- tratamento de possiveis inconsistencias nos dados
    
    -- remove caracteres do CNPJ
    CNPJ = REPLACE(REPLACE(REPLACE(CNPJ, '.', ''), '/', ''), '-', ''),

    -- trata valores invalidos em campos numericos
    ValorDespesas =
        CASE
            WHEN ValorDespesas REGEXP '^[0-9]+(\\.[0-9]{1,2})?$'
            THEN ValorDespesas
            ELSE 0
        END, -- valor invalido não pode ser usado em cálculo, logo assume 0 para manter consistencia

    -- trata ano invalido
    Ano =
        CASE
            WHEN Ano REGEXP '^[0-9]{4}$'
            THEN Ano
            ELSE NULL
        END, -- só aceita ano com 4 dígitos numericos

    -- trata trimestre inválido
    Trimestre =
        CASE
            WHEN Trimestre IN (1,2,3,4)
            THEN Trimestre
            ELSE NULL
        END; -- trimestre só pode ser 1 a 4, qualquer outro valor vira NULL


-- importação relatorio_cadop
LOAD DATA LOCAL INFILE 'C:/Users/jpque/OneDrive/Desktop/Intuitive_Care_Teste/Intuitive_Care03/Etapa03/data/Relatorio_cadop.csv'
INTO TABLE relatorio_cadop
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(REG_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade,
 Logradouro, Numero, Complemento, Bairro, Cidade, UF, CEP,
 DDD, Telefone, Fax, Endereco_eletronico,
 Representante, Cargo_Representante, Regiao_de_Comercializacao,
 Data_Registro_ANS)

SET
    -- normaliza CNPJ
    CNPJ = REPLACE(REPLACE(REPLACE(CNPJ, '.', ''), '/', ''), '-', ''),

    -- normaliza UF
    UF = UPPER(UF),

    -- remove hífen do CEP
    CEP = REPLACE(CEP, '-', ''),

    -- converte data para formato DATE
    Data_Registro_ANS = STR_TO_DATE(Data_Registro_ANS, '%d/%m/%Y'), 
    -- converte: 31/12/2022 em 2022-12-31, sem isso MySQL não entende como DATE

    -- valida região de comercialização
    Regiao_de_Comercializacao =
        CASE
            WHEN Regiao_de_Comercializacao BETWEEN 1 AND 9
            THEN Regiao_de_Comercializacao
            ELSE NULL
        END;


-- importacao despesas_agregadas
LOAD DATA LOCAL INFILE 'C:/Users/jpque/OneDrive/Desktop/Intuitive_Care_Teste/Intuitive_Care03/Etapa03/data/despesas_agregadas.csv'
INTO TABLE despesas_agregadas
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Razao_Social, UF, Total_Despesas)
-- nao foi preciso criar um set para tratar incosistências, pois tal arquivo ja vem de um tratamento de dados
