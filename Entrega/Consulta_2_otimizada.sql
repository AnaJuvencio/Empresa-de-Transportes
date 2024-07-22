CREATE INDEX idx_compra_cidade_data ON compra (nome_cidade_destino, data_hora_chegada);

SELECT Cliente.*
FROM Compra
JOIN Cliente ON Cliente.CPF = Compra.CPF
WHERE Compra.Nome_Cidade_Destino = 'Recife' AND Data_Hora_Chegada >= '2024-08-04 00:00:00'
    AND Data_Hora_Chegada < '2024-08-05 00:00:00';
