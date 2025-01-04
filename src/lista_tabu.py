from src.busca import Busca
import time


MAX_ITER = 100
NUMBERS = [i for i in range(1, 11)]


def tabu_search(
        numeros: list[int | float],
        iteracoes: int = 1000,
        tamanho: int = 100
):
    melhor_solucao, melhor_fitness = Busca.inicia_busca(numeros, iteracoes, tamanho)

    return melhor_solucao, melhor_fitness


def somas_encontradas(S, F):
    x, y = [], []

    for i in range(len(S)):
        if F[i] == 0:
            x.append(S[i])
        else:
            y.append(S[i])

    return (x, y)


def contar_ocorrencias(lista):
    contador = {}
    for numero in lista:
        if numero in contador:
            contador[numero] += 1
        else:
            contador[numero] = 1
    return contador

def result_to_file(path, input, result):
    with open(path, "w") as file:
        for i in range(len(input)):
            file.write(f"{input[i]} | {result[i]}\n")


def exibir_tabela(contador):
    print(f"{'Inteiro':<10}{'Frequência':<10}")
    print("-" * 20)
    for numero, frequencia in sorted(contador.items(), key=lambda item: item[1], reverse=True):
        print(f"{numero:<10}{frequencia:<10}")


def tabela_fitness(lista_fitness):
    contador = contar_ocorrencias(lista_fitness)
    exibir_tabela(contador)


if __name__ == '__main__':
    tabu_search("../outputs/lista_tabu.txt", numeros=NUMBERS, iteracoes=MAX_ITER, tamanho=10)
