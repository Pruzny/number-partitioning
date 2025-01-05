from concurrent.futures import ThreadPoolExecutor
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
        cls.tamanho = int(len(S) * 0.1)

        cls.limite_sem_melhoria = max(int(iteracoes * 0.1), 100)

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

        sem_melhoria = 0

        for _ in range(cls.iteracoes):
            vizinhos = cls.gerar_vizinhos(solucao_atual)
            melhor_vizinho, melhor_fitness_vizinho = cls.selecionar_melhor_vizinho(vizinhos, lista, melhor_fitness)

            if melhor_fitness_vizinho < melhor_fitness:
                melhor_solucao = melhor_vizinho
                melhor_fitness = melhor_fitness_vizinho
                sem_melhoria = 0
            else:
                sem_melhoria += 1

            if sem_melhoria > cls.limite_sem_melhoria:
                solucao_atual = cls.gerar_aleatorio()
                sem_melhoria = 0
            elif melhor_vizinho:
                solucao_atual = melhor_vizinho
                fitness_atual = melhor_fitness_vizinho

            cls.atualizar_lista(lista, solucao_atual)
            if melhor_fitness == 0: break
            if melhor_fitness == 1 & random.randint(0, 1) == 1: break 

        return melhor_solucao, melhor_fitness

    # Gera uma configuracao inicial aleatoria para os dois grupos
    @classmethod
    def gerar_aleatorio(cls):
        return [random.randint(0, 1) for _ in cls.S]

    # Gera diversos vizinhos a partir da inversao de cada elemento da solucao atual
    # com uma heurística para priorizar elementos que causam maior desequilíbrio
    @classmethod
    def gerar_vizinhos(cls, solucao):
        soma_grupo_0 = sum(cls.S[i] for i in range(len(solucao)) if solucao[i] == 0)
        soma_grupo_1 = sum(cls.S[i] for i in range(len(solucao)) if solucao[i] == 1)

        desequilibrio = abs(soma_grupo_0 - soma_grupo_1)
        vizinhos = []

        for i in range(len(solucao)):
            vizinho = solucao.copy()
            vizinho[i] = 1 - vizinho[i]
            nova_soma_0 = soma_grupo_0 + (cls.S[i] if solucao[i] == 1 else -cls.S[i])
            nova_soma_1 = soma_grupo_1 + (cls.S[i] if solucao[i] == 0 else -cls.S[i])
            novo_desequilibrio = abs(nova_soma_0 - nova_soma_1)

            if novo_desequilibrio < desequilibrio:
                vizinhos.append(vizinho)

        return vizinhos

    # Essa funcao escolhe o melhor vizinho gerado a partir do fitness calculado entre eles
    # filtrando aqueles vizinhos que estiverem presentes na lista tabu no momento do calculo
    # e excluindo os vizinhos cujo fitness é pior do que o atual melhor fitness
    @classmethod
    def selecionar_melhor_vizinho(cls, vizinhos, lista, melhor_fitness):
        melhor_vizinho = None
        melhor_fitness_vizinho = float('inf')

        def calcular_fitness_vizinho(vizinho):
            return vizinho, Fitness.calcula_fitness(vizinho, cls.S)

        with ThreadPoolExecutor() as executor:
            resultados = executor.map(calcular_fitness_vizinho, vizinhos)

        for vizinho, fitness_atual in resultados:
            if vizinho in lista and fitness_atual >= melhor_fitness:
                continue

            if fitness_atual < melhor_fitness_vizinho:
                melhor_vizinho = vizinho
                melhor_fitness_vizinho = fitness_atual
                if melhor_fitness_vizinho == 0:
                    break

        return melhor_vizinho, melhor_fitness_vizinho

    # Atualiza a lista tabu conforme cada solucao for escolhida
    @classmethod
    def atualizar_lista(cls, lista, solucao):
        lista.append(solucao)
        if len(lista) > cls.tamanho:
            lista.pop(0)
