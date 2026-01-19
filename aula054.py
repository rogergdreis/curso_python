"""
Faça uma lista de compras com listas

O usuário deve ter a possilidade de
inserir, apagar e listar valores de sua lista.
Não permita que o program quebre com
erros de índices inexistentes na lista.
"""

import os

lista = []
while True:
    print('Selecine uma opção')
    opcao = input('[i]inserir [a]apagar [l]listar: ')

    if opcao == 'i':
        os.system('clear')

        valor = input('Valor: ')
        lista.append(valor)
    elif opcao == 'a':
        indice_str = input('Escolha o índice para apagar: ')

        try:
            indice = int(indice_str)
            del lista[indice]
        except ValueError:
            print('Por favor digite um número inteiro.')
        except IndexError:
            print('Índice não exite na lista.')
        except Exception:
            print('Erro desconhecido.')

    elif opcao == 'l':
        os.system('clear')

        if len(lista) == 0:
            print('Nada para listar')

        for i, valor in enumerate(lista):
            print(i, valor)

    else:
        os.system('clear')
        print('Por favor, escolha i, a ou l.')