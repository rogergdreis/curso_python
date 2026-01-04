"""
Faça um programa que peça ao usuário para digitar um número inteiro,
informe se este número é par ou ímpar. Caso o usuário não digite um número
inteiro, informe que não é um número inteiro.
"""

# entrada = input('Digite um número: ')

# if entrada.isdigit():
#     entrada_int = int(entrada)
#     par_impar = entrada_int % 2 == 0
#     par_impar_texto = 'ímpar'

#     if par_impar:
#         par_impar_texto = 'par'

#     print(f'O número{entrada_int} é {par_impar_texto}')
# else:
#     print('Você não digitou um número inteiro')

########################################################################

# try:
#     n = input('Digite um número inteiro: ')
#     n = int(n)

#     if n % 2 == 0:
#         print('O número é par')
#     else:
#         print('O número é ímpar')
# except:
#     print('Isso não é um número inteiro')

"""
Faça um programa que pergunte ao usuário e, baseando-se no horário
descrito, exiba a saudação apropriada. Ex.:
Bom dia 0-11, Boa tarde 12-17 e Boa noite 18-23.
"""

# try:
#     hora = input('Digite o horario: ')
#     hora = int(hora)

#     if hora <= 11:
#         print('Bom dia!')
#     elif hora <=17:
#         print('Boa tarde!')
#     elif hora <= 23:
#         print('Boa noite!')
#     else:
#         print('Informe um horario valido.')
# except:
#     print('Informe um horario valido.')

"""
Faça um programa que peça o primeiro nome do usuário. Se o nome tiver 4 letras ou
menos escreva "Seu nome é curto"; se tiver entre 5 e 6 letras, escreva
"Seu nome é normal"; maior que 6 escreva "Seu nome é muito grande".
"""

nome = input('Digite seu primero nome: ')

if len(nome) <= 4:
    print('Seu nome é curto')
elif len(nome) <= 6:
    print('Seu nome é normal')
else:
    print('Seu nome é muito grande')