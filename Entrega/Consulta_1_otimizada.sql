SELECT Cliente.*
FROM Cliente
WHERE Cliente.Nome ILIKE ‘<letras>%’
AND Cliente.CPF IN (SELECT Compra.CPF FROM Compra WHERE data_hora_partida BETWEEN 'X' AND ‘Y’')
ORDER BY nome;
