--criando o bd
CREATE DATABASE empresa_de_transportes;

-- Criação da tabela Cliente
CREATE TABLE Cliente (
    CPF VARCHAR(11) PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Endereco VARCHAR(255) NOT NULL,
    Telefone VARCHAR(20) NOT NULL,
    Email VARCHAR(100) NOT NULL
);

-- Criação da tabela Cidade
CREATE TABLE Cidade (
    Origem VARCHAR(100),
    Destino VARCHAR(100),
    PRIMARY KEY (Origem, Destino)
);

-- Criação da tabela Horario
CREATE TABLE Horario (
    Data_Hora_Chegada TIMESTAMP WITHOUT TIME ZONE,
    Data_Hora_Partida TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (Data_Hora_Chegada, Data_Hora_Partida)
);

-- Criação da tabela Rotas
CREATE TABLE Rotas (
    Origem VARCHAR(100),
    Destino VARCHAR(100),
    Distancia DECIMAL(10,2) NOT NULL,
    Preco DECIMAL(10,2) NOT NULL ,
    FOREIGN KEY (Origem, Destino) REFERENCES Cidade(Origem, Destino),
    PRIMARY KEY (Origem, Destino)
);

-- Criação da tabela Veiculos
CREATE TABLE Veiculos (
    Placa VARCHAR(10) PRIMARY KEY,
    Modelo VARCHAR(50) NOT NULL,
    Ano INT NOT NULL,
    Status_vei VARCHAR(20) CHECK (Status_vei IN ('disponivel', 'em manutencao')) NOT NULL,
    Capacidade INT NOT NULL
);

-- Criação da tabela Compra
CREATE TABLE Compra (
    CPF VARCHAR(11),
    Data_Hora_Chegada TIMESTAMP WITHOUT TIME ZONE,
    Data_Hora_Partida TIMESTAMP WITHOUT TIME ZONE,
    Assento INT NOT NULL,
    Status_ag VARCHAR(20) CHECK (Status_ag IN ('confirmado', 'cancelado', 'realizado')) NOT NULL,
    FOREIGN KEY (CPF) REFERENCES Cliente(CPF),
    FOREIGN KEY (Data_Hora_Chegada, Data_Hora_Partida) REFERENCES Horario(Data_Hora_Chegada, Data_Hora_Partida),
    PRIMARY KEY (CPF, Data_Hora_Chegada, Data_Hora_Partida)
);

-- Criação da tabela Possui
CREATE TABLE Possui (
    Data_Hora_Chegada TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    Data_Hora_Partida TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	Origem VARCHAR(100) NOT NULL,
    Destino VARCHAR(100) NOT NULL,
    FOREIGN KEY (Data_Hora_Chegada, Data_Hora_Partida) REFERENCES Horario(Data_Hora_Chegada, Data_Hora_Partida),
	FOREIGN KEY (Origem, Destino) REFERENCES Rotas(Origem, Destino),
    PRIMARY KEY (Data_Hora_Chegada, Data_Hora_Partida, Origem, Destino)
);
--Criação da tabela Realizado_por
CREATE TABLE Realizado_por (
    Placa VARCHAR(10) NOT NULL,
    Origem VARCHAR(100) NOT NULL,
    Destino VARCHAR(100) NOT NULL,
    FOREIGN KEY (Placa) REFERENCES Veiculos(Placa),
    FOREIGN KEY (Origem, Destino) REFERENCES Rotas(Origem, Destino),
	PRIMARY KEY (Placa, Origem, Destino)
);

CREATE OR REPLACE FUNCTION verificar_capacidade_assento() RETURNS TRIGGER AS $$
DECLARE
    capacidade_veiculo INT;
BEGIN
	
    -- Busca a capacidade do veículo usando as junções necessárias
    SELECT Veiculos.capacidade INTO capacidade_veiculo
    FROM Horario h NATURAL
    JOIN Possui  NATURAL JOIN Realizado_por  NATURAL JOIN Veiculos 
    WHERE h.Data_Hora_Chegada = NEW.Data_Hora_Chegada AND h.Data_Hora_Partida = NEW.Data_Hora_Partida;

    -- Verifica se o assento escolhido é menor ou igual à capacidade do veículo
  	IF capacidade_veiculo IS NULL THEN
    RAISE EXCEPTION 'Capacidade do veículo não encontrada ou veículo não existe.';
    ELSIF NEW.Assento > capacidade_veiculo THEN
        RAISE EXCEPTION 'O número do assento % é maior que a capacidade do veículo, que é %.', NEW.Assento, capacidade_veiculo;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER verificar_capacidade_antes_insercao
BEFORE INSERT OR UPDATE ON Compra
FOR EACH ROW EXECUTE FUNCTION verificar_capacidade_assento();




-------------------------------------------------------------------------------------------------
/* testes
-- Inserindo dados na tabela Cliente
INSERT INTO Cliente (CPF, Nome, Endereco, Telefone, Email) VALUES
('12345678901', 'João Silva', 'Rua das Flores, 123', '11987654321', 'joao.silva@email.com'),
('23456789012', 'Maria Oliveira', 'Avenida Central, 456', '21976543210', 'maria.oliveira@email.com');

-- Inserindo dados na tabela Cidade
INSERT INTO Cidade (Origem, Destino) VALUES
('São Paulo', 'Rio de Janeiro'),
('Rio de Janeiro', 'São Paulo');

-- Inserindo dados na tabela Horario
INSERT INTO Horario (Data_Hora_Chegada, Data_Hora_Partida) VALUES
('2024-04-20 12:00:00', '2024-04-20 07:00:00'),
('2024-04-21 12:00:00', '2024-04-21 07:00:00');

-- Inserindo dados na tabela Rotas
INSERT INTO Rotas (Origem, Destino, Distancia, Preco) VALUES
('São Paulo', 'Rio de Janeiro', 430.00, 120.00),
('Rio de Janeiro', 'São Paulo', 430.00, 120.00);

-- Inserindo dados na tabela Veiculos
INSERT INTO Veiculos (Placa, Modelo, Ano, Status_vei, Capacidade) VALUES
('XYZ1234', 'Volvo Bus', 2020, 'disponivel', 40),
('ABC5678', 'Mercedes Sprinter', 2021, 'em manutencao', 20);

-- Inserindo dados na tabela Compra (aqui vamos inserir um teste que deveria ser bloqueado pela trigger se o assento for maior do que a capacidade)
-- Certifique-se de que a trigger está ativada para fazer este teste
INSERT INTO Compra (CPF, Data_Hora_Chegada, Data_Hora_Partida, Assento, Status_ag) VALUES
('12345678901', '2024-04-20 12:00:00', '2024-04-20 07:00:00', 40, 'confirmado');
INSERT INTO Compra (CPF, Data_Hora_Chegada, Data_Hora_Partida, Assento, Status_ag) VALUES
('23456789012', '2024-04-21 12:00:00', '2024-04-21 07:00:00', 50, 'confirmado');

-- Inserindo dados na tabela Possui
INSERT INTO Possui (Data_Hora_Chegada, Data_Hora_Partida, Origem, Destino) VALUES
('2024-04-20 12:00:00', '2024-04-20 07:00:00', 'São Paulo', 'Rio de Janeiro');
INSERT INTO Possui (Data_Hora_Chegada, Data_Hora_Partida, Origem, Destino) VALUES
('2024-04-21 12:00:00', '2024-04-21 07:00:00', 'Rio de Janeiro', 'São Paulo');

-- Inserindo dados na tabela Realizado_por
INSERT INTO Realizado_por (Placa, Origem, Destino) VALUES
('XYZ1234', 'São Paulo', 'Rio de Janeiro');
INSERT INTO Realizado_por (Placa, Origem, Destino) VALUES
('ABC5678', 'Rio de Janeiro', 'São Paulo');

*/
/*teste
DELETE FROM compra 
SELECT * FROM compra
SELECT * FROM veiculos

SELECT *
    FROM Compra  NATURAL JOIN Horario  NATURAL
    JOIN Possui  NATURAL JOIN Realizado_por  NATURAL JOIN Veiculos 
	
SELECT *
    FROM Compra  NATURAL JOIN Horario
	SELECT Veiculos.capacidade
    FROM Horario NATURAL
    JOIN Possui  NATURAL JOIN Realizado_por  NATURAL JOIN Veiculos NATURAL JOIN compra
	
SELECT Veiculos.capacidade
    FROM Horario NATURAL
    JOIN Possui  NATURAL JOIN Realizado_por  NATURAL JOIN Veiculos 
*/