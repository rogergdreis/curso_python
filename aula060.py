"""
Operação ternária (condicional de uma linha)
<valor> if <condição> else <outro valor>
"""
digito = 9
novo_digito = digito if digito <= 9 else 0
print(novo_digito)

print('Valor' if True else 'Outro valor' if True else 'Fim')