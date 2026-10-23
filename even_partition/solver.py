from math import inf

from even_partition.logger import PartitionLogger


class EvenPartitionSolver:
    def __init__(self, length, weights, logger=None):
        if length < 0:
            raise ValueError("Invalid length")

        self.length = length
        self.weights = weights
        self.logger = logger or PartitionLogger()
        self.table = None

    def build_dp_table(self):
        self.logger.info("Constructing DP table for size %s", self.length)

        costs = [inf] * (self.length + 1)
        table = [[] for _ in range(self.length + 1)]
        costs[0] = 0

        for end in range(1, self.length + 1):
            row = []

            for count in range(1, end + 1):
                start = end - count
                weight = self.weights.get((start, end), inf)
                row.append(costs[start] + weight)

            table[end] = row
            costs[end] = min(row)

        self.table = {"R": costs, "A": table}
        return self.table

    def get_optimal_path(self):
        raise NotImplementedError("")

    def find_optimal_even_path(self):
        raise NotImplementedError("")

    def solve(self):
        raise NotImplementedError("")
