VACUUM 
EXPLAIN ANALYSE SELECT Cliente.*
FROM Compra
JOIN Cliente ON Cliente.CPF = Compra.CPF
WHERE Compra.Nome_Cidade_Destino = 'Recife' AND DATE(Compra.Data_Hora_Chegada) = '2024-08-04';

CREATE INDEX idx_compra_cidade_data ON compra (nome_cidade_destino, data_hora_chegada);


EXPLAIN ANALYSE SELECT Cliente.*
FROM Compra
JOIN Cliente ON Cliente.CPF = Compra.CPF
WHERE Compra.Nome_Cidade_Destino = 'Recife' AND Data_Hora_Chegada >= '2024-08-04 00:00:00'
    AND Data_Hora_Chegada < '2024-08-05 00:00:00';
	
EXPLAIN ANALYSE SELECT Cliente.*
FROM Compra NATURAL JOIN Cliente 
WHERE Compra.Nome_Cidade_Destino = 'Recife' AND Data_Hora_Chegada >= '2024-08-04 00:00:00'
    AND Data_Hora_Chegada < '2024-08-05 00:00:00';

 
EXPLAIN ANALYZE
SELECT Cliente.*
FROM Cliente
JOIN (
  SELECT CPF
  FROM Compra
  WHERE Nome_Cidade_Destino = 'Recife'
    AND Data_Hora_Chegada >= '2024-08-04 00:00:00'
    AND Data_Hora_Chegada < '2024-08-05 00:00:00'
) AS ComprasFiltradas ON Cliente.CPF = ComprasFiltradas.CPF;
 
 
SELECT
    indexname,
    indexdef
FROM
    pg_indexes
WHERE
    tablename = 'compra';

DROP INDEX idx_compra_cidade_data;


SELECT * FROM 