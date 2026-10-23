import math
import random
import unittest

from even_partition import EvenPartitionSolver


class TestEvenPartitionSolver(unittest.TestCase):
    def test_solver_can_be_created(self):
        solver = EvenPartitionSolver(3, {})
        self.assertEqual(solver.length, 3)
        self.assertIsNone(solver.table)

    def test_missing_weights_are_infinite(self):
        solver = EvenPartitionSolver(2, {(0, 1): 1})
        table = solver.build_dp_table()

        self.assertTrue(math.isinf(table["A"][2][0]))
        self.assertTrue(math.isinf(table["A"][2][1]))
        self.assertTrue(math.isinf(table["R"][2]))

    def test_negative_length_is_rejected(self):
        with self.assertRaises(ValueError):
            EvenPartitionSolver(-1, {})

    def test_recovers_single_edge_path(self):
        solver = EvenPartitionSolver(
            2,
            {
                (0, 1): 5,
                (1, 2): 5,
                (0, 2): 2,
            },
        )

        result = solver.get_optimal_path()
        self.assertEqual(result.edges, ((0, 2),))
        self.assertEqual(result.cost, 2)

    def test_recovers_multi_edge_path_in_forward_order(self):
        weights = {
            (0, 1): 2,
            (1, 2): 3,
            (2, 3): 1,
            (0, 2): 10,
            (1, 3): 10,
            (0, 3): 100,
        }
        solver = EvenPartitionSolver(3, weights)

        result = solver.get_optimal_path()
        self.assertEqual(
            result.edges,
            ((0, 1), (1, 2), (2, 3)),
        )
        self.assertEqual(result.cost, 6)

    def test_path_is_none_when_end_is_unreachable(self):
        solver = EvenPartitionSolver(2, {(0, 1): 1})
        self.assertIsNone(solver.get_optimal_path())

    def test_path_method_builds_table_when_needed(self):
        solver = EvenPartitionSolver(1, {(0, 1): 4})
        result = solver.get_optimal_path()
        self.assertEqual(result.edges, ((0, 1),))
        self.assertIsNotNone(solver.table)

    def test_even_path_can_be_more_expensive_than_unrestricted_path(self):
        weights = {
            (0, 3): 1,
            (0, 1): 2,
            (1, 3): 2,
            (0, 2): 1.5,
            (2, 3): 1.5,
        }
        solver = EvenPartitionSolver(3, weights)

        ordinary = solver.get_optimal_path()
        result = solver.find_optimal_even_path()

        self.assertEqual(ordinary.edges, ((0, 3),))
        self.assertEqual(result.edges, ((0, 2), (2, 3)))
        self.assertEqual(result.edge_count, 2)
        self.assertEqual(result.cost, 3)

    def test_even_path_returns_unrestricted_path_when_already_even(self):
        solver = EvenPartitionSolver(
            2,
            {
                (0, 1): 1,
                (1, 2): 1,
                (0, 2): 5,
            },
        )
        result = solver.find_optimal_even_path()

        self.assertEqual(result.edges, ((0, 1), (1, 2)))
        self.assertEqual(result.cost, 2)

    def test_no_even_path_exists(self):
        solver = EvenPartitionSolver(1, {(0, 1): 1})
        self.assertIsNone(solver.find_optimal_even_path())

    def test_solve_builds_table_and_finds_even_path(self):
        solver = EvenPartitionSolver(
            2,
            {
                (0, 1): 1,
                (1, 2): 1,
                (0, 2): 4,
            },
        )
        result = solver.solve()

        self.assertEqual(result.edges, ((0, 1), (1, 2)))
        self.assertEqual(result.cost, 2)
        self.assertIsNotNone(solver.table)

    def test_invalid_edge_key_is_rejected(self):
        with self.assertRaises(ValueError):
            EvenPartitionSolver(2, {"0-1": 1})

    def test_edge_outside_interval_is_rejected(self):
        with self.assertRaises(ValueError):
            EvenPartitionSolver(2, {(0, 3): 1})

    def test_search_matches_exhaustive_enumeration(self):
        generator = random.Random(17)

        for length in range(2, 7):
            for _ in range(25):
                weights = {}
                for start in range(length):
                    for end in range(start + 1, length + 1):
                        if generator.random() < 0.7:
                            weights[(start, end)] = generator.randint(1, 20)

                expected = exhaustive_even_cost(length, weights)
                result = EvenPartitionSolver(
                    length,
                    weights,
                ).find_optimal_even_path()

                if expected is None:
                    self.assertIsNone(result)
                else:
                    self.assertIsNotNone(result)
                    self.assertEqual(result.edge_count % 2, 0)
                    self.assertEqual(result.cost, expected)


def exhaustive_even_cost(length, weights):
    best_cost = None

    def visit(current, cost, edge_count):
        nonlocal best_cost

        if current == length:
            if edge_count % 2 == 0:
                if best_cost is None or cost < best_cost:
                    best_cost = cost
            return

        for end in range(current + 1, length + 1):
            weight = weights.get((current, end))
            if weight is not None:
                visit(end, cost + weight, edge_count + 1)

    visit(0, 0, 0)
    return best_cost


if __name__ == "__main__":
    unittest.main()
