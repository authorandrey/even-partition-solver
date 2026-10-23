import math
import unittest

from even_partition import EvenPartitionSolver


class TestEvenPartitionSolver(unittest.TestCase):
    def test_solver_can_be_created(self):
        solver = EvenPartitionSolver(3, {})
        self.assertEqual(solver.length, 3)
        self.assertIsNone(solver.table)

    def test_builds_dp_table(self):
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

        self.assertEqual(table["R"], [0, 1, 2, 3])
        self.assertEqual(table["A"][1], [1])
        self.assertEqual(table["A"][2], [2, 3])
        self.assertEqual(table["A"][3], [3, 3, 10])
        self.assertIs(solver.table, table)

    def test_missing_weights_are_infinite(self):
        solver = EvenPartitionSolver(2, {(0, 1): 1})

        table = solver.build_dp_table()

        self.assertTrue(math.isinf(table["A"][2][0]))
        self.assertTrue(math.isinf(table["A"][2][1]))
        self.assertTrue(math.isinf(table["R"][2]))

    def test_zero_length(self):
        solver = EvenPartitionSolver(0, {})

        table = solver.build_dp_table()

        self.assertEqual(table["R"], [0])
        self.assertEqual(table["A"], [[]])

    def test_negative_length_is_rejected(self):
        with self.assertRaises(ValueError):
            EvenPartitionSolver(-1, {})

    def test_path_methods_are_not_implemented_yet(self):
        solver = EvenPartitionSolver(2, {})

        with self.assertRaises(NotImplementedError):
            solver.get_optimal_path()

        with self.assertRaises(NotImplementedError):
            solver.find_optimal_even_path()

        with self.assertRaises(NotImplementedError):
            solver.solve()
