from src.fitness import Fitness
import random


class Busca:
    S = []
    iteracoes = 0
    tamanho = 0

    solucao_final, fitness_final = None, None

    # inicia a busca e salva os parametros necessarios para os calculos
    @classmethod
    def inicia_busca(cls, S, iteracoes, tamanho_tabu):
        cls.S = S
        cls.iteracoes = iteracoes
        cls.tamanho = tamanho_tabu

        Fitness.inicia_Fitness()

        cls.solucao_final, cls.fitness_final = cls.busca()

        return cls.solucao_final, cls.fitness_final

    # A funcao de busca gera e procura por vizinhos proximos um determinado numero de vezes,
    # comparando-os ate encontrar aquele que oferece a menor diferenca entre os grupos (melhor fitness)
    @classmethod
    def busca(cls):
        solucao_atual = cls.gerar_aleatorio()
        fitness_atual = Fitness.calcula_fitness(solucao_atual, cls.S)
        lista = []

        melhor_solucao = solucao_atual
        melhor_fitness = fitness_atual

        for _ in range(cls.iteracoes):
            vizinhos = cls.gerar_vizinhos(solucao_atual)
            melhor_vizinho, melhor_fitness_vizinho = cls.selecionar_melhor_vizinho(vizinhos, lista)

            if melhor_fitness_vizinho < melhor_fitness:
                melhor_solucao = melhor_vizinho
                melhor_fitness = melhor_fitness_vizinho

            solucao_atual = melhor_vizinho
            fitness_atual = melhor_fitness_vizinho

            cls.atualizar_lista(lista, solucao_atual)
            if melhor_fitness == 0: break

        return melhor_solucao, melhor_fitness

    # Gera uma configuracao inicial aleatoria para os dois grupos
    @classmethod
    def gerar_aleatorio(cls):
        solucao = []
        for _ in cls.S:
            solucao.append(random.randint(0, 1))

        return solucao

    # Gera diversos vizinhos a partir da inversao de cada elemento da solucao atual
    # essa metodologia pode ser alterada conforme a preferencia dos testes
    @classmethod
    def gerar_vizinhos(cls, solucao):
        vizinhos = []
        for i in range(len(solucao)):
            vizinho = solucao.copy()
            vizinho[i] = 1 - vizinho[i]
            vizinhos.append(vizinho)

        return vizinhos

    # Essa funcao escolhe o melhor vizinho gerado a partir do fitness calculado entre eles
    # filtrando aqueles vizinhos que estiverem presentes na lista tabu no momento do calculo
    @classmethod
    def selecionar_melhor_vizinho(cls, vizinhos, lista):
        melhor_vizinho = None
        melhor_fitness = float('inf')

        for vizinho in vizinhos:
            if vizinho in lista: continue

            fitness_atual = Fitness.calcula_fitness(vizinho, cls.S)

            if fitness_atual < melhor_fitness:
                melhor_vizinho = vizinho
                melhor_fitness = fitness_atual
                if melhor_fitness == 0: break

        return melhor_vizinho, melhor_fitness

    # Atualiza a lista tabu conforme cada solucao for escolhida
    @classmethod
    def atualizar_lista(cls, lista, solucao):
        lista.append(solucao)
        if len(lista) > cls.tamanho:
            lista.pop(0)
