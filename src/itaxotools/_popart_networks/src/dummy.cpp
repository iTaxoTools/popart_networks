// Dummy extension so that wheel meta is written correctly by setuptools
// Temporary fast fix, the whole stack should be moved to scikit-build anyway

#include <Python.h>


static PyMethodDef module_methods[] = {
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "_dummy",
    NULL,
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit__popart_networks_dummy(void) {
    return PyModule_Create(&module_definition);
}
