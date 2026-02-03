-- Opção B: Tabelas normalizadas separadas
-- Justificativa perfeita para o teste:
-- Alto volume de despesas (milhões de linhas)
-- Dados cadastrais mudam pouco
-- Queries analíticas mais limpas com JOIN
-- Evita redundância e inconsistência


-- data/consolidado_despesas.csv
CREATE TABLE despesas_consolidadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    REG_ANS INT NOT NULL,
    CNPJ VARCHAR(14) NOT NULL,
    ValorDespesas DECIMAL(14,2) NOT NULL,
    Ano INT NOT NULL,
    Trimestre INT NOT NULL
);


-- indices
CREATE INDEX idx_despesas_cnpj
ON despesas_consolidadas (CNPJ);
-- indice ordenado pelo CNPJ
CREATE INDEX idx_despesas_periodo
ON despesas_consolidadas (CNPJ, Ano, Trimestre);
-- indice composto ordenado primeiro por CNPJ, depois Ano, depois Trimestre
CREATE INDEX idx_despesas_reg_ans
ON despesas_consolidadas (REG_ANS);


-- data/Relatorio_cadop
CREATE TABLE relatorio_cadop (
    id INT AUTO_INCREMENT PRIMARY KEY,
    REG_ANS INT NOT NULL,
    CNPJ VARCHAR(14) NOT NULL,
    Razao_Social VARCHAR(255) NOT NULL,
    Nome_Fantasia VARCHAR(100),
    Modalidade VARCHAR(150),
    Logradouro VARCHAR(150),
    Numero VARCHAR(10),
    Complemento VARCHAR(100),
    Bairro VARCHAR(100),
    Cidade VARCHAR(50),
    UF CHAR(2),
    CEP VARCHAR(8),
    DDD CHAR(2),
    Telefone VARCHAR(11),
    Fax VARCHAR(11),
    Endereco_eletronico VARCHAR(254), -- limite maximo definido pelos padroes rfc de email
    Representante VARCHAR(150),
    Cargo_Representante VARCHAR(100),
    Regiao_de_Comercializacao TINYINT UNSIGNED NOT NULL,
    Data_Registro_ANS DATE NOT NULL,
    CHECK (Regiao_de_Comercializacao BETWEEN 1 AND 9)
);

-- indices
CREATE INDEX idx_relatorio_reg_ans
ON Relatorio_cadop (REG_ANS);

CREATE INDEX idx_relatorio_cnpj
ON Relatorio_cadop (CNPJ);

CREATE INDEX idx_relatorio_uf
ON Relatorio_cadop (UF);


-- data/despesas_agregadas
CREATE TABLE despesas_agregadas (
    Razao_Social VARCHAR(255) NOT NULL,
    UF CHAR(2) NOT NULL,
    Total_Despesas DECIMAL(14,2) NOT NULL,
    PRIMARY KEY (Razao_Social, UF)
)
-- PRIMARY KEY --> por ultimo, pois é uma PK composta e deve ficar no final da tabela



-- observações:
-- índice é uma estrutura ordenada de consultas, vai direto ao ponto
-- toda PRIMARY KEY já cria automaticamente um índice

-- o índice da PK(id) NÃO ajuda nas consultas reais em relatorio_cadop e despesas_consolidadas
-- indice da PK é diferente do indice para consultas de negócio
-- despesas_agregadas nao possui indices adicionais
-- a PRIMARY KEY composta já cria o indice necessario

-- CREATE INDEX idx_despesas_cnpj ON despesas_consolidadas (CNPJ); -->
-- “Crie um índice chamado idx_despesas_cnpj na tabela despesas_consolidadas, usando a coluna CNPJ.”
-- CREATE INDEX -> comando DDL / idx_despesas_cnpj → nome do índice / ON tabela (coluna) -> onde e sobre o quê

-- TINYINT UNSIGNED --> usado para numeros inteiros pequenos e controlados alem de remover numeros negativos
-- DATE --> Melhor que VARCHAR para representar datas e TIMESTAMP só seria necessário caso tivesse hora/minuto

-- decimal(p, s) --> precision(total de digitos) / scale(quantas casas decimais) 
-- garantir precisão exata e suportar valores financeiros elevados sem risco de overflow 
-- melhor que float e mais legivel