from math import inf, isfinite, isinf

from even_partition.logger import PartitionLogger
from even_partition.models import PartitionResult


class EvenPartitionSolver:
    def __init__(self, length, weights, logger=None):
        if length < 0:
            raise ValueError("Invalid length")

        self._validate_weights(length, weights)
        self.length = length
        self.weights = dict(weights)
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
        self.logger.info("DP table constructed")
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
        return PartitionResult(tuple(path), self.table["R"][self.length])

    def find_optimal_even_path(self):
        if self.table is None:
            self.build_dp_table()

        ordinary_path = self.get_optimal_path()
        if ordinary_path is None:
            self.logger.warning("No path to the end of the line")
            return None

        if ordinary_path.edge_count % 2 == 0:
            self.logger.info(
                "Optimal path already is even"
            )
            return ordinary_path

        best_cost = inf
        best_edges = None
        reversed_path = []
        costs = self.table["R"]
        rows = self.table["A"]

        def search(current, cost_so_far, edge_count):
            nonlocal best_cost, best_edges

            if current == 0:
                if edge_count % 2 == 0 and cost_so_far < best_cost:
                    best_cost = cost_so_far
                    best_edges = tuple(reversed(reversed_path))
                    self.logger.debug(
                        "Found even path with cost %s",
                        best_cost,
                    )
                return

            if not isfinite(costs[current]):
                return

            lower_bound = cost_so_far + costs[current]
            if best_edges is not None and lower_bound >= best_cost:
                self.logger.debug(
                    "Brunch cut at the point %s: lower bound %s, best %s",
                    current,
                    lower_bound,
                    best_cost,
                )
                return

            distances = sorted(
                range(1, current + 1),
                key=lambda distance: rows[current][distance - 1],
            )

            for distance in distances:
                candidate = rows[current][distance - 1]

                if best_edges is not None:
                    if cost_so_far + candidate >= best_cost:
                        break

                previous = current - distance
                edge_cost = self.weights.get((previous, current), inf)

                if not isfinite(costs[previous]) or not isfinite(edge_cost):
                    continue

                reversed_path.append((previous, current))
                self.logger.debug(
                    "Transition (%s, %s), cost so far %s",
                    previous,
                    current,
                    cost_so_far + edge_cost,
                )
                search(
                    previous,
                    cost_so_far + edge_cost,
                    edge_count + 1,
                )
                reversed_path.pop()

        self.logger.info("Start finding even path")
        search(self.length, 0, 0)

        if best_edges is None:
            self.logger.warning("Even path does not exist")
            return None

        result = PartitionResult(best_edges, best_cost)
        self.logger.info(
            "Found optimal even path: cost %s, parts %s",
            result.cost,
            result.edge_count,
        )
        return result

    def solve(self):
        self.build_dp_table()
        return self.find_optimal_even_path()

    @staticmethod
    def _validate_weights(length, weights):
        for edge, weight in weights.items():
            if not isinstance(edge, tuple) or len(edge) != 2:
                raise ValueError("Key must ba a pair (start, end)")

            start, end = edge

            if not 0 <= start < end <= length:
                raise ValueError(
                    "0 <= start < end <= length"
                )
