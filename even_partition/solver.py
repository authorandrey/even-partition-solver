from collections.abc import Mapping
from math import inf
from numbers import Real

from even_partition.logger import PartitionLogger
from even_partition.models import DPTable, Edge, PartitionResult


class EvenPartitionSolver:
    def __init__(
        self,
        length: int,
        weights: Mapping[Edge, Real],
        logger: PartitionLogger | None = None,
    ) -> None:
        self._validate_length(length)
        self._validate_weights(length, weights)

        self.length = length
        self._weights = dict(weights)
        self.logger = logger if logger is not None else PartitionLogger()
        self.table: DPTable | None = None

    @property
    def weights(self) -> Mapping[Edge, Real]:
        return self._weights.copy()

    def build_dp_table(self) -> DPTable:
        self.logger.info("Constructing DP table for size %s", self.length)

        costs: list[Real] = [inf] * (self.length + 1)
        candidates: list[tuple[Real, ...]] = [()] * (self.length + 1)
        costs[0] = 0

        for end in range(1, self.length + 1):
            row = []
            for distance in range(1, end + 1):
                start = end - distance
                weight = self._weights.get((start, end), inf)
                row.append(costs[start] + weight)

            candidates[end] = tuple(row)
            costs[end] = min(row, default=inf)
            self.logger.debug(
                "R(%s) = %s",
                end,
                costs[end],
            )

        self.table = DPTable(tuple(costs), tuple(candidates))
        self.logger.info("DP table constructed")
        return self.table

    def get_optimal_path(self) -> PartitionResult | None:
        table = self._get_table()
        total_cost = table.costs[self.length]

        if _is_infinite(total_cost):
            self.logger.warning(
                "Path to the point %s does not exist",
                self.length,
            )
            return None

        reversed_edges: list[Edge] = []
        end = self.length

        while end > 0:
            row = table.candidates[end]
            best_cost = table.costs[end]
            selected_start = None

            for distance, candidate_cost in enumerate(row, start=1):
                if candidate_cost == best_cost:
                    selected_start = end - distance
                    break

            if selected_start is None:
                self.logger.error(
                    "Could not restore the path to the point %s",
                    end,
                )
                return None

            reversed_edges.append((selected_start, end))
            end = selected_start

        reversed_edges.reverse()
        result = PartitionResult(tuple(reversed_edges), total_cost)
        self.logger.info(
            "Usual optimal path: cost=%s, parts=%s",
            result.cost,
            result.edge_count,
        )
        return result

    def find_optimal_even_path(self) -> PartitionResult | None:
        table = self._get_table()
        ordinary_path = self.get_optimal_path()

        if ordinary_path is None:
            return None

        if ordinary_path.is_even:
            self.logger.info("Optimal path already is even")
            return ordinary_path

        best_cost: Real = inf
        best_edges: tuple[Edge, ...] | None = None
        reversed_edges: list[Edge] = []
        costs = table.costs
        candidates = table.candidates

        def search(current: int, accrued_cost: Real, edge_count: int) -> None:
            nonlocal best_cost, best_edges

            if current == 0:
                if edge_count % 2 == 0 and accrued_cost < best_cost:
                    best_cost = accrued_cost
                    best_edges = tuple(reversed(reversed_edges))
                    self.logger.debug(
                        "Found even path with cost %s",
                        best_cost,
                    )
                return

            remaining_cost = costs[current]
            if _is_infinite(remaining_cost):
                return

            lower_bound = accrued_cost + remaining_cost
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
                key=lambda distance: candidates[current][distance - 1],
            )

            for distance in distances:
                start = current - distance
                edge_candidate = candidates[current][distance - 1]

                if best_edges is not None:
                    if accrued_cost + edge_candidate >= best_cost:
                        break

                edge_weight = self._weights.get((start, current))
                if edge_weight is None or _is_infinite(costs[start]):
                    continue

                reversed_edges.append((start, current))
                search(start, accrued_cost + edge_weight, edge_count + 1)
                reversed_edges.pop()

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

    def solve(self) -> PartitionResult | None:
        self.build_dp_table()
        return self.find_optimal_even_path()

    def _get_table(self) -> DPTable:
        if self.table is None:
            return self.build_dp_table()
        return self.table

    @staticmethod
    def _validate_length(length: int) -> None:
        if isinstance(length, bool) or not isinstance(length, int):
            raise TypeError("Длина отрезка должна быть целым числом")
        if length < 0:
            raise ValueError("Длина отрезка должна быть неотрицательной")

    @classmethod
    def _validate_weights(
        cls,
        length: int,
        weights: Mapping[Edge, Real],
    ) -> None:
        for edge, weight in weights.items():
            cls._validate_edge(length, edge)
            cls._validate_weight(weight)

    @staticmethod
    def _validate_edge(length: int, edge: Edge) -> None:
        if not isinstance(edge, tuple) or len(edge) != 2:
            raise ValueError("Key must ba a pair (start, end)")

        start, end = edge

        if not 0 <= start < end <= length:
            raise ValueError("0 <= start < end <= length")

    @staticmethod
    def _validate_weight(weight: Real) -> None:
        if weight != weight or weight == inf or weight == -inf:
            raise ValueError("Infinite weight is unavailable")


def _is_infinite(value: Real) -> bool:
    return value == inf or value == -inf
