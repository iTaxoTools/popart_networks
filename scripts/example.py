#!/usr/bin/env python

from itaxotools import popart_networks as pn

seqs = [
    pn.Sequence("seq_1a",  "ATATACGGTGTTATC", "Pan_troglodytes"      ),
    pn.Sequence("seq_1b",  "TTATACGGTGTTATC", "Pan_troglodytes"      ),
    pn.Sequence("seq_2a",  "TTATACGGGGTTATC", "Pan_troglodytes"      ),
    pn.Sequence("seq_2b",  "ATCTACGGGGTTATC", "Pan_troglodytes"      ),
    pn.Sequence("seq_3a",  "ATATTCGGGATTATC", "Pan_paniscus"         ),
    pn.Sequence("seq_3b",  "ATATACGGGGTTATC", "Pan_paniscus"         ),
    pn.Sequence("seq_4a",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_4b",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_5a",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_5b",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_6a",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_6b",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_7a",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_7b",  "ATATACGGGGTAATC", "Homo_sapiens"         ),
    pn.Sequence("seq_8a",  "ATATACGGGGTAATC", "Homo_neanderthalensis"),
    pn.Sequence("seq_8b",  "ATATACGGGGTAATC", "Homo_neanderthalensis"),
    pn.Sequence("seq_9a",  "ATATACGGGGTAATC", "Homo_neanderthalensis"),
    pn.Sequence("seq_9b",  "ATATACGGGGTAATC", "Homo_neanderthalensis"),
    pn.Sequence("seq_10a", "ATATACGGGGTAATC", "Homo_altaiensis"      ),
    pn.Sequence("seq_10b", "ATATACGGGGTAATC", "Homo_altaiensis"      ),
]

g = pn.build_mst(seqs)
# g = pn.build_mjt(seqs)
# g = pn.build_tsw(seqs)
# g = pn.build_tcs(seqs)

nodes, edges = g

print('# nodes:', len(nodes))
for i, node in enumerate(nodes):
    seqs, colors = node
    print(f'{i}: #{len(seqs)}: {seqs} -> {colors}')

print()

print('# edges:', len(edges))
for edge in edges:
    print(edge)
