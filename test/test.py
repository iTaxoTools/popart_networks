#!/usr/bin/env python

from itaxotools import popart_networks as pn

seqs = [
	["seq_1a",  "ATATACGGTGTTATC", "Pan_troglodytes"      ],
	["seq_1b",  "TTATACGGTGTTATC", "Pan_troglodytes"      ],
	["seq_2a",  "TTATACGGGGTTATC", "Pan_troglodytes"      ],
	["seq_2b",  "ATCTACGGGGTTATC", "Pan_troglodytes"      ],
	["seq_3a",  "ATATTCGGGATTATC", "Pan_paniscus"         ],
	["seq_3b",  "ATATACGGGGTTATC", "Pan_paniscus"         ],
	["seq_4a",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_4b",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_5a",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_5b",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_6a",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_6b",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_7a",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_7b",  "ATATACGGGGTAATC", "Homo_sapiens"         ],
	["seq_8a",  "ATATACGGGGTAATC", "Homo_neanderthalensis"],
	["seq_8b",  "ATATACGGGGTAATC", "Homo_neanderthalensis"],
	["seq_9a",  "ATATACGGGGTAATC", "Homo_neanderthalensis"],
	["seq_9b",  "ATATACGGGGTAATC", "Homo_neanderthalensis"],
	["seq_10a", "ATATACGGGGTAATC", "Homo_altaiensis"      ],
	["seq_10b", "ATATACGGGGTAATC", "Homo_altaiensis"      ],
]

g = pn.calcGraph(seqs, 1, 0)
print(g)
