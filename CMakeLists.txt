cmake_minimum_required(VERSION 3.15...3.26)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

find_package(
    Python
    COMPONENTS Interpreter Development.Module
    REQUIRED)


file(GLOB POPART_SOURCES
    ${PROJECT_SOURCE_DIR}/src/popart/src/networks/*.cpp
    ${PROJECT_SOURCE_DIR}/src/popart/src/tree/*.cpp
    ${PROJECT_SOURCE_DIR}/src/popart/src/seqio/*.cpp
)
list(REMOVE_ITEM POPART_SOURCES
    ${PROJECT_SOURCE_DIR}/src/popart/src/networks/IntNJ.cpp
)
set(POPART_INCLUDE_DIRS
    ${PROJECT_SOURCE_DIR}/src/popart/src/networks
    ${PROJECT_SOURCE_DIR}/src/popart/src/seqio
    ${PROJECT_SOURCE_DIR}/src/popart/src/tree
)
add_library(popart STATIC ${POPART_SOURCES})
target_include_directories(popart PUBLIC ${POPART_INCLUDE_DIRS})
set_property(TARGET popart PROPERTY CXX_STANDARD 11)


file(GLOB PYMODULE_SOURCES
    ${PROJECT_SOURCE_DIR}/src/itaxotools/_popart_networks/src/*.cpp
)
set(PYMODULE_INCLUDE_DIRS
    ${PROJECT_SOURCE_DIR}/src/itaxotools/_popart_networks/include
)

python_add_library(_popart_networks MODULE ${PYMODULE_SOURCES} WITH_SOABI)
target_include_directories(_popart_networks PRIVATE ${PYMODULE_INCLUDE_DIRS})
target_link_libraries(_popart_networks PRIVATE popart)
target_compile_definitions(_popart_networks PRIVATE -DDISABLE_INTNJ)
set_property(TARGET popart PROPERTY CXX_STANDARD 17)

install(TARGETS _popart_networks DESTINATION itaxotools)
