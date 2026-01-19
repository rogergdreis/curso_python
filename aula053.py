"""
enumerate - enumera iteráveis (índices)
"""

lista = ['Maria', 'Helena', 'Luiz']
lista.append('João')

for i, nome in enumerate(lista):
    print(i, nome)