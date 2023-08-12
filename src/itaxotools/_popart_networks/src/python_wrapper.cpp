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
	"_popart_networks",
	NULL,
	-1,
	pnFuncs,
	0,
	0,
	0,
	0
};

PyMODINIT_FUNC PyInit__popart_networks(){
	return PyModule_Create(&pnModule);
}

PyObject* calcGraphOutput(SeqGraph const& g){
	PyObject* gl = PyTuple_New(2);

	PyObject* vl = PyList_New(g.vertices.size());
	PyTuple_SetItem(gl, 0, vl);

	for(size_t i = 0; i < g.vertices.size(); ++i){
		SeqVertex const& v = g.vertices[i];

		PyObject* pyV = PyTuple_New(2);
		PyList_SetItem(vl, i, pyV);

		PyObject* pyVSeqs = PyList_New(v.seqs.size());
		PyTuple_SetItem(pyV, 0, pyVSeqs);

		for(size_t j = 0; j < v.seqs.size(); ++j){
			Sequence* s = v.seqs[j];
			std::string c = g.coloring.at(s);

			PyObject* pyVSeq = PyTuple_New(3);
			PyList_SetItem(pyVSeqs, j, pyVSeq);

			PyObject* pyVSeqName = PyUnicode_FromString(s->name().c_str());
			PyObject* pyVSeqData = PyUnicode_FromString(s->seq().c_str());
			PyObject* pyVSeqPop  = PyUnicode_FromString(c.c_str());
			PyTuple_SetItem(pyVSeq, 0, pyVSeqName);
			PyTuple_SetItem(pyVSeq, 1, pyVSeqData);
			PyTuple_SetItem(pyVSeq, 2, pyVSeqPop);
		}

		PyObject* pyVPops = PyList_New(0);
		PyTuple_SetItem(pyV, 1, pyVPops);

		for(std::pair<std::string, int> pop: v.pops){
			if(!pop.first.size())
				continue;
			PyObject* pyVPop = PyTuple_New(2);
			PyObject* pyVPopName  = PyUnicode_FromString(pop.first.c_str());
			PyObject* pyVPopCount = PyLong_FromLong(pop.second);
			PyTuple_SetItem(pyVPop, 0, pyVPopName);
			PyTuple_SetItem(pyVPop, 1, pyVPopCount);

			PyList_Append(pyVPops, pyVPop);
		}
	}

	PyObject* el = PyList_New(g.edges.size());
	PyTuple_SetItem(gl, 1, el);

	for(size_t i = 0; i < g.edges.size(); ++i){
		SeqEdge const& e = g.edges[i];

		PyObject* pyE = PyTuple_New(3);
		PyList_SetItem(el, i, pyE);

		PyObject* pyEV1 = PyLong_FromLong(e.v1);
		PyObject* pyEV2 = PyLong_FromLong(e.v2);
		PyObject* pyEW  = PyLong_FromLong(e.w);
		PyTuple_SetItem(pyE, 0, pyEV1);
		PyTuple_SetItem(pyE, 1, pyEV2);
		PyTuple_SetItem(pyE, 2, pyEW);
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

		const char *c_name, *c_data, *c_color;

		if (!PyArg_ParseTuple(pySeq, "sss", &c_name, &c_data, &c_color)) {
			return NULL;
		}

		std::string name = c_name;
		std::string data = c_data;
		std::string color = c_color;

		Sequence* seq = new Sequence{name, data};
		seqs.push_back(seq);

		if (!color.empty())
			coloring[seq] = color;
	}

	long algo = PyLong_AsLong(pyAlgo);
	SeqGraph g{seqs, (PopartNetworkAlgo)algo};
	unsigned p0U;
#ifndef DISABLE_INTNJ
	double   p0D;
	int      p1I;
#endif
	switch(algo){
		case MINIMUM_SPANNING_TREE:
		case MED_JOIN_NET:
			if(PyTuple_Size(args) >= 3){
				PyObject* pyP = PyTuple_GetItem(args, 2);
				p0U = PyLong_AsLong(pyP);
				g.p0 = &p0U;
			}
			break;
#ifndef DISABLE_INTNJ
		case INTEGER_NJ_NET:
			if(PyTuple_Size(args) >= 3){
				PyObject* pyP = PyTuple_GetItem(args, 2);
				p0D = PyLong_AsDouble(pyP);
				g.p0 = &p0D;
			}
			if(PyTuple_Size(args) >= 4){
				PyObject* pyP = PyTuple_GetItem(args, 3);
				p1I = PyLong_AsLong(pyP);
				g.p1 = &p1I;
			}
			break;
#endif
	}
	g.coloring = coloring;


    try {
		g.calc();
    }
    catch (const UnequalSequencesError& e) {
        PyErr_SetString(PyExc_ValueError, e.what());
		return NULL;
    }
    catch (const std::runtime_error& e) {
        PyErr_SetString(PyExc_RuntimeError, e.what());
		return NULL;
    }


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
