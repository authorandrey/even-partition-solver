from collections.abc import Mapping
from math import inf
from numbers import Real

from even_partition.logger import PartitionLogger
from even_partition.models import Edge, ParityDPTable, PartitionResult
from even_partition.validation import validate_length, validate_weights


class EvenPartitionDPSolver:
    def __init__(
        self,
        length: int,
        weights: Mapping[Edge, Real],
        logger: PartitionLogger | None = None,
    ) -> None:
        validate_length(length)
        validate_weights(length, weights)

        self.length = length
        self._weights = dict(weights)
        self.logger = logger if logger is not None else PartitionLogger()
        self.table: ParityDPTable | None = None

    @property
    def weights(self) -> Mapping[Edge, Real]:
        return self._weights.copy()

    def build_dp_table(self) -> ParityDPTable:
        self.logger.info(
            "Построение таблиц паритетов для n=%s",
            self.length,
        )

        even_costs: list[Real] = [inf] * (self.length + 1)
        odd_costs: list[Real] = [inf] * (self.length + 1)
        even_predecessors: list[int | None] = [None] * (
            self.length + 1
        )
        odd_predecessors: list[int | None] = [None] * (
            self.length + 1
        )
        even_costs[0] = 0

        for end in range(1, self.length + 1):
            for start in range(end):
                weight = self._weights.get((start, end), inf)
                if weight == inf:
                    continue

                if odd_costs[start] != inf:
                    candidate = odd_costs[start] + weight
                    if candidate < even_costs[end]:
                        even_costs[end] = candidate
                        even_predecessors[end] = start

                if even_costs[start] != inf:
                    candidate = even_costs[start] + weight
                    if candidate < odd_costs[end]:
                        odd_costs[end] = candidate
                        odd_predecessors[end] = start

            self.logger.debug(
                "E(%s) = %s, O(%s) = %s",
                end,
                even_costs[end],
                end,
                odd_costs[end],
            )

        self.table = ParityDPTable(
            tuple(even_costs),
            tuple(odd_costs),
            tuple(even_predecessors),
            tuple(odd_predecessors),
        )
        self.logger.info("Таблицы E и O построены")
        return self.table

    def get_optimal_even_path(self) -> PartitionResult | None:
        table = self._get_table()
        total_cost = table.even_costs[self.length]

        if total_cost == inf:
            self.logger.warning(
                "Чётный путь до точки %s не существует",
                self.length,
            )
            return None

        reversed_edges: list[Edge] = []
        current = self.length
        need_even_state = True

        while current > 0:
            if need_even_state:
                previous = table.even_predecessors[current]
            else:
                previous = table.odd_predecessors[current]

            if previous is None or previous >= current:
                self.logger.error(
                    "Не удалось восстановить путь до %s",
                    current,
                )
                return None

            reversed_edges.append((previous, current))
            current = previous
            need_even_state = not need_even_state

        reversed_edges.reverse()
        result = PartitionResult(tuple(reversed_edges), total_cost)
        self.logger.info(
            "ДП: стоимость=%s, звеньев=%s",
            result.cost,
            result.edge_count,
        )
        return result

    def solve(self) -> PartitionResult | None:
        self.build_dp_table()
        return self.get_optimal_even_path()

    def _get_table(self) -> ParityDPTable:
        if self.table is None:
            return self.build_dp_table()
        return self.table
