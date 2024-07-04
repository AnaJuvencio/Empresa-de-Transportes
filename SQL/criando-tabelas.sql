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
    Nome_Cidade VARCHAR(100),
    PRIMARY KEY (Nome_Cidade)
);

-- Criação da tabela Horario
CREATE TABLE Horario (
    Data_Hora_Chegada TIMESTAMP WITHOUT TIME ZONE,
    Data_Hora_Partida TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY (Data_Hora_Chegada, Data_Hora_Partida)
);

-- Criação da tabela Veiculos
CREATE TABLE Veiculos (
    Placa VARCHAR(10) PRIMARY KEY,
    Modelo VARCHAR(50) NOT NULL,
    Ano INT NOT NULL,
    Status_vei VARCHAR(20) CHECK (Status_vei IN ('disponivel', 'em manutencao')) NOT NULL,
    Capacidade INT NOT NULL
);

-- Criação da tabela Rotas
CREATE TABLE Rotas (
    Nome_Cidade_Origem VARCHAR(100),
    Nome_Cidade_Destino VARCHAR(100),
    Distancia DECIMAL(10,2) NOT NULL,
    Preco DECIMAL(10,2) NOT NULL ,
    Placa VARCHAR(10),
    FOREIGN KEY (Placa) REFERENCES Veiculos (Placa),
    FOREIGN KEY (Nome_Cidade_Origem) REFERENCES Cidade(Nome_Cidade),
    FOREIGN KEY (Nome_Cidade_Destino) REFERENCES Cidade(Nome_Cidade),
    PRIMARY KEY (Nome_Cidade_Origem, Nome_Cidade_Destino),
	CHECK (Nome_Cidade_Origem <> Nome_Cidade_Destino) -- Restrição de verificação
);

-- Criação da tabela Compra
CREATE TABLE Compra (
    CPF VARCHAR(11),
    Data_Hora_Chegada TIMESTAMP WITHOUT TIME ZONE,
    Data_Hora_Partida TIMESTAMP WITHOUT TIME ZONE,
    Nome_Cidade_Origem VARCHAR(100),
    Nome_Cidade_Destino VARCHAR(100),
    Assento INT NOT NULL,
    Status_ag VARCHAR(20) CHECK (Status_ag IN ('confirmado', 'cancelado', 'realizado')) NOT NULL,
    FOREIGN KEY (CPF) REFERENCES Cliente(CPF),
    FOREIGN KEY (Data_Hora_Chegada, Data_Hora_Partida) REFERENCES Horario(Data_Hora_Chegada, Data_Hora_Partida),
    FOREIGN KEY (Nome_Cidade_Origem, Nome_Cidade_Destino) REFERENCES Rotas(Nome_Cidade_Origem, Nome_Cidade_Destino),
    PRIMARY KEY (CPF, Data_Hora_Chegada, Data_Hora_Partida)
);


-- Criação da tabela Disponibilidade
CREATE TABLE Disponibilidade (
    Data_Hora_Chegada TIMESTAMP WITHOUT TIME ZONE,
    Data_Hora_Partida TIMESTAMP WITHOUT TIME ZONE,
    Nome_Cidade_Origem VARCHAR(100),
    Nome_Cidade_Destino VARCHAR(100),
    FOREIGN KEY (Data_Hora_Chegada, Data_Hora_Partida) REFERENCES Horario(Data_Hora_Chegada, Data_Hora_Partida),
    FOREIGN KEY (Nome_Cidade_Origem, Nome_Cidade_Destino) REFERENCES Rotas(Nome_Cidade_Origem, Nome_Cidade_Destino),
    PRIMARY KEY (Nome_Cidade_Origem, Nome_Cidade_Destino, Data_Hora_Chegada, Data_Hora_Partida)
);