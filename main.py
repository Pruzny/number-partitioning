import time
import numpy

from src.simulated_annealing import simulated_annealing


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
        SIMULATED_ANNEALING_PATH,
        numbers,
        max_iter=INTERN_ITER,
        initial_temp=INITIAL_TEMP,
        cooling_rate=COOLING_RATE
    )
    solutions_sa.append(solution_sa)
    differences_sa.append(difference_sa)
end_sa = time.time()
best_sa = numpy.argmin(differences_sa)


# Solução com o algoritmo Busca Tabu
# TODO: add tabu search

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
