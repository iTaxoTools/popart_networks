#ifndef SEQGRAPH_HPP
#define SEQGRAPH_HPP

#include "seqvertex.hpp"
#include "seqedge.hpp"

#include "networks/HapNet.h"

#include <vector>
#include <string>

enum PopartNetworkAlgo{
	MINIMUM_SPANNING_TREE,
	MED_JOIN_NET,
	INTEGER_NJ_NET,
	TIGHT_SPAN_WALKER,
	TCS_NETWORK,

	POPART_NETWORK_ALGO_COUNT
};

class SeqGraph{
public:
	SeqGraph(std::vector<Sequence*> const& s, PopartNetworkAlgo algo, bool moID = false);
	
	void setColoringFromMoID();
	void calc();
	void print() const;

	HapNet* g;
	std::vector<Sequence*>           seqs;
	std::map<Sequence*, std::string> coloring;
	std::vector<SeqVertex>           vertices;
	std::vector<SeqEdge>             edges;
};

#endif
