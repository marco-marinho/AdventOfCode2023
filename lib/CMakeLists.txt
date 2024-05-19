cmake_minimum_required(VERSION 3.4...3.18)

project(advent_lib)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

add_subdirectory(extern/pybind11)
pybind11_add_module(day17_pybind day17/day17.cpp)

include_directories(day21)
add_library(day21 SHARED day21/day21.c)

get_target_property(DAY21_BIN day21 BINARY_DIR)
get_filename_component(DAY21_BIN_ABSOLUTE_PATH ${DAY21_BIN} ABSOLUTE)
set(day21_path ${DAY21_BIN_ABSOLUTE_PATH}/$<CONFIG>/day21_cffi.${SO_EXT})
set(day21_binary ${DAY21_BIN_ABSOLUTE_PATH}/$<CONFIG>)

get_property(INC_DIRS DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)

find_package(Python COMPONENTS Interpreter)
add_custom_command(
    TARGET day21 POST_BUILD
    COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/build_wrapper.py -I ${INC_DIRS}
             -W ${day21_binary} -D ${CMAKE_CURRENT_SOURCE_DIR}/day21 -N day21_cffi -l day21
    COMMENT "Generating API wrapper"
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

install(
        FILES $<TARGET_FILE:day21> $<TARGET_FILE:day17_pybind> ${day21_path}
        DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/../src/native
)
