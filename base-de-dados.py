import psycopg2 #para fazer a conexão com o bd
from faker import Faker #gerar dados 
from random import randint
from datetime import datetime

#OBS: 
# 1º Precisa verificar se está inserindo as data corretamente, na tabela Horário coloquei um exemplo de como ficaria, mas precisa ver se nas outras tabela tbm está certo;
# 2º O try Exception foi inserido por conta da trigger em compra
# 3º Verificar se está violando a restrição de integridade referencial
  
# Conectando ao banco de dados
conn = psycopg2.connect(
    dbname="empresa_de_transportes",
    user="seu_usuario",
    password="sua_senha",
    host="localhost",
    port="5432"
)

# Criando um cursor
cur = conn.cursor()

# Instanciando o Faker
fake = Faker()

# Inserindo dados na tabela Cliente
for _ in range(10):
    cpf = fake.unique.random_number(digits=11)
    nome = fake.name()
    endereco = fake.address()
    telefone = fake.phone_number()
    email = fake.email()
    
    cur.execute("INSERT INTO Cliente (CPF, Nome, Endereco, Telefone, Email) VALUES (%s, %s, %s, %s, %s)",
                (cpf, nome, endereco, telefone, email))

# Inserindo dados na tabela Cidade
for _ in range(10):
    origem = fake.city()
    destino = fake.city()
    
    cur.execute("INSERT INTO Cidade (Origem, Destino) VALUES (%s, %s)", (origem, destino))

# Inserindo dados na tabela Horario
for _ in range(10):
    data_hora_chegada = fake.future_datetime(end_date='+30d').strftime('%Y-%m-%d %H:%M:%S') #"YYYY-MM-DD HH:MM:SS"
    data_hora_partida = fake.date_time_between(start_date=data_hora_chegada, end_date=data_hora_chegada).strftime('%Y-%m-%d %H:%M:%S')
    
    cur.execute("INSERT INTO Horario (Data_Hora_Chegada, Data_Hora_Partida) VALUES (%s, %s)",
                (data_hora_chegada, data_hora_partida))

# Inserindo dados na tabela Rotas
for _ in range(10):
    origem, destino = fake.random.choice([row for row in cur.execute("SELECT Origem, Destino FROM Cidade")])
    distancia = randint(100, 1000)
    preco = randint(50, 200)
    
    cur.execute("INSERT INTO Rotas (Origem, Destino, Distancia, Preco) VALUES (%s, %s, %s, %s)",
                (origem, destino, distancia, preco))

# Inserindo dados na tabela Veiculos
for _ in range(5):
    placa = fake.unique.license_plate()
    modelo = fake.car_model()  
    ano = fake.random.randint(2010, 2023)
    status_vei = fake.random.choice(["disponivel", "em manutencao"])
    capacidade = randint(1, 10)
    
    cur.execute("INSERT INTO Veiculos (Placa, Modelo, Ano, Status_vei, Capacidade) VALUES (%s, %s, %s, %s, %s)",
                (placa, modelo, ano, status_vei, capacidade))

# Inserindo dados na tabela Compra
for _ in range(10):
    cpf = fake.unique.random_number(digits=11)
    data_hora_chegada = fake.future_datetime(end_date='+30d').strftime('%Y-%m-%d %H:%M:%S')
    data_hora_partida = fake.date_time_between(start_date=data_hora_chegada, end_date=data_hora_chegada).strftime('%Y-%m-%d %H:%M:%S')
    assento = randint(1, 50)
    status_ag = fake.random.choice(["confirmado", "cancelado", "realizado"])
    
    try: #respeita a trigger verificar_capacidade_antes_insercao
        cur.execute("INSERT INTO Compra (CPF, Data_Hora_Chegada, Data_Hora_Partida, Assento, Status_ag) VALUES (%s, %s, %s, %s, %s)",
                    (cpf, data_hora_chegada, data_hora_partida, assento, status_ag))
        conn.commit()  # Commit se não houver exceção
    except psycopg2.Error as e:
        print("Erro ao inserir compra:", e)
        conn.rollback()  # Desfaz qualquer operação pendente
        
# Inserindo dados na tabela Possui
for _ in range(10):
    data_hora_chegada, data_hora_partida, origem, destino = fake.random.choice([row for row in cur.execute("SELECT Data_Hora_Chegada, Data_Hora_Partida, Origem, Destino FROM Horario, Rotas")])
    
    cur.execute("INSERT INTO Possui (Data_Hora_Chegada, Data_Hora_Partida, Origem, Destino) VALUES (%s, %s, %s, %s)",
                (data_hora_chegada, data_hora_partida, origem, destino))

# Inserindo dados na tabela Realizado_por
for _ in range(10):
    placa = fake.random.choice([row[0] for row in cur.execute("SELECT Placa FROM Veiculos")])
    origem, destino = fake.random.choice([row for row in cur.execute("SELECT Origem, Destino FROM Rotas")])
    
    cur.execute("INSERT INTO Realizado_por (Placa, Origem, Destino) VALUES (%s, %s, %s)",
                (placa, origem, destino))

conn.commit() #literalmente insere no bd
cur.close() #fecha o cursor que se comunica com o bd
conn.close() # economizar recursos
