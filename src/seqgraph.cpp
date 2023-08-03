#include "seqgraph.hpp"

#include "networks/MinSpanNet.h"
#include "networks/MedJoinNet.h"
#include "networks/IntNJ.h"
#include "networks/TightSpanWalker.h"
#include "networks/TCS.h"

#include <cassert>

SeqGraph::SeqGraph(std::vector<Sequence*> const& s, PopartNetworkAlgo algo, bool moID){
	seqs = s;
	if(moID)
		setColoringFromMoID();

	switch(algo){
		case MINIMUM_SPANNING_TREE:
			g = new MinSpanNet(seqs, std::vector<bool>{});
			break;
		case MED_JOIN_NET:
			g = new MedJoinNet(seqs, std::vector<bool>{});
			break;
		case INTEGER_NJ_NET:
			g = new IntNJ(seqs, std::vector<bool>{});
			break;
		case TIGHT_SPAN_WALKER:
			g = new TightSpanWalker(seqs, std::vector<bool>{});
			break;
		case TCS_NETWORK:
			g = new TCS(seqs, std::vector<bool>{});
			break;
		default:
			fprintf(stderr, "Error: Algorithm not recognized!\n");
	}
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

		se.w = e->weight();

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

std::vector<std::vector<Sequence*>> temppackSequences(std::vector<Sequence*> const& seqs){
	std::vector<std::vector<Sequence*>> pack;
	for(Sequence* s: seqs){
		for(std::vector<Sequence*>& packSeq: pack)
			if(s->seq() == packSeq.front()->seq()){
				packSeq.push_back(s);
				goto packNextSeq;
			}
		pack.push_back(std::vector<Sequence*>{});
		pack.back().push_back(s);
packNextSeq:
		continue;
	}
	return pack;
}
std::map<std::string, int> tempgetColors(std::vector<std::vector<Sequence*>>& pack, std::map<Sequence*, std::string>& coloring, size_t index){
	std::map<std::string, int> colors;

	for(Sequence* s: pack[index]){
		if(!colors.count(coloring[s]))
			colors[coloring[s]] = 0;
		++colors[coloring[s]];
	}

	return colors;
}
std::map<std::string, int> tempgetColors(std::vector<std::vector<Sequence*>>& pack, std::map<Sequence*, std::string>& coloring, std::string seqName){
	for(size_t i = 0; i < pack.size(); ++i)
		for(Sequence* s: pack[i])
			if(s->name() == seqName)
				return tempgetColors(pack, coloring, i);
	assert(false);
	return std::map<std::string, int>{};
}
