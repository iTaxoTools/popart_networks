#ifndef PYTHON_WRAPPER_H
#define PYTHON_WRAPPER_H

#include <Python.h>

PyMODINIT_FUNC PyInit_popart_networks();

static PyObject* calcGraph(PyObject* self, PyObject* args);

#endif

