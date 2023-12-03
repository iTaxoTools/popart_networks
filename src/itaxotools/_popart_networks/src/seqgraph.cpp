#include "seqgraph.hpp"

#include "MinSpanNet.h"
#include "MedJoinNet.h"
#include "TightSpanWalker.h"
#include "TCS.h"
#ifndef DISABLE_INTNJ
#include "IntNJ.h"
#endif

#include <cassert>
#include <cmath>

SeqGraph::SeqGraph(std::vector<Sequence*> const& s, PopartNetworkAlgo a, bool moID):
	algo{a},
	p0{nullptr},
	p1{nullptr},
	seqs{s}{
}

void SeqGraph::setColoringFromMoID(){
	for(Sequence* s: seqs){
		std::string name = s->name();
		size_t i = 0;
		while(i < name.size() && name[i] != '|')
			++i;

		if(i < name.size()){
			s->setName(name.substr(0, i));
			coloring[s] = name.substr(i+1);
		} else
			coloring[s] = name;
	}
}
void SeqGraph::calc(){
	switch(algo){
		case MINIMUM_SPANNING_TREE:
			if(p0)
				g = new MinSpanNet(seqs, std::vector<bool>{}, *((unsigned*)p0));
			else
				g = new MinSpanNet(seqs, std::vector<bool>{});
			break;
		case MED_JOIN_NET:
			if(p0)
				g = new MedJoinNet(seqs, std::vector<bool>{}, *((unsigned*)p0));
			else
				g = new MedJoinNet(seqs, std::vector<bool>{});
			break;
#ifndef DISABLE_INTNJ
		case INTEGER_NJ_NET:
			if(p0)
				if(p1)
					g = new IntNJ(seqs, std::vector<bool>{}, *((double*)p0), *((int*)p1));
				else
					g = new IntNJ(seqs, std::vector<bool>{}, *((double*)p0));
			else
				g = new IntNJ(seqs, std::vector<bool>{});
			break;
#endif
		case TIGHT_SPAN_WALKER:
			g = new TightSpanWalker(seqs, std::vector<bool>{});
			break;
		case TCS_NETWORK:
			g = new TCS(seqs, std::vector<bool>{});
			break;
		default:
			fprintf(stderr, "Error: Algorithm not recognized!\n");
	}

	g->setupGraph();

	for(size_t i = 0; i < g->vertexCount(); ++i){
		Vertex const* v = g->vertex(i);
		SeqVertex sv;
		for(Sequence* s: seqs)
			if(s->name() == v->label())
				sv.seqs.push_back(s);
		vertices.push_back(sv);
	}

	for(size_t i = 0; i < g->edgeCount(); ++i){
		Edge const* e = g->edge(i);
		SeqEdge se;

		se.v1 = -1;
		for(size_t i = 0; i < g->vertexCount(); ++i)
			if(g->vertex(i) == e->from()){
				se.v1 = i;
				break;
			}

		se.v2 = -2;
		for(size_t i = 0; i < g->vertexCount(); ++i)
			if(g->vertex(i) == e->to()){
				se.v2 = i;
				break;
			}

		se.w = ceil(e->weight());

		edges.push_back(se);
	}

	for(Sequence* s: seqs)
		for(SeqVertex& sv: vertices)
			if(sv.seqs.front()->seq() == s->seq()){
				if(sv.seqs.front() != s)
					sv.seqs.push_back(s);
				sv.pops[coloring[s]]++;
				break;
			}
}
void SeqGraph::print() const{
	printf("Sequences:\n");
	for(Sequence const* s: seqs)
		printf("%-15s %s\n", s->name().c_str(), s->seq().c_str());

	printf("Vertices:\n");
	for(size_t i = 0; i < vertices.size(); ++i){
		for(Sequence const* s: vertices[i].seqs)
			printf("%2zu: %-15s\n", i, s->name().c_str());
		for(std::pair<std::string, int> pop: vertices[i].pops)
			printf("\t%-25s: %2i\n", pop.first.c_str(), pop.second);
	}

	printf("Edges:\n");
	for(SeqEdge const& se: edges)
		printf("%2i -> %2i: %2i\n", se.v1, se.v2, se.w);

	printf("Coloring:\n");
	for(std::pair<Sequence*, std::string> c: coloring)
		printf("%-15s %s\n", c.first->name().c_str(), c.second.c_str());
}
