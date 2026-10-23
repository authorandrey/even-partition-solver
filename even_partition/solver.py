from math import inf, isinf

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
            self.logger.debug(
                "For the point %s minimal cost is: %s",
                end,
                costs[end],
            )

        self.table = {"R": costs, "A": table}
        return self.table

    def get_optimal_path(self):
        if self.table is None:
            self.build_dp_table()

        if isinf(self.table["R"][self.length]):
            self.logger.warning("Route to the end does not exist")
            return None

        path = []
        end = self.length

        while end > 0:
            row = self.table["A"][end]
            current_cost = self.table["R"][end]
            selected_start = None

            for count, candidate_cost in enumerate(row, start=1):
                if candidate_cost == current_cost:
                    selected_start = end - count
                    break

            if selected_start is None:
                self.logger.warning(
                    "Could not restore the route to the point %s",
                    end,
                )
                return None

            path.append((selected_start, end))
            self.logger.debug(
                "Restored (%s, %s)",
                selected_start,
                end,
            )
            end = selected_start

        path.reverse()
        return path

    def find_optimal_even_path(self):
        raise NotImplementedError("")

    def solve(self):
        raise NotImplementedError("")
