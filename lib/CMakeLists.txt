cmake_minimum_required(VERSION 3.4...3.18)

project(advent_lib)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

if (UNIX)
    set(CMAKE_CXX_FLAGS_RELEASE "-O3")
endif (UNIX)

if (MSVC)
    set(CMAKE_CXX_FLAGS_RELEASE "/O2")
endif (MSVC)

add_subdirectory(extern/pybind11)

pybind11_add_module(day17_pybind day17/day17.cpp)

add_library(day21 SHARED day21/day21.c)