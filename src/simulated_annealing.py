import random
import math


MAX_ITER = 1000
INITIAL_TEMP = 1000
COOLING_RATE = 0.95
NUMBERS = [i for i in range(1, 11)]


def simulated_annealing(
        path: str,
        numbers: list[int | float],
        max_iter: int,
        initial_temp: int,
        cooling_rate: float
) -> tuple[list[int], int]:
    """
    Solução do problema da partição utilizando Simulated Annealing.

    :param path: Caminho para o arquivo de saída dos números.
    :param numbers: Lista de números a serem particionados.
    :param max_iter: Número máximo de iterações.
    :param initial_temp: Temperatura inicial.
    :param cooling_rate: Fator de resfriamento por iteração.
    :return: Melhor solução encontrada e a diferença absoluta entre as somas dos subconjuntos.
    """
    # Função para calcular a diferença absoluta entre as somas dos subconjuntos
    def calculate_difference(partition):
        subset1 = sum(numbers[i] for i in range(len(numbers)) if partition[i] == 0)
        subset2 = sum(numbers[i] for i in range(len(numbers)) if partition[i] == 1)
        return abs(subset1 - subset2)

    # Solução inicial aleatória
    current_solution = [random.randint(0, 1) for _ in numbers]
    current_difference = calculate_difference(current_solution)

    best_solution = current_solution[:]
    best_difference = current_difference

    temperature = initial_temp

    for iteration in range(max_iter):
        neighbor_solution = current_solution[:]
        index_to_flip = random.randint(0, len(numbers) - 1)

        # Flipar o bit
        neighbor_solution[index_to_flip] = 1 - neighbor_solution[index_to_flip]

        neighbor_difference = calculate_difference(neighbor_solution)

        # Verificar se aceita a nova solução
        delta = neighbor_difference - current_difference
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperature):
            current_solution = neighbor_solution[:]
            current_difference = neighbor_difference

            # Atualizar a melhor solução encontrada
            if current_difference < best_difference:
                best_solution = current_solution[:]
                best_difference = current_difference

        # Reduzir a temperatura após o fim da iteração
        temperature *= cooling_rate

    with open(path, "w") as file:
        for i in range(len(numbers)):
            file.write(f"{numbers[i]} | {best_solution[i]}\n")

    return best_solution, best_difference


if __name__ == "__main__":
    solution, difference = simulated_annealing(
        "../outputs/simulated_annealing.txt",
        NUMBERS,
        initial_temp=INITIAL_TEMP,
        max_iter=MAX_ITER,
        cooling_rate=COOLING_RATE
    )

    first_set = [NUMBERS[i] for i in range(len(NUMBERS)) if solution[i] == 0]
    second_set = [NUMBERS[i] for i in range(len(NUMBERS)) if solution[i] == 1]

    print("Subconjunto 1:", first_set)
    print("Subconjunto 2:", second_set)
    print("Diferença mínima:", difference)
