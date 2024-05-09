cmake_minimum_required(VERSION 3.4...3.18)
project(advent_lib)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")
add_subdirectory(extern/pybind11)

pybind11_add_module(day17_pybind day17/day17.cpp)