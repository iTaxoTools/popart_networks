from .._popart_networks import calcGraph
from .types import (
    Coloration, Edge, Network, PopartNetworkAlgo, Sequence, Vertex)


def _format_vertex(v: tuple[list[tuple], list[tuple]]) -> Vertex:
    return Vertex(
        list(Sequence(*s) for s in v[0]),
        list(Coloration(*c) for c in v[1])
    )


def _format_output(g: tuple[list[tuple], list[tuple]]) -> Network:
    return Network(
        list(_format_vertex(v) for v in g[0]),
        list(Edge(*e) for e in g[1])
    )


def build_mst(input: list[Sequence], epsilon: int = 0) -> Network:
    """Build minimum spanning tree network"""
    algo = PopartNetworkAlgo.MINIMUM_SPANNING_TREE
    g = calcGraph(input, algo, epsilon)
    return _format_output(g)


def build_mjt(input: list[Sequence], epsilon: int = 0) -> Network:
    """Build median joining network"""
    algo = PopartNetworkAlgo.MED_JOIN_NET
    g = calcGraph(input, algo, epsilon)
    return _format_output(g)


def build_tsw(input: list[Sequence]) -> Network:
    """Build tight span walker network"""
    algo = PopartNetworkAlgo.TIGHT_SPAN_WALKER
    g = calcGraph(input, algo)
    return _format_output(g)


def build_tcs(input: list[Sequence]) -> Network:
    """Build TCS network"""
    algo = PopartNetworkAlgo.TCS_NETWORK
    g = calcGraph(input, algo)
    return _format_output(g)
