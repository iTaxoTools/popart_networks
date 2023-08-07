from __future__ import annotations

from typing import NamedTuple, Callable
from itertools import chain

import pytest
import networkx as nx

from itaxotools.popart_networks import build_mst, build_mjt, build_tsw, build_tcs
from itaxotools.popart_networks.types import Sequence, Network, Vertex, Edge, Coloration


class NetworkTest(NamedTuple):
    sequences_fixture: Callable[[], list[Sequence]]
    network_fixture: Callable[[], Network]
    method: Callable
    parameters: dict[str, object]

    @property
    def sequences(self) -> list[Sequence]:
        return self.sequences_fixture()

    @property
    def network(self) -> Network:
        return self.network_fixture()

    def validate(self):
        result = self.method(self.sequences, **self.parameters)
        print('fixture', self.network)
        print('result', result)
        assert(self.check_networks_equal(self.network, result))

    @classmethod
    def graph_from_network(cls, n: Network) -> nx.Graph:
        g = nx.Graph()
        for i, v in enumerate(n.vertices):
            g.add_node(i, value=v)
        for e in n.edges:
            g.add_edge(e.u, e.v, value=e.d)
        return g

    @classmethod
    def check_networks_equal(cls, n1: Network, n2: Network) -> bool:
        g1 = cls.graph_from_network(n1)
        g2 = cls.graph_from_network(n2)
        return nx.is_isomorphic(g1, g2,
            node_match=cls.value_match,
            edge_match=cls.value_match)

    @staticmethod
    def value_match(u, v):
        return u['value'] == v['value']


class UniversalNetworkTest(NamedTuple):
    sequences_fixture: Callable[[], list[Sequence]]
    network_fixture: Callable[[], Network]

    def get_all_tests(self):
        return (
            NetworkTest(self.sequences_fixture, self.network_fixture, algo, {})
            for algo in [build_mjt, build_mst, build_tcs, build_tsw]
        )



def sequences_simple() -> list[Sequence]:
    return [
        Sequence('id1', 'A', 'X'),
        Sequence('id2', 'T', 'Y'),
    ]


def network_simple() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'A', 'X')],
                [Coloration('X', 1)],
            ),
            Vertex(
                [Sequence('id2', 'T', 'Y')],
                [Coloration('Y', 1)],
            ),
        ],
        [
            Edge(0, 1, 1),
        ],
    )


def sequences_simple_two_mutations() -> list[Sequence]:
    return [
        Sequence('id1', 'AC', 'X'),
        Sequence('id2', 'GT', 'Y'),
    ]


def network_simple_two_mutations() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'AC', 'X')],
                [Coloration('X', 1)],
            ),
            Vertex(
                [Sequence('id2', 'GT', 'Y')],
                [Coloration('Y', 1)],
            ),
        ],
        [
            Edge(0, 1, 2),
        ],
    )


def sequences_simple_cluster() -> list[Sequence]:
    return [
        Sequence('id1_1', 'AC', 'X'),
        Sequence('id1_2', 'AC', 'X'),
        Sequence('id1_3', 'AC', 'X'),
        Sequence('id2_1', 'GT', 'Y'),
        Sequence('id2_2', 'GT', 'X'),
    ]


def network_simple_cluster() -> Network:
    return Network(
        [
            Vertex(
                [
                    Sequence('id1_1', 'AC', 'X'),
                    Sequence('id1_2', 'AC', 'X'),
                    Sequence('id1_3', 'AC', 'X'),
                ],
                [
                    Coloration('X', 3),
                ],
            ),
            Vertex(
                [
                    Sequence('id2_2', 'GT', 'X'),
                    Sequence('id2_1', 'GT', 'Y'),
                ],
                [
                    Coloration('X', 1),
                    Coloration('Y', 1),
                ],
            ),
        ],
        [
            Edge(0, 1, 2),
        ],
    )


def sequences_simple_shuffled() -> list[Sequence]:
    return [
        Sequence('id2', 'T', 'Y'),
        Sequence('id1', 'A', 'X'),
    ]


def sequences_simple_bad_seq() -> list[Sequence]:
    return [
        Sequence('id1', 'C', 'X'),
        Sequence('id2', 'G', 'Y'),
    ]


def sequences_simple_bad_color() -> list[Sequence]:
    return [
        Sequence('id1', 'A', 'm'),
        Sequence('id2', 'T', 'n'),
    ]


networks_tests_universal = [
    UniversalNetworkTest(sequences_simple, network_simple),
    UniversalNetworkTest(sequences_simple_shuffled, network_simple),
    UniversalNetworkTest(sequences_simple_two_mutations, network_simple_two_mutations),
    UniversalNetworkTest(sequences_simple_cluster, network_simple_cluster),
]


network_tests = [
    *chain(*(test.get_all_tests() for test in networks_tests_universal))
]


@pytest.mark.parametrize('test', network_tests)
def test_algorithms(test: NetworkTest) -> None:
    test.validate()


networks_tests_bad_universal = [
    UniversalNetworkTest(sequences_simple_bad_seq, network_simple),
    UniversalNetworkTest(sequences_simple_bad_color, network_simple),
]


network_tests_bad = [
    *chain(*(test.get_all_tests() for test in networks_tests_bad_universal))
]


@pytest.mark.parametrize('test', network_tests_bad)
def test_algorithms_bad(test: NetworkTest) -> None:
    with pytest.raises(AssertionError):
        test.validate()
