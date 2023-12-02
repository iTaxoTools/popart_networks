from __future__ import annotations

from functools import wraps

from .types import Network, Sequence, Vertex


def prune_positions(sequences: list[Sequence], kept: str):
    if not sequences or not kept:
        return []

    positions_pruned = set()

    for sequence in sequences:
        for position, character in enumerate(sequence.seq):
            if character not in kept:
                positions_pruned.add(position)

    if not positions_pruned:
        return sequences

    positions_kept = [
        position
        for position in range(len(sequences[0].seq))
        if position not in positions_pruned
    ]

    pruned_sequences = []
    for old_sequence in sequences:
        old_seq = old_sequence.seq
        pruned_seq = "".join([old_seq[i] for i in positions_kept])
        pruned_sequence = Sequence(
            id=old_sequence.id,
            seq=pruned_seq,
            color=old_sequence.color,
        )
        pruned_sequences.append(pruned_sequence)

    return pruned_sequences


def replace_character(sequences: list[Sequence], old: str, new: str):
    return [Sequence(s.id, s.seq.replace(old, new), s.color) for s in sequences]


def preparse_input(input: iter[tuple[str, str, str]]):
    input = list(Sequence(*s) for s in input)
    input = prune_positions(input, "ATCG-")
    input = replace_character(input, "-", "!")
    return input


def preparse_arguments(args: list, kwargs: dict):
    if "input" in kwargs:
        kwargs["input"] = preparse_input(kwargs["input"])
    else:
        input = preparse_input(args[0])
        args = (input, *args[1:])
    return args, kwargs


def preparse_result(result: Network):
    return Network(
        [
            Vertex(
                replace_character(v.seqs, "!", "-"),
                v.colors,
            )
            for v in result.vertices
        ],
        result.edges,
    )


def preparse(func):
    """Preparse both input and output for build_* methods"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        args, kwargs = preparse_arguments(args, kwargs)
        result = func(*args, **kwargs)
        return preparse_result(result)

    return wrapper
