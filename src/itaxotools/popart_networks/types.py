from enum import IntEnum
from typing import NamedTuple


class PopartNetworkAlgo(IntEnum):
    """Mirrors seqgraph.hpp"""
    MINIMUM_SPANNING_TREE = 0
    MED_JOIN_NET = 1
    TIGHT_SPAN_WALKER = 2
    TCS_NETWORK = 3
    INTEGER_NJ_NET = 4


class Sequence(NamedTuple):
    id: str
    seq: str
    color: str


class Coloration(NamedTuple):
    color: str
    weight: int


class Vertex(NamedTuple):
    seqs: list[Sequence]
    colors: list[Coloration]

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return all((
            set(self.seqs) == set(other.seqs),
            set(self.colors) == set(other.colors)
        ))


class Edge(NamedTuple):
    u: int
    v: int
    d: int


class Network(NamedTuple):
    vertices: list[Vertex]
    edges: list[Edge]
