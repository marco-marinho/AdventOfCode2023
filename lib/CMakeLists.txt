cmake_minimum_required(VERSION 3.18)

project(advent_lib)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

add_subdirectory(extern/pybind11)
add_subdirectory(cffiTools)
pybind11_add_module(day17_pybind day17/day17.cpp)

add_library(day21 day21/day21.c)
target_include_directories(day21 PRIVATE day21)

cffi_add_module(day21)

get_target_property(day21_path day21 CFFI_MODULE_PATH)

install(
        FILES $<TARGET_FILE:day17_pybind> ${day21_path}
        DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/../src/native)
