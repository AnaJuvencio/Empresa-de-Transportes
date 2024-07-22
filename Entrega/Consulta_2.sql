SELECT Cliente.*
FROM Compra
JOIN Cliente ON Cliente.CPF = Compra.CPF
WHERE Compra.Nome_Cidade_Destino = 'Recife' AND DATE(Compra.Data_Hora_Chegada) = '2024-08-04';
