from __future__ import annotations

from dataclasses import dataclass
from itertools import chain
from typing import Callable

import networkx as nx
import pytest

from itaxotools.popart_networks import (
    build_mjt, build_mst, build_tcs, build_tsw)
from itaxotools.popart_networks.types import (
    Coloration, Edge, Network, Sequence, Vertex)


@dataclass
class NetworkTest:
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
        assert self.check_networks_equal(self.network, result)

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
        return nx.is_isomorphic(
            g1, g2,
            node_match=cls.value_match,
            edge_match=cls.value_match)

    @staticmethod
    def value_match(u, v):
        return u['value'] == v['value']


@dataclass
class UniversalNetworkTest:
    sequences_fixture: Callable[[], list[Sequence]]
    network_fixture: Callable[[], Network]

    def get_all_tests(self):
        return (
            NetworkTest(self.sequences_fixture, self.network_fixture, algo, {})
            for algo in [build_mjt, build_mst, build_tcs, build_tsw]
        )


@dataclass
class BadNetworkTest(NetworkTest):
    exception: Exception


@dataclass
class BadUniversalNetworkTest(UniversalNetworkTest):
    exception: Exception

    def get_all_bad_tests(self):
        return (
            BadNetworkTest(self.sequences_fixture, self.network_fixture, algo, {}, self.exception)
            for algo in [build_mjt, build_mst, build_tcs, build_tsw]
        )


def sequences_simple() -> list[Sequence]:
    return [
        Sequence('id1', 'A', 'X'),
        Sequence('id2', 'T', 'Y'),
    ]


def sequences_simple_shuffled() -> list[Sequence]:
    return [
        Sequence('id2', 'T', 'Y'),
        Sequence('id1', 'A', 'X'),
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


def sequences_colorless() -> list[Sequence]:
    return [
        Sequence('id1', 'A', ''),
        Sequence('id2', 'T', ''),
    ]


def network_colorless() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'A', '')],
                [],
            ),
            Vertex(
                [Sequence('id2', 'T', '')],
                [],
            ),
        ],
        [
            Edge(0, 1, 1),
        ],
    )


def sequences_gaps() -> list[Sequence]:
    return [
        Sequence('id1', 'AAAA', ''),
        Sequence('id2', '----', ''),
    ]


def network_gaps() -> Network:
    return Network(
        [
            Vertex(
                [
                    Sequence('id1', 'AAAA', ''),
                    Sequence('id2', 'T', ''),
                ],
                [],
            ),
        ],
        [],
    )


def sequences_two_mutations() -> list[Sequence]:
    return [
        Sequence('id1', 'AC', 'X'),
        Sequence('id2', 'GT', 'Y'),
    ]


def network_two_mutations() -> Network:
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


def sequences_cluster() -> list[Sequence]:
    return [
        Sequence('id1_1', 'AC', 'X'),
        Sequence('id1_2', 'AC', 'X'),
        Sequence('id1_3', 'AC', 'X'),
        Sequence('id2_1', 'GT', 'Y'),
        Sequence('id2_2', 'GT', 'X'),
    ]


def network_cluster() -> Network:
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


def sequences_mst_simple() -> list[Sequence]:
    return [
        Sequence('id1', 'AAAA', ''),
        Sequence('id2', 'TAAA', ''),
        Sequence('id3', 'TAAC', ''),
    ]


def network_mst_simple() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'AAAA', '')],
                [],
            ),
            Vertex(
                [Sequence('id2', 'TAAA', '')],
                [],
            ),
            Vertex(
                [Sequence('id3', 'TAAC', '')],
                [],
            ),
        ],
        [
            Edge(0, 1, 1),
            Edge(1, 2, 1),
        ],
    )


def network_mst_epsilon() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'AAAA', '')],
                [],
            ),
            Vertex(
                [Sequence('id2', 'TAAA', '')],
                [],
            ),
            Vertex(
                [Sequence('id3', 'TAAC', '')],
                [],
            ),
        ],
        [
            Edge(0, 1, 1),
            Edge(1, 2, 1),
            Edge(0, 2, 2),
        ],
    )


def sequences_mjt_simple() -> list[Sequence]:
    return [
        Sequence('id1', 'AAAAAA', ''),
        Sequence('id2', 'CAAACC', ''),
        Sequence('id3', 'GAAACC', ''),
    ]


def network_mjt_simple() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'AAAAAA', '')],
                [],
            ),
            Vertex(
                [Sequence('id2', 'CAAACC', '')],
                [],
            ),
            Vertex(
                [Sequence('id3', 'GAAACC', '')],
                [],
            ),
            Vertex(
                [],
                [],
            ),
        ],
        [
            Edge(1, 2, 1),
            Edge(1, 3, 1),
            Edge(2, 3, 1),
            Edge(0, 3, 2),
        ],
    )


def network_mjt_epsilon() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'AAAAAA', '')],
                [],
            ),
            Vertex(
                [Sequence('id2', 'CAAACC', '')],
                [],
            ),
            Vertex(
                [Sequence('id3', 'GAAACC', '')],
                [],
            ),
            Vertex(
                [],
                [],
            ),
        ],
        [
            Edge(1, 2, 1),
            Edge(1, 3, 1),
            Edge(2, 3, 1),
            Edge(0, 3, 2),
            Edge(0, 1, 3),
            Edge(0, 2, 3),
        ],
    )


def sequences_tsw_simple() -> list[Sequence]:
    return [
        Sequence('id1', 'AAAAAA', 'X'),
        Sequence('id2', 'CAAACC', 'Y'),
        Sequence('id3', 'GAAACC', 'Z'),
    ]


def network_tsw_simple() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'AAAAAA', 'X')],
                [Coloration('X', 1)],
            ),
            Vertex(
                [Sequence('id2', 'CAAACC', 'Y')],
                [Coloration('Y', 1)],
            ),
            Vertex(
                [Sequence('id3', 'GAAACC', 'Z')],
                [Coloration('Z', 1)],
            ),
            Vertex(
                [],
                [],
            ),
        ],
        [
            Edge(1, 3, 1),
            Edge(2, 3, 1),
            Edge(0, 3, 3),
        ],
    )



def sequences_tcs_simple() -> list[Sequence]:
    return [
        Sequence('id1', 'TA', ''),
        Sequence('id2', 'GC', ''),
        Sequence('id3', 'CT', ''),
    ]


def network_tcs_simple() -> Network:
    return Network(
        [
            Vertex(
                [Sequence('id1', 'TA', '')],
                [],
            ),
            Vertex(
                [Sequence('id2', 'GC', '')],
                [],
            ),
            Vertex(
                [Sequence('id3', 'CT', '')],
                [],
            ),
            Vertex(
                [],
                [],
            ),
        ],
        [
            Edge(0, 3, 1),
            Edge(1, 3, 1),
            Edge(2, 3, 1),
        ],
    )


def sequences_line_long(count: int, duplicates: int = 1) -> list[Sequence]:
    return [
        Sequence(f'id{x}', 'A' * x + 'C' * (count - x), f'sub{x}')
        for _ in range(duplicates)
        for x in range(count)
    ]


def network_line_long(count: int, duplicates: int = 1) -> Network:
    vertices = [
        Vertex(
            [Sequence(f'id{x}', 'A' * x + 'C' * (count - x), f'sub{x}')],
            [Coloration(f'sub{x}', duplicates)],
        )
        for x in range(count)
    ]
    edges = [
        Edge(x, x + 1, 1) for x in range(count - 1)
    ]
    return Network(vertices, edges)


networks_tests_universal = [
    UniversalNetworkTest(sequences_simple, network_simple),
    UniversalNetworkTest(sequences_simple_shuffled, network_simple),
    UniversalNetworkTest(sequences_colorless, network_colorless),
    UniversalNetworkTest(sequences_two_mutations, network_two_mutations),
    UniversalNetworkTest(sequences_cluster, network_cluster),
    # UniversalNetworkTest(sequences_gaps, network_gaps),

    UniversalNetworkTest(lambda: sequences_line_long(10, 1), lambda: network_line_long(10, 1)),
    UniversalNetworkTest(lambda: sequences_line_long(1, 10), lambda: network_line_long(1, 10)),
]


network_tests = [
    *chain(*(test.get_all_tests() for test in networks_tests_universal)),

    NetworkTest(sequences_mst_simple, network_mst_simple, build_mst, {}),
    NetworkTest(sequences_mst_simple, network_mst_epsilon, build_mst, dict(epsilon=1)),

    NetworkTest(sequences_mjt_simple, network_mjt_simple, build_mjt, {}),
    NetworkTest(sequences_mjt_simple, network_mjt_epsilon, build_mjt, dict(epsilon=1)),

    NetworkTest(sequences_tsw_simple, network_tsw_simple, build_tsw, {}),

    NetworkTest(sequences_tcs_simple, network_tcs_simple, build_tcs, {}),

    NetworkTest(lambda: sequences_line_long(500), lambda: network_line_long(500), build_mst, {}),
    NetworkTest(lambda: sequences_line_long(1, 500), lambda: network_line_long(1, 500), build_mst, {}),
]


@pytest.mark.parametrize('test', network_tests)
def test_algorithms(test: NetworkTest) -> None:
    test.validate()


def sequences_bad_seq() -> list[Sequence]:
    return [
        Sequence('id1', 'C', 'X'),
        Sequence('id2', 'G', 'Y'),
    ]


def sequences_bad_color() -> list[Sequence]:
    return [
        Sequence('id1', 'A', 'm'),
        Sequence('id2', 'T', 'n'),
    ]


def sequences_bad_length() -> list[Sequence]:
    return [
        Sequence('id1', 'A', ''),
        Sequence('id2', 'AA', ''),
    ]


networks_tests_bad_universal = [
    BadUniversalNetworkTest(sequences_bad_seq, network_simple, AssertionError),
    BadUniversalNetworkTest(sequences_bad_color, network_simple, AssertionError),
    # BadUniversalNetworkTest(sequences_bad_length, None, ValueError),
]


network_tests_bad = [
    *chain(*(test.get_all_bad_tests() for test in networks_tests_bad_universal))
]


@pytest.mark.parametrize('test', network_tests_bad)
def test_algorithms_bad(test: NetworkTest) -> None:
    with pytest.raises(test.exception):
        test.validate()
