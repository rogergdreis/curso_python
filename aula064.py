import random
import time

def gerar_cpfs(quantidade = int(input('Informe a quantidade de CPFs a serem gerados: '))):
    vetor_cpfs = []

    for _ in range(quantidade):
        nove_digitos = ''
        for i in range(9):
            nove_digitos += str(random.randint(0, 9))

        # Cálculo do primeiro dígito
        contador_regressivo_1 = 10
        resultado_digito_1 = 0
        for digito in nove_digitos:
            resultado_digito_1 += int(digito) * contador_regressivo_1
            contador_regressivo_1 -= 1
        digito_1 = (resultado_digito_1 * 10) % 11
        digito_1 = digito_1 if digito_1 <= 9 else 0

        # Cálculo do segundo dígito
        dez_digitos = nove_digitos + str(digito_1)
        contador_regressivo_2 = 11
        resultado_digito_2 = 0
        for digito in dez_digitos:
            resultado_digito_2 += int(digito) * contador_regressivo_2
            contador_regressivo_2 -= 1
        digito_2 = (resultado_digito_2 * 10) % 11
        digito_2 = digito_2 if digito_2 <= 9 else 0

        cpf_calculado = f'{nove_digitos}{digito_1}{digito_2}'
        vetor_cpfs.append(cpf_calculado)

    return vetor_cpfs

def buscar_cpf(cpf_procurado, vetor_cpfs):
    inicio = time.perf_counter()

    for i in range(len(vetor_cpfs)):
        if vetor_cpfs[i] == cpf_procurado:
            fim = time.perf_counter()
            tempo_gasto = fim - inicio
            return i, tempo_gasto

meus_cpfs = gerar_cpfs()
print(f"CPFs gerados: {meus_cpfs}")

total_cpfs = gerar_cpfs()
print(f"Total de CPFs gerados: {len(total_cpfs)}")

cpf_para_procurar = meus_cpfs[random.randint(0, len(meus_cpfs) - 1)]
indice_cpf_encontrado, tempo_execucao = buscar_cpf(cpf_para_procurar, meus_cpfs)
print(f"O CPF '{cpf_para_procurar}' foi encontrado na {indice_cpf_encontrado + 1}° posição")
print(f"Tempo gasto na busca: {tempo_execucao:.8f} segundos.")