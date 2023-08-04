#ifndef SEQVERTEX_HPP
#define SEQVERTEX_HPP

#include <map>
#include <vector>
#include <string>

class Sequence;

class SeqVertex{
public:
	std::vector<Sequence*> seqs;
	std::map<std::string, int> pops;
};

#endif
