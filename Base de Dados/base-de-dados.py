import psycopg2 #para fazer a conexão com o bd
from faker import Faker #gerar dados 
from random import randint
from datetime import datetime

#OBS: 
# 1º Precisa verificar se está inserindo as datas corretamente, coloquei oq é pra ser a estrutura correta
# 2º Verificar se está respeitando as duas triggers 
# 3º Verificar se está violando a restrição de integridade referencial
# 4º Criar mecanismo que tente gerar os dados novamente em caso de erro de inserção (por segurança)

# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname="empresa_de_transportes",
    user="seu_usuario",
    password="sua_senha",
    host="localhost",
    port="5432"
)

# Cursor
cur = conn.cursor()

# Faker para gerar dados falsos
fake = Faker()

# Função para inserir dados 
def inserir_dados(tabela, dados):
    try:
        cur.execute(f"INSERT INTO {tabela} VALUES ({', '.join(['%s'] * len(dados))})", dados)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados na tabela {tabela}: {e}")
        conn.rollback()

# Inserção de dados na tabela Cliente
for _ in range(10):
    cpf = fake.unique.random_number(digits=11)
    nome = fake.name()
    endereco = fake.address()
    telefone = fake.phone_number()
    email = fake.email()
    inserir_dados("Cliente", (cpf, nome, endereco, telefone, email))

# Inserção de dados na tabela Cidade
for _ in range(10):
    nome_cidade = fake.city()
    inserir_dados("Cidade", (nome_cidade,))

# Inserção de dados na tabela Horario
for _ in range(10):
    data_hora_chegada = fake.future_datetime(end_date='+30d').strftime('%Y-%m-%d %H:%M:%S')
    data_hora_partida = fake.date_time_between(start_date=data_hora_chegada, end_date=data_hora_chegada).strftime('%Y-%m-%d %H:%M:%S')
    inserir_dados("Horario", (data_hora_chegada, data_hora_partida))

# Inserção de dados na tabela Rotas
for _ in range(10):
    nome_cidade_origem = fake.random.choice([row[0] for row in cur.execute("SELECT Nome_Cidade FROM Cidade")])
    nome_cidade_destino = fake.random.choice([row[0] for row in cur.execute("SELECT Nome_Cidade FROM Cidade")])
    while nome_cidade_origem == nome_cidade_destino:  # Garante que as cidades de origem e destino sejam diferentes
        nome_cidade_destino = fake.random.choice([row[0] for row in cur.execute("SELECT Nome_Cidade FROM Cidade")])
    distancia = randint(100, 1000)
    preco = randint(50, 200)
    inserir_dados("Rotas", (nome_cidade_origem, nome_cidade_destino, distancia, preco))

# Inserção de dados na tabela Veiculos
for _ in range(5):
    placa = fake.unique.license_plate()
    modelo = fake.car_model()  
    ano = fake.random.randint(2010, 2023)
    status_vei = fake.random.choice(["disponivel", "em manutencao"])
    capacidade = randint(1, 60)
    inserir_dados("Veiculos", (placa, modelo, ano, status_vei, capacidade))

# Inserção de dados na tabela Compra
for _ in range(10):
    cpf = fake.unique.random_number(digits=11)
    data_hora_chegada = fake.future_datetime(end_date='+30d').strftime('%Y-%m-%d %H:%M:%S')
    data_hora_partida = fake.date_time_between(start_date=data_hora_chegada, end_date=data_hora_chegada).strftime('%Y-%m-%d %H:%M:%S')
    assento = randint(1, 59)
    status_ag = fake.random.choice(["confirmado", "cancelado", "realizado"])
    inserir_dados("Compra", (cpf, data_hora_chegada, data_hora_partida, assento, status_ag))

# Inserção de dados na tabela Possui
for _ in range(10):
    data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino = fake.random.choice([row for row in cur.execute("SELECT Data_Hora_Chegada, Data_Hora_Partida, Nome_Cidade_Origem, Nome_Cidade_Destino FROM Horario, Rotas")])
    inserir_dados("Possui", (data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino))

# Inserção de dados na tabela Realizado_por
for _ in range(10):
    placa = fake.random.choice([row[0] for row in cur.execute("SELECT Placa FROM Veiculos")])
    nome_cidade_origem, nome_cidade_destino = fake.random.choice([row for row in cur.execute("SELECT Nome_Cidade_Origem, Nome_Cidade_Destino FROM Rotas")])
    inserir_dados("Realizado_por", (placa, nome_cidade_origem, nome_cidade_destino))

# Fechar conexão e cursor
cur.close()
conn.close()
