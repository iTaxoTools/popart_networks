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

int main(int argc, char* argv[]){
	std::vector<Sequence*> seqs = testSequences1();

	SeqGraph sg{seqs, MINIMUM_SPANNING_TREE};
	unsigned a = 10;
	sg.p0 = &a;
	sg.calc();
	sg.print();

	for(Sequence* s: seqs)
		delete s;

	return 0;
}
