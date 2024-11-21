# Empresa-de-Transportes

Quantidade de linhas por tabela:\
Cliente - 10.000 linhas\
Disponibilidade - 100.000 linhas\
Compra - 994.584 linhas\
Veiculos - .10.000 linhas\
Rotas - 9.998 linhas\
Horario - 10.000 linhas\
Cidade - 7.171 linhas

# Inserção de Dados em Banco de Dados PostgreSQL

Este script gera e insere dados falsos em várias tabelas de um banco de dados PostgreSQL utilizando a biblioteca Faker para dados brasileiros. O script garante a integridade referencial e aplica várias restrições para manter a consistência dos dados.

## Tópicos do Script

1. **Importação de Bibliotecas:**
   - `psycopg2` para conectar ao banco de dados PostgreSQL.
   - `Faker` para gerar dados falsos.
   - `random` e `datetime` para gerar dados aleatórios e manipular datas.
   - `csv` para ler arquivos CSV.

2. **Conexão com o Banco de Dados:**
   - Estabelece uma conexão com o banco de dados PostgreSQL utilizando credenciais específicas.
   - Cria um cursor para executar comandos SQL.

3. **Instância do Faker:**
   - Cria uma instância do Faker configurada para gerar dados no formato brasileiro.

4. **Função para Inserir Dados:**
   - Define uma função que insere dados em uma tabela específica.
   - Em caso de erro, a transação é revertida e uma mensagem de erro é exibida.

5. **Inserção de Dados na Tabela `Cliente`:**
   - Gera 10.000 registros falsos para clientes com campos como CPF, nome, endereço, telefone e email.
   - **Regras:** Cada cliente deve ter um CPF único e válido.

6. **Função para Carregar Cidades de um Arquivo CSV:**
   - Define uma função que carrega os nomes das cidades de um arquivo CSV.

7. **Carregar Cidades e Inserir na Tabela `Cidade`:**
   - Carrega as cidades de um arquivo CSV e insere esses dados na tabela `Cidade`.
   - **Regras:** Cada cidade deve ter um nome único.

8. **Inserção de Dados na Tabela `Horario`:**
   - Gera 10.000 registros únicos de horários com data/hora de partida e chegada.
   - **Regras:** 
     - As combinações de data/hora de chegada e partida devem ser únicas.
     - A data/hora de partida deve ser menor que a data/hora de chegada.

9. **Funções para Carregar Marcas e Modelos de Carros de Arquivos CSV:**
   - Define funções para carregar listas de marcas e modelos de carros de arquivos CSV.

10. **Carregar Marcas e Modelos de Carros e Inserir na Tabela `Veiculos`:**
    - Carrega marcas e modelos de carros e insere 10.000 registros únicos na tabela `Veiculos`.
    - **Regras:** 
      - Cada veículo deve ter uma combinação única de marca e modelo.
      - A placa deve ser única.

11. **Inserção de Dados na Tabela `Rotas`:**
    - Seleciona aleatoriamente cidades e placas de veículos e insere aproximadamente 10.000 registros na tabela `Rotas`.
    - **Regras:**
      - As cidades de origem e destino devem ser diferentes.

12. **Inserção de Dados na Tabela `Disponibilidade`:**
    - Gera 100.000 registros únicos de disponibilidade, garantindo que cada combinação de horário e rota seja única.
    - **Regras:** 
      - As combinações de data/hora de chegada, partida e cidades de origem e destino devem ser únicas.
      - Os dados de disponibilidade devem referenciar horários e rotas válidos.

13. **Inserção de Dados na Tabela `Compra`:**
    - Gera aproximadamente 1.000.000 registros únicos de compra, garantindo que cada combinação de cliente e disponibilidade seja única.
    - **Regras:** 
      - As combinações de CPF do cliente e detalhes da disponibilidade (data/hora e cidades) devem ser únicas.
      - Os dados de compra devem referenciar uma disponibilidade existente.

14. **Fechar a Conexão:**
    - Fecha o cursor e a conexão com o banco de dados após a inserção de todos os dados.

## Regras Principais e Restrições para Cada Tabela

- **Cliente:**
  - **Regras:** 
    - CPF deve ser único e válido.
    - Campos: CPF, nome, endereço, telefone, email.

- **Cidade:**
  - **Regras:** 
    - Nome da cidade deve ser único.
    - Campo: Nome da cidade.

- **Horario:**
  - **Regras:** 
    - Combinações de data/hora de chegada e partida devem ser únicas.
    - A data/hora de partida deve ser menor que a data/hora de chegada.
    - Campos: Data/hora de chegada, data/hora de partida.

- **Veiculos:**
  - **Regras:** 
    - Placa deve ser única.
    - Combinações de marca e modelo devem ser únicas.
    - Campos: Placa, marca, modelo, ano, status, capacidade.

- **Rotas:**
  - **Regras:** 
    - Cidades de origem e destino devem ser diferentes.
    - Campos: Cidade de origem, cidade de destino, distância, preço, placa.

- **Disponibilidade:**
  - **Regras:** 
    - Combinações de data/hora de chegada, partida e cidades de origem e destino devem ser únicas.
    - Os dados de disponibilidade devem referenciar horários e rotas válidos.
    - Campos: Data/hora de chegada, data/hora de partida, cidade de origem, cidade de destino.

- **Compra:**
  - **Regras:** 
    - Combinações de CPF do cliente e detalhes da disponibilidade devem ser únicas.
    - Os dados de compra devem referenciar uma disponibilidade existente.
    - Campos: CPF do cliente, data/hora de chegada, data/hora de partida, cidade de origem, cidade de destino, assento, status de compra.
