#include "seqgraph.hpp"
#include "networks/MedJoinNet.h"

#include <cstdio>
#include <cassert>

std::vector<Sequence*> testSequences1(){
	std::vector<Sequence*> seqs{};

	seqs.push_back(new Sequence{"seq_1a|Pan_troglodytes",       "ATATACGGTGTTATC"});
	seqs.push_back(new Sequence{"seq_1b|Pan_troglodytes",       "TTATACGGTGTTATC"});
	seqs.push_back(new Sequence{"seq_2a|Pan_troglodytes",       "TTATACGGGGTTATC"});
	seqs.push_back(new Sequence{"seq_2b|Pan_troglodytes",       "ATCTACGGGGTTATC"});
	seqs.push_back(new Sequence{"seq_3a|Pan_paniscus",          "ATATTCGGGATTATC"});
	seqs.push_back(new Sequence{"seq_3b|Pan_paniscus",          "ATATACGGGGTTATC"});
	seqs.push_back(new Sequence{"seq_4a|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_4b|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_5a|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_5b|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_6a|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_6b|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_7a|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_7b|Homo_sapiens",          "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_8a|Homo_neanderthalensis", "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_8b|Homo_neanderthalensis", "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_9a|Homo_neanderthalensis", "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_9b|Homo_neanderthalensis", "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_10a|Homo_altaiensis",      "ATATACGGGGTAATC"});
	seqs.push_back(new Sequence{"seq_10b|Homo_altaiensis",      "ATATACGGGGTAATC"});
	return seqs;
}
std::vector<Sequence*> testSequences2(){
	std::vector<Sequence*> seqs{};

	seqs.push_back(new Sequence{"seq_1", "ATATACGGGGTTA---TTAGA----AAAATGTGTGTGTGTTTTTTTTTTCATGTGG"});
	seqs.push_back(new Sequence{"seq_2", "......--..A..---...C.----.G...C.A...C..C...C............"});
	seqs.push_back(new Sequence{"seq_3", "..........A..---...T.----.G............................."});
	seqs.push_back(new Sequence{"seq_4", "..........A..---G...T----..............................A"});
	seqs.push_back(new Sequence{"seq_5", "..........A..---G...G----..............................C"});
	seqs.push_back(new Sequence{"seq_6", "..........A..---G...C----..............................T"});
	seqs.push_back(new Sequence{"seq_7", "..........A..---G....----..............................A"});

	return seqs;
}
std::map<Sequence*, std::string> testColors(std::vector<Sequence*> const& seqs){
	std::map<Sequence*, std::string> coloring;
	for(Sequence* s: seqs){
		std::string name = s->name();
		//name.pop_back();
		coloring[s] = name;
	}
	return coloring;
}
std::map<Sequence*, std::string> colorsFromMoID(std::vector<Sequence*> const& seqs){
	std::map<Sequence*, std::string> coloring;
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
	return coloring;
}
void fillSequences(std::vector<Sequence*>& seqs){
	for(size_t i = 1; i < seqs.size(); ++i){
		std::string const& seqPrev = seqs[i-1]->seq();
		std::string seq = seqs[i]->seq();
		for(size_t j = 0; j < seq.size(); ++j)
			if(seq[j] == '.')
				seq[j] = seqPrev[j];
		seqs[i]->setSeq(seq);
	}
}
std::vector<std::vector<Sequence*>> packSequences(std::vector<Sequence*> const& seqs){
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
std::map<std::string, int> getColors(std::vector<std::vector<Sequence*>>& pack, std::map<Sequence*, std::string>& coloring, size_t index){
	std::map<std::string, int> colors;

	for(Sequence* s: pack[index]){
		if(!colors.count(coloring[s]))
			colors[coloring[s]] = 0;
		++colors[coloring[s]];
	}

	return colors;
}
std::map<std::string, int> getColors(std::vector<std::vector<Sequence*>>& pack, std::map<Sequence*, std::string>& coloring, std::string seqName){
	for(size_t i = 0; i < pack.size(); ++i)
		for(Sequence* s: pack[i])
			if(s->name() == seqName)
				return getColors(pack, coloring, i);
	assert(false);
	return std::map<std::string, int>{};
}

void test(){
	std::vector<Sequence*> seqs = testSequences1();
	std::map<Sequence*, std::string> coloring = colorsFromMoID(seqs);
	//std::map<Sequence*, std::string> coloring = testColors(seqs);

	HapNet* g = new MedJoinNet(seqs, std::vector<bool>{}, 0);
	g->setupGraph();
	std::cout << std::endl;

	std::cout << *g;

	fillSequences(seqs);
	std::vector<std::vector<Sequence*>> pack = packSequences(seqs);
	for(std::vector<Sequence*>& packSeq: pack){
		printf("%s\n", packSeq.front()->seq().c_str());
		for(Sequence* s: packSeq)
			printf("%s\n", s->name().c_str());
		printf("\n");
	}
	std::map<std::string, int> colors = getColors(pack, coloring, "seq_6b");
	//std::map<std::string, int> colors = getColors(pack, coloring, 6);
	for(std::pair<std::string, int> color: colors)
		printf("%s: %i\n", color.first.c_str(), color.second);

	delete g;
	for(Sequence* s: seqs)
		delete s;
	seqs.clear();
}

int main(int argc, char* argv[]){
	//printf("Hello popart!\n");

	//test();
	//printf("\n");

	std::vector<Sequence*> seqs = testSequences1();
	SeqGraph sg{seqs, MED_JOIN_NET};
	sg.calc();
	sg.print();

	for(Sequence* s: seqs)
		delete s;
	return 0;
}
