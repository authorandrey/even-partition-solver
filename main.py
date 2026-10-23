import logging

from even_partition import EvenPartitionSolver, PartitionLogger


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    weights = {
        (0, 1): 1,
        (1, 2): 1,
        (2, 3): 1,
        (0, 2): 3,
        (1, 3): 2,
        (0, 3): 10,
    }

    solver = EvenPartitionSolver(
        length=3,
        weights=weights,
        logger=PartitionLogger(),
    )
    table = solver.build_dp_table()

    print("R:", list(table.costs))
    print("A:", [list(row) for row in table.candidates])

    result = solver.find_optimal_even_path()
    if result is None:
        print("Путь с чётным числом звеньев не существует")
        return

    print("Путь:", result.edges)
    print("Число звеньев:", result.edge_count)
    print("Стоимость:", result.cost)


if __name__ == "__main__":
    main()
