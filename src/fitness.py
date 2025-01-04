class Fitness:

	soma1 = 0
	soma2 = 0
	solucao_antiga = []

	@classmethod
	def inicia_Fitness(cls):
		cls.soma1 = 0
		cls.soma2 = 0
		cls.solucao_antiga = []

	# A funcao fitness e responsavel por calcular a qualidade de uma solucao gerada,
	# a partir dela o algoritmo seleciona qual vizinho gerado e o melhor,
	# comparando a soma dos dois subgrupos gerados com o objetivo de minimizar a diferenca
	@classmethod
	def calcula_fitness(cls, solucao, S):
		if not cls.solucao_antiga:
			cls.solucao_antiga = solucao.copy()
			cls.soma1 = sum([S[i] for i in range(len(S)) if solucao[i] == 0])
			cls.soma2 = sum([S[i] for i in range(len(S)) if solucao[i] == 1])

			return abs(cls.soma1 - cls.soma2)

		for i in range(len(solucao)):
			if solucao[i] != cls.solucao_antiga[i]:
				if solucao[i] == 0:
					cls.soma1 += S[i]
					cls.soma2 -= S[i]
				else:
					cls.soma1 -= S[i]
					cls.soma2 += S[i]

		cls.solucao_antiga = solucao.copy()
		return abs(cls.soma1 - cls.soma2)