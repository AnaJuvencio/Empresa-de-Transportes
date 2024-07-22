SELECT Cliente.*
FROM Cliente
JOIN Compra ON Cliente.CPF = Compra.CPF
WHERE Cliente.Nome ILIKE ‘<letras>%’
AND data_hora_partida BETWEEN ‘X’ AND ‘Y’
ORDER BY nome;
