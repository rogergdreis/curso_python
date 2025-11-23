"""
Interpolação básica de strings
s - string
d e i - int
f - float
x e X - Hexadecimal
"""

nome = 'Luiz'
preco = 1000.95897643
variavel = '%s, o preço é R$%.2f' % (nome, preco)
print(variavel)
print('O hexadcimal de %d é %04x' % (1500, 1500))
