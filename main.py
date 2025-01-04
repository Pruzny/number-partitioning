import time
import numpy

from src.simulated_annealing import simulated_annealing
from src.lista_tabu import tabu_search, result_to_file


NUMBERS_PATH = "inputs/numbers.txt"

SIMULATED_ANNEALING_PATH = "outputs/simulated_annealing.txt"
TABU_SEARCH_PATH = "outputs/tabu_search.txt"

# Geral
REPEAT = 1000
INTERN_ITER = 1000

# Simulated Annealing
INITIAL_TEMP = 1000
COOLING_RATE = 0.95

# Busca Tabu
TABU_SIZE = 20

with open(NUMBERS_PATH) as file:
    numbers = [int(line) for line in file]

# Solução com o algoritmo Simulated Annealing
solutions_sa = []
differences_sa = []
start_sa = time.time()
for _ in range(REPEAT):
    solution_sa, difference_sa = simulated_annealing(
        numbers,
        max_iter=INTERN_ITER,
        initial_temp=INITIAL_TEMP,
        cooling_rate=COOLING_RATE
    )
    solutions_sa.append(solution_sa)
    differences_sa.append(difference_sa)
end_sa = time.time()
best_sa = numpy.argmin(differences_sa)
result_to_file(SIMULATED_ANNEALING_PATH, numbers, solutions_sa[best_sa])

# Solução com o algoritmo Busca Tabu
solutions_lt = []
fitnesses_lt = []
start_lt = time.time()
for _ in range(REPEAT):
    solucao_lt, fitness_lt = tabu_search(
        numeros=numbers,
        iteracoes=INTERN_ITER,
        tamanho=TABU_SIZE
    )
    solutions_lt.append(solucao_lt)
    fitnesses_lt.append(fitness_lt)
end_lt = time.time()
best_lt = numpy.argmin(fitnesses_lt)
result_to_file(TABU_SEARCH_PATH, numbers, solutions_lt[best_lt])


# Resultados
print(f"Numbers: {numbers}")
print(f"Total numbers: {len(numbers)}")
print(f"Total cycles: {REPEAT}")
print()

print(f"Simulated Annealing:")
print(f"Solution: {solutions_sa[best_sa]}")
print(f"Difference: {differences_sa[best_sa]}")
print(f"Average difference: {numpy.mean(differences_sa)}")
print(f"Time: {end_sa - start_sa:.4f} seconds")
print()

print(f"Lista Tabu:")
print(f"Solution: {solutions_lt[best_lt]}")
print(f"Fitness: {fitnesses_lt[best_lt]}")
print(f"Average Fitness: {numpy.mean(fitnesses_lt)}")
print(f"Time: {end_lt - start_lt:.4f} seconds")
