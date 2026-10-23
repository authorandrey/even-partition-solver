from dataclasses import dataclass
from numbers import Real
from typing import TypeAlias

Edge: TypeAlias = tuple[int, int]


@dataclass(frozen=True)
class DPTable:
    costs: tuple[Real, ...]
    candidates: tuple[tuple[Real, ...], ...]

    def __getitem__(
        self, key: str
    ) -> tuple[Real, ...] | tuple[tuple[Real, ...], ...]:
        if key == "R":
            return self.costs
        if key == "A":
            return self.candidates
        raise KeyError(key)


@dataclass(frozen=True)
class PartitionResult:
    edges: tuple[Edge, ...]
    cost: Real

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    @property
    def is_even(self) -> bool:
        return self.edge_count % 2 == 0
