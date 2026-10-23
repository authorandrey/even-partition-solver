from even_partition import EvenPartitionSolver


weights = {
    (0, 1): 1,
    (1, 2): 1,
    (2, 3): 1,
    (0, 2): 3,
    (1, 3): 2,
    (0, 3): 10,
}

solver = EvenPartitionSolver(3, weights)
table = solver.build_dp_table()
ordinary = solver.get_optimal_path()
result = solver.find_optimal_even_path()

print("R:", table["R"])
print("A:", table["A"])
print("Обычный оптимальный путь:", ordinary)
print("Оптимальный чётный путь:", result)

if result is not None:
    print("Звеньев:", result.edge_count)
    print("Стоимость:", result.cost)
