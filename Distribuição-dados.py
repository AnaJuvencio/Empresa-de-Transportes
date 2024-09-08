import matplotlib.pyplot as plt
import numpy as np

# Dados fornecidos
categorias = ['Cliente', 'Disponibilidade', 'Compra', 'Veiculos', 'Rotas', 'Horario', 'Cidade']
valores = [10000, 100000, 994584, 10000, 9998, 10000, 7171]

# Criar o gráfico de barras com escala logarítmica
plt.figure(figsize=(10, 6))  # Define o tamanho da figura
plt.bar(categorias, valores, color='skyblue')  # Cria o gráfico de barras

# Adicionar título e rótulos aos eixos
plt.title('Distribuição dos Dados na Tabela (Escala Logarítmica)')
plt.xlabel('Categoria')
plt.ylabel('Valor (Escala Logarítmica)')

# Aplicar a escala logarítmica no eixo Y
plt.yscale('log')

# Mostrar o gráfico
plt.show()
