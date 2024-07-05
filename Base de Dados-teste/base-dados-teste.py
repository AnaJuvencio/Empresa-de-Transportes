import psycopg2 #para fazer a conexão com o bd
from faker import Faker #gerar dados 
import random
from random import randint, choice
from datetime import datetime
import csv
from datetime import timedelta

#OBS: 
# 1º Precisa verificar se está inserindo as datas corretamente, coloquei oq é pra ser a estrutura correta
# 2º Verificar se está respeitando as duas triggers 
# 3º Verificar se está violando a restrição de integridade referencial
# 4º Criar mecanismo que tente gerar os dados novamente em caso de erro de inserção (por segurança)
#5º Verificar a capacidade, 4?

# Conexão com o banco de dados
conn = psycopg2.connect(
    dbname="empresa_de_transportes",
    user="postgres",
    password="0113",
    host="localhost",
    port="5432"
)

# Cursor
cur = conn.cursor()

# Criar uma instância do Faker com suporte para dados brasileiros
fake = Faker(['pt_BR'])

# Função para inserir dados 
def inserir_dados(tabela, dados):
    try:
        cur.execute(f"INSERT INTO {tabela} VALUES ({', '.join(['%s'] * len(dados))})", dados)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Erro ao inserir dados na tabela {tabela}: {e}")
        conn.rollback()

# Inserção de dados na tabela Cliente
for _ in range(2):
    cpf = fake.unique.random_number(digits=11)
    nome = fake.name()
    endereco = fake.address()
    telefone = fake.phone_number()
    email = fake.email()
    inserir_dados("Cliente", (cpf, nome, endereco, telefone, email))

def carregar_cidades(municipios_test):
    with open(municipios_test, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        municipios =[row[-1].strip() for row in reader]   # Pegar o último elemento de cada linha (após a vírgula) e remover espaços em branco extras
    return municipios

municipios = carregar_cidades('C:/Users/Beatriz/OneDrive/Documentos/UFSCar/2024-1/sbd/sbd-Empresa-de-Transportes/Base de Dados-teste/municipios_test.csv')

for cidade in municipios:  # Iterar sobre a lista de municípios
    inserir_dados("Cidade", (cidade,))
     
# Inserção de dados na tabela Cidade
for _ in range(2): #4430
    nome_cidade = fake.city()
    inserir_dados("Cidade", (nome_cidade,))


# Inserção de dados na tabela Horario
# Gerar dados realistas para a tabela Horario
horarios = set()

while len(horarios) < 6:
    # Gerar uma data de partida aleatória dentro dos próximos 60 dias
    data_hora_partida = fake.date_time_between(start_date='now', end_date='+60d')
    
    # A duração da viagem pode variar de 1 a 12 horas
    duracao_viagem = timedelta(hours=random.randint(1, 12))
    
    # A data de chegada é a data de partida mais a duração da viagem
    data_hora_chegada = data_hora_partida + duracao_viagem
    
    # Adicionar o horário à coleção de horários se for único
    if (data_hora_chegada, data_hora_partida) not in horarios:
        horarios.add((data_hora_chegada, data_hora_partida))
        inserir_dados("Horario", (data_hora_chegada, data_hora_partida))

# Função para carregar marcas de carros de um arquivo CSV
def carregar_marcas(marcas_carros_test):
    with open(marcas_carros_test, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        marcas = [row[0] for row in reader]
    return marcas

# Função para carregar modelos de carros de um arquivo CSV
def carregar_modelos(modelos_carro_test):
    with open(modelos_carro_test, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        modelos = [row[0] for row in reader]
    return modelos

# Carregar marcas de carros e modelos de carros dos arquivos CSV
marcas_carros = carregar_marcas('C:/Users/Beatriz/OneDrive/Documentos/UFSCar/2024-1/sbd/sbd-Empresa-de-Transportes/Base de Dados-teste/marcas_carros_test.csv')
modelos_carro = carregar_modelos('C:/Users/Beatriz/OneDrive/Documentos/UFSCar/2024-1/sbd/sbd-Empresa-de-Transportes/Base de Dados-teste/modelos_carro_test.csv')

# Conjunto para rastrear as combinações únicas de marca e modelo de veículos
veiculos_gerados = set()

# Inserção de dados na tabela Veiculos
while len(veiculos_gerados) < 5:  # Gerar 10000 registros de veículos únicos
    placa = fake.license_plate()  # Gerar uma placa falsa aleatória
    marca = random.choice(marcas_carros)  # Escolher uma marca de carro aleatória
    modelo = random.choice(modelos_carro)  # Escolher um modelo de carro aleatório
    ano = random.randint(1900, 2024)  # Gerar um ano de fabricação aleatório entre 2010 e 2023
    status_vei = random.choice(["disponivel", "em manutencao"])  # Escolher um status aleatório
    capacidade = 65  # Gerar uma capacidade aleatória entre 1 e 60
    
    veiculo = f"{marca} {modelo}"  # Concatenar marca e modelo do veículo
    
    # Verificar se a combinação de marca e modelo já foi gerada
    if veiculo not in veiculos_gerados:
        # Inserir os dados na tabela Veiculos
        inserir_dados("Veiculos", (placa, veiculo, ano, status_vei, capacidade))
        veiculos_gerados.add(veiculo)  # Adicionar a combinação à lista de veículos gerados


# Inserção de dados na tabela Rotas
# Consulta para selecionar todas as cidades da tabela Cidade
cur.execute("SELECT Nome_Cidade FROM Cidade")
# Recuperar todas as cidades da consulta
cidades = [row[0] for row in cur.fetchall()]

# Consulta para selecionar todas as placas da tabela Veiculos
cur.execute("SELECT Placa FROM Veiculos")
# Recuperar todas as placas da consulta
placas = [row[0] for row in cur.fetchall()]

for _ in range(2):
    # Selecionar cidades aleatórias de origem e destino
    nome_cidade_origem = random.choice(cidades)
    nome_cidade_destino = random.choice(cidades)

    # Garantir que as cidades de origem e destino sejam diferentes
    while nome_cidade_origem == nome_cidade_destino:
        nome_cidade_destino = random.choice(cidades)

    # Selecionar uma placa aleatória
    placa = random.choice(placas)
    # Gerar distância e preço aleatórios
    distancia = randint(100, 1000)
    preco = randint(50, 200)

    # Inserir dados na tabela Rotas
    inserir_dados("Rotas", (nome_cidade_origem, nome_cidade_destino, distancia, preco, placa))
    

tentativas = 0
insercoes_bem_sucedidas = 0
# Tabela Disponibilidade
for _ in range(2):  # Altere o valor dentro do range para o número desejado de inserções
    # Para cada linha a ser inserida, precisamos garantir que os dados sejam únicos
    while True:
        # Consulta para obter um horário existente na tabela Horario
        cur.execute("SELECT data_hora_chegada, data_hora_partida FROM Horario ORDER BY RANDOM() LIMIT 1")
        data_hora_chegada, data_hora_partida = cur.fetchone()

        # Consulta para obter cidades de origem e destino existentes na tabela Rotas
        cur.execute("SELECT Nome_Cidade_Origem, Nome_Cidade_Destino FROM Rotas ORDER BY RANDOM() LIMIT 1")
        nome_cidade_origem, nome_cidade_destino = cur.fetchone()

        # Verificar se essa combinação de dados já existe na tabela Disponibilidade
        cur.execute("SELECT COUNT(*) FROM Disponibilidade WHERE data_hora_chegada = %s AND data_hora_partida = %s AND nome_cidade_origem = %s AND nome_cidade_destino = %s", (data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino))
        if cur.fetchone()[0] == 0:  # Se não houver registros com essa combinação de dados
            tentativas += 1
            # Inserir os dados na tabela Disponibilidade
            inserir_dados("Disponibilidade", (data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino))
            insercoes_bem_sucedidas += 1
            break  # Sai do loop while

        
# Tabela Compra
tentativas_compra = 0
insercoes_bem_sucedidas_compra = 0
for _ in range(2):  # Altere o valor dentro do range para o número desejado de inserções
    # Para cada linha a ser inserida, precisamos garantir que os dados sejam únicos
    while True:
        # Consulta para obter um CPF existente na tabela Cliente
        cur.execute("SELECT cpf FROM Cliente ORDER BY RANDOM() LIMIT 1")
        cpf_cliente = cur.fetchone()[0]

        # Consulta para obter uma disponibilidade existente na tabela Disponibilidade
        cur.execute("SELECT data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino FROM Disponibilidade ORDER BY RANDOM() LIMIT 1")
        data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino = cur.fetchone()

        # Gerar um número de assento aleatório entre 1 e 650
        assento = randint(1, 65)

        # Escolher um status de compra aleatório entre "confirmado", "cancelado" e "realizado"
        status_ag = choice(["confirmado", "cancelado", "realizado"])

        # Verificar se essa combinação de dados já existe na tabela Compra
        cur.execute("SELECT COUNT(*) FROM Compra WHERE cpf = %s AND data_hora_chegada = %s AND data_hora_partida = %s AND assento = %s", (cpf_cliente, data_hora_chegada, data_hora_partida, assento))
        if cur.fetchone()[0] == 0:  # Se não houver registros com essa combinação de dados
            tentativas_compra += 1
            # Inserir os dados na tabela Compra
            inserir_dados("Compra", (cpf_cliente, data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino, assento, status_ag))
            insercoes_bem_sucedidas_compra += 1
            break  # Sai do loop while


print(f"Tentativas de inserção em Disponibilidade: {tentativas}")
print(f"Inserções bem-sucedidas da tabela Disponibilidade: {insercoes_bem_sucedidas}")
print(f"Tentativas de inserção em compra: {tentativas_compra}")
print(f"Inserções bem-sucedidas da tabela compra: {insercoes_bem_sucedidas_compra}")
print('Inserção completa!')

# Fechar conexão e cursor
cur.close()
conn.close()


# Inserção de dados na tabela Rotas
#for _ in range(1):
#    nome_cidade_origem = fake.random.choice([row[0] for row in cur.execute("SELECT nome_cidade FROM Cidade")])
#    nome_cidade_destino = fake.random.choice([row[0] for row in cur.execute("SELECT nome_cidade FROM Cidade")])
#    while nome_cidade_origem == nome_cidade_destino:  # Garante que as cidades de origem e destino sejam diferentes
#        nome_cidade_destino = fake.random.choice([row[0] for row in cur.execute("SELECT nome_cidade FROM Cidade")])
#    distancia = randint(100, 1000)
#    preco = randint(50, 200)
#    inserir_dados("Rotas", (nome_cidade_origem, nome_cidade_destino, distancia, preco))

# Inserção de dados na tabela Veiculos
#for _ in range(1):
#    placa = fake.unique.license_plate()
#    modelo = fake.car_make() #dando erro
#    ano = fake.random.randint(2010, 2023)
#    status_vei = fake.random.choice(["disponivel", "em manutencao"])
#    capacidade = randint(1, 60)
#    inserir_dados("Veiculos", (placa, modelo, ano, status_vei, capacidade))

# Inserção de dados na tabela Possui
#for _ in range(2):
#    # Executar a consulta no banco de dados
#    cur.execute("SELECT Data_Hora_Chegada, Data_Hora_Partida, Nome_Cidade_Origem, Nome_Cidade_Destino FROM Horario, Rotas")
#    # Buscar todos os resultados da consulta
#    rows = cur.fetchall()
#    # Usar o fake.random.choice() para selecionar aleatoriamente uma linha dos resultados
#    data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino = fake.random.choice(rows)
#    # Inserir os dados na tabela Possui
#    inserir_dados("Possui", (data_hora_chegada, data_hora_partida, nome_cidade_origem, nome_cidade_destino))


# Inserção de dados na tabela Realizado_por
#for _ in range(2):
#    # Executar a consulta para obter as placas dos veículos
#    cur.execute("SELECT Placa FROM Veiculos")
#    placas = [row[0] for row in cur.fetchall()]
#    # Selecionar aleatoriamente uma placa
#    placa = fake.random.choice(placas)
#    # Executar a consulta para obter os nomes das cidades de origem e destino das rotas
#    cur.execute("SELECT Nome_Cidade_Origem, Nome_Cidade_Destino FROM Rotas")
#    rows = cur.fetchall()
#    # Selecionar aleatoriamente um par de cidades de origem e destino
#    nome_cidade_origem, nome_cidade_destino = fake.random.choice(rows)
#    # Inserir os dados na tabela Realizado_por
#   inserir_dados("Realizado_por", (placa, nome_cidade_origem, nome_cidade_destino))

# Inserção de dados na tabela Compra
#for _ in range(1):
#    cpf = fake.unique.random_number(digits=11)
#    data_hora_chegada = fake.future_datetime(end_date='+30d')
#    data_hora_partida = fake.date_time_between(start_date=data_hora_chegada, end_date=data_hora_chegada)
#    assento = randint(1, 50)
#    status_ag = fake.random.choice(["confirmado", "cancelado", "realizado"])
#    inserir_dados("Compra", (cpf, data_hora_chegada, data_hora_partida, assento, status_ag))