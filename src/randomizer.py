import random


PATH = '../inputs/numbers.txt'
AMOUNT = 100
MINIMUM = 1
MAXIMUM = 1000


def randomize(
        path: str,
        amount: int,
        minimum: int,
        maximum: int
) -> None:
    """
    Creates a random set of numbers and saves in a file.

    :param path: Path to save the file.
    :param amount: Number of elements.
    :param minimum: Minimum possible value.
    :param maximum: Maximum possible value.
    """
    assert amount > 0, "Amount must be greater than 0"
    assert minimum < maximum, "Minimum must be less than maximum"
    assert maximum - minimum + 1 >= amount, "Range must be greater than or equal to amount"

    with open(path, 'w') as file:
        numbers = random.sample(range(minimum, maximum + 1), amount)
        for number in numbers:
            file.write(f'{number}\n')


if __name__ == "__main__":
    randomize(PATH, AMOUNT, MINIMUM, MAXIMUM)
