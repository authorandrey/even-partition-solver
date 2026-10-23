from collections.abc import Mapping
from math import inf
from numbers import Real

from even_partition.models import Edge


def validate_length(length: int) -> None:
    if length < 0:
        raise ValueError("Length must be >= 0")


def validate_weights(
    length: int,
    weights: Mapping[Edge, Real],
) -> None:
    for edge, weight in weights.items():
        validate_edge(length, edge)
        validate_weight(weight)


def validate_edge(length: int, edge: Edge) -> None:
    if not isinstance(edge, tuple) or len(edge) != 2:
        raise ValueError("Key must ba a pair (start, end)")

    start, end = edge

    if not 0 <= start < end <= length:
        raise ValueError("0 <= start < end <= length")


def validate_weight(weight: Real) -> None:
    if weight != weight or weight == inf or weight == -inf:
        raise ValueError("Infinite weight is unavailable")
