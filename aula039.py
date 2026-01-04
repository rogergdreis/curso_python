"""
Iterando string com while
"""

nome = 'Luiz Otávio'  # Iteráveis
tamanho_nome = len(nome)
i = 0
nova_string = ''

while i < tamanho_nome:
    nova_string += f'*{nome[i:i+1]}'
    i += 1

nova_string += '*'
print(nova_string)