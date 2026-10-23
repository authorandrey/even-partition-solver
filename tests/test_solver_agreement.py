import itertools
import logging
import random
import unittest

from even_partition import EvenPartitionDPSolver, EvenPartitionSolver


class TestSolverAgreement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._logger = logging.getLogger("even_partition")
        cls._original_level = cls._logger.level
        cls._logger.setLevel(logging.CRITICAL)

    @classmethod
    def tearDownClass(cls):
        cls._logger.setLevel(cls._original_level)

    def assert_solvers_agree(self, length, weights):
        tree_result = EvenPartitionSolver(length, weights).solve()
        dp_result = EvenPartitionDPSolver(length, weights).solve()

        self.assertEqual(tree_result is None, dp_result is None)
        if tree_result is None:
            return

        self.assertEqual(tree_result.cost, dp_result.cost)
        self.assertTrue(dp_result.is_even)
        self.assertEqual(
            sum(weights[edge] for edge in dp_result.edges),
            dp_result.cost,
        )
        self.assertEqual(dp_result.edges[0][0] if dp_result.edges else 0, 0)
        self.assertEqual(
            dp_result.edges[-1][1] if dp_result.edges else 0,
            length,
        )
        for left, right in zip(dp_result.edges, dp_result.edges[1:]):
            self.assertEqual(left[1], right[0])

    def test_solvers_agree_on_sample(self):
        self.assert_solvers_agree(3, sample_weights())

    def test_solvers_agree_for_zero_length(self):
        self.assert_solvers_agree(0, {})

    def test_solvers_agree_when_end_is_unreachable(self):
        self.assert_solvers_agree(3, {(0, 1): 2, (1, 2): 3})

    def test_solvers_agree_with_negative_weights(self):
        weights = {
            (0, 1): -4,
            (1, 2): 2,
            (2, 3): -3,
            (0, 2): 0,
            (1, 3): 5,
            (0, 3): -10,
        }
        self.assert_solvers_agree(3, weights)

    def test_solvers_agree_on_exhaustive_small_inputs(self):
        length = 3
        edges = list(itertools.combinations(range(length + 1), 2))
        possible_weights = (None, -2, 3)

        for values in itertools.product(
            possible_weights, repeat=len(edges)
        ):
            weights = {
                edge: value
                for edge, value in zip(edges, values)
                if value is not None
            }
            with self.subTest(weights=weights):
                self.assert_solvers_agree(length, weights)

    def test_solvers_agree_on_random_inputs(self):
        generator = random.Random(20261023)

        for length in range(1, 8):
            for _ in range(40):
                weights = {}
                for start in range(length):
                    for end in range(start + 1, length + 1):
                        if generator.random() < 0.7:
                            weights[(start, end)] = generator.randint(-10, 20)
                with self.subTest(length=length, weights=weights):
                    self.assert_solvers_agree(length, weights)


def sample_weights():
    return {
        (0, 1): 1,
        (1, 2): 1,
        (2, 3): 1,
        (0, 2): 3,
        (1, 3): 2,
        (0, 3): 10,
    }


if __name__ == "__main__":
    unittest.main()
