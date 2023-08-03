#include "python_wrapper.h"
#include "seqgraph.hpp"

#include <cassert>
#include <vector>

static PyMethodDef pnFuncs[]{
	{"calcGraph", calcGraph, METH_VARARGS, "Calculate the graph from given sequences and optional populations"},
	{NULL, NULL, 0, NULL}
};
static struct PyModuleDef pnModule{
	PyModuleDef_HEAD_INIT,
	"popart_networks",
	NULL,
	-1,
	pnFuncs,
	0,
	0,
	0,
	0
};

PyMODINIT_FUNC PyInit_popart_networks(){
	return PyModule_Create(&pnModule);
}

inline char const* getStrFromList(PyObject* l, Py_ssize_t i){
	PyObject* str = PyList_GetItem(l, i);
	assert(PyUnicode_Check(str));
	return PyUnicode_AsUTF8(str);
}
PyObject* calcGraphOutput(SeqGraph const& g){
	PyObject* gl = PyList_New(2);

	PyObject* vl = PyList_New(g.vertices.size());
	PyList_SetItem(gl, 0, vl);

	for(size_t i = 0; i < g.vertices.size(); ++i){
		SeqVertex const& v = g.vertices[i];

		PyObject* pyV = PyList_New(2);
		PyList_SetItem(vl, i, pyV);

		PyObject* pyVSeqs = PyList_New(v.seqs.size());
		PyList_SetItem(pyV, 0, pyVSeqs);

		for(size_t j = 0; j < v.seqs.size(); ++j){
			Sequence* s = v.seqs[j];

			PyObject* pyVSeq = PyList_New(3);
			PyList_SetItem(pyVSeqs, j, pyVSeq);

			PyObject* pyVSeqName = PyUnicode_FromString(s->name().c_str());
			PyObject* pyVSeqData = PyUnicode_FromString(s->seq().c_str());
			PyObject* pyVSeqPop  = PyUnicode_FromString(g.coloring.at(s).c_str());
			PyList_SetItem(pyVSeq, 0, pyVSeqName);
			PyList_SetItem(pyVSeq, 1, pyVSeqData);
			PyList_SetItem(pyVSeq, 2, pyVSeqPop);
		}

		PyObject* pyVPops = PyList_New(v.pops.size());
		PyList_SetItem(pyV, 1, pyVPops);

		size_t j = 0;
		for(std::pair<std::string, int> pop: v.pops){
			PyObject* pyVPop = PyList_New(2);
			PyList_SetItem(pyVPops, j++, pyVPop);

			PyObject* pyVPopName  = PyUnicode_FromString(pop.first.c_str());
			PyObject* pyVPopCount = PyLong_FromLong(pop.second);
			PyList_SetItem(pyVPop, 0, pyVPopName);
			PyList_SetItem(pyVPop, 1, pyVPopCount);
		}
	}

	PyObject* el = PyList_New(g.edges.size());
	PyList_SetItem(gl, 1, el);

	for(size_t i = 0; i < g.edges.size(); ++i){
		SeqEdge const& e = g.edges[i];

		PyObject* pyE = PyList_New(3);
		PyList_SetItem(el, i, pyE);

		PyObject* pyEV1 = PyLong_FromLong(e.v1);
		PyObject* pyEV2 = PyLong_FromLong(e.v2);
		PyObject* pyEW  = PyLong_FromLong(e.w);
		PyList_SetItem(pyE, 0, pyEV1);
		PyList_SetItem(pyE, 1, pyEV2);
		PyList_SetItem(pyE, 2, pyEW);
	}

	return gl;
}
PyObject* calcGraph(PyObject* self, PyObject* args){
	if(PyTuple_Size(args) < 2)
		return NULL;

	PyObject* pySeqs = PyTuple_GetItem(args, 0);
	PyObject* pyAlgo = PyTuple_GetItem(args, 1);
	assert(pySeqs);
	assert(PyList_Check(pySeqs));
	assert(pyAlgo);
	assert(PyLong_Check(pyAlgo));

	std::vector<Sequence*> seqs;
	std::map<Sequence*, std::string> coloring;
	for(Py_ssize_t i = 0; i < PyList_Size(pySeqs); ++i){
		PyObject* pySeq = PyList_GetItem(pySeqs, i);
		assert(PyList_Check(pySeq));
		assert(PyList_Size(pySeq) >= 2);

		std::string name = getStrFromList(pySeq, 0);
		std::string data = getStrFromList(pySeq, 1);

		Sequence* seq = new Sequence{name, data};
		seqs.push_back(seq);

		if(PyList_Size(pySeq) >= 3)
			coloring[seq] = getStrFromList(pySeq, 2);
	}

	long algo = PyLong_AsLong(pyAlgo);
	SeqGraph g{seqs, (PopartNetworkAlgo)algo};
	g.coloring = coloring;
	g.calc();

	PyObject* graphList = calcGraphOutput(g);

	for(Sequence* s: seqs)
		delete s;
	seqs.clear();
	coloring.clear();

	return graphList;
}
/*
 * [
 * 	VertexData,
 * 	EdgeData,
 * ]
 * VertexData:
 * [
 * 	Vertex1,
 * 	Vertex2,
 * ]
 * Vertex:
 * [
 * 	Sequences,
 * 	Populations,
 * ]
 * Sequences:
 * [
 * 	Sequence1,
 * 	Sequence2,
 * ]
 * Sequence:
 * [
 * 	name,
 * 	data,
 * 	pop,
 * ]
 * Populations:
 * [
 * 	Population1,
 * 	Population2,
 * ]
 * Population:
 * [
 * 	Name,
 * 	Count,
 * ]
 * EdgeData:
 * [
 * 	Edge1,
 * 	Edge2,
 * ]
 * Edge:
 * [
 * 	VertexIndex1,
 * 	VertexIndex2,
 * 	weight,
 * ]
 */
