import logging
import random
from collections.abc import Mapping

from even_partition import (
    EvenPartitionDPSolver,
    EvenPartitionSolver,
    PartitionLogger,
    PartitionResult,
)


RANDOM_SEED = 20261023
EXAMPLE_COUNT = 50000
MAX_LENGTH = 10
EDGE_PROBABILITY = 0.7
MIN_WEIGHT = -10
MAX_WEIGHT = 20


def generate_weights(
    length: int,
    generator: random.Random,
) -> dict[tuple[int, int], int]:
    weights = {}

    for start in range(length):
        for end in range(start + 1, length + 1):
            if generator.random() < EDGE_PROBABILITY:
                weights[(start, end)] = generator.randint(
                    MIN_WEIGHT,
                    MAX_WEIGHT,
                )

    return weights


def validate_result(
    result: PartitionResult,
    length: int,
    weights: Mapping[tuple[int, int], int],
    case_number: int,
    solver_name: str,
) -> None:
    if not result.is_even:
        raise AssertionError(
            f"Пример #{case_number}: {solver_name} вернул "
            "путь нечётной длины"
        )

    current = 0
    total_cost = 0

    for edge in result.edges:
        if edge not in weights:
            raise AssertionError(
                f"Пример #{case_number}: {solver_name} использовал "
                f"отсутствующее звено {edge}"
            )

        start, end = edge
        if start != current:
            raise AssertionError(
                f"Пример #{case_number}: разрыв пути у звена "
                f"{edge} в результате {solver_name}"
            )

        current = end
        total_cost += weights[edge]

    if current != length:
        raise AssertionError(
            f"Пример #{case_number}: {solver_name} завершил путь "
            f"в точке {current}, ожидалась {length}"
        )

    if total_cost != result.cost:
        raise AssertionError(
            f"Пример #{case_number}: стоимость {total_cost} не "
            f"совпадает с {result.cost} ({solver_name})"
        )


def check_equivalence(
    case_number: int,
    length: int,
    weights: Mapping[tuple[int, int], int],
    logger: PartitionLogger,
) -> bool:
    tree_result = EvenPartitionSolver(length, weights, logger).solve()
    dp_result = EvenPartitionDPSolver(length, weights, logger).solve()

    if (tree_result is None) != (dp_result is None):
        raise AssertionError(
            f"Различается наличие решения в примере #{case_number}: "
            f"n={length}, weights={weights}, "
            f"tree={tree_result}, dp={dp_result}"
        )

    if tree_result is None:
        return False

    if tree_result.cost != dp_result.cost:
        raise AssertionError(
            f"Различается стоимость в примере #{case_number}: "
            f"n={length}, weights={weights}, "
            f"tree={tree_result}, dp={dp_result}"
        )

    validate_result(
        tree_result,
        length,
        weights,
        case_number,
        "поиск по дереву",
    )
    validate_result(
        dp_result,
        length,
        weights,
        case_number,
        "динамическое программирование",
    )
    return True


def main() -> None:
    generator = random.Random(RANDOM_SEED)
    logger = PartitionLogger(level=logging.CRITICAL)
    solved_count = 0

    for case_number in range(1, EXAMPLE_COUNT + 1):
        length = generator.randint(0, MAX_LENGTH)
        weights = generate_weights(length, generator)

        if check_equivalence(case_number, length, weights, logger):
            solved_count += 1

    print(
        "Эквивалентность подтверждена на "
        f"{EXAMPLE_COUNT} случайных примерах."
    )
    print(f"Seed: {RANDOM_SEED}")
    print(f"Допустимое решение найдено: {solved_count}")
    print(
        "Решение отсутствует у обоих алгоритмов: "
        f"{EXAMPLE_COUNT - solved_count}"
    )


if __name__ == "__main__":
    main()
