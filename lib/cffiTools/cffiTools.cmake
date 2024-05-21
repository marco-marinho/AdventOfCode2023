function(cffi_add_module target_name)
    set(oneValueArgs NAME WORKING_DIR OUTPUT_DIR)
    set(multiValueArgs HEADER_PATHS LIBRARY_PATHS CDEF_PATHS LIBRARIES)
    cmake_parse_arguments(ARG "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

    if (NOT DEFINED ARG_NAME)
        set(ARG_NAME ${target_name}_cffi)
    endif()

    if (NOT DEFINED ARG_LIBRARIES)
        set(ARG_LIBRARIES ${target_name})
    endif()

    if (NOT DEFINED ARG_HEADER_PATHS)
        get_target_property(ARG_HEADER_PATHS ${target_name} INCLUDE_DIRECTORIES)
    endif()

    if (NOT DEFINED ARG_CDEF_PATHS)
        get_target_property(ARG_CDEF_PATHS ${target_name} INCLUDE_DIRECTORIES)
    endif()

    set(target_binary $<TARGET_FILE_DIR:${target_name}>)

    find_package(Python COMPONENTS Interpreter)

    execute_process(
            COMMAND
            "${Python_EXECUTABLE}" "-c"
            "import sys, importlib; s = importlib.import_module('distutils.sysconfig' if sys.version_info < (3, 10) else 'sysconfig'); print(s.get_config_var('EXT_SUFFIX') or s.get_config_var('SO'))"
            OUTPUT_VARIABLE PYTHON_MODULE_EXT
            OUTPUT_STRIP_TRAILING_WHITESPACE)

    set_target_properties(${target_name} PROPERTIES CFFI_MODULE_NAME "${ARG_NAME}${PYTHON_MODULE_EXT}")
    set_target_properties(${target_name} PROPERTIES CFFI_MODULE_PATH "${target_binary}/${ARG_NAME}${PYTHON_MODULE_EXT}")

    add_custom_command(
            TARGET ${target_name} POST_BUILD
            COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_FUNCTION_LIST_DIR}/build_wrapper.py -I ${ARG_HEADER_PATHS}
            -W ${target_binary} -D ${ARG_CDEF_PATHS} -N ${ARG_NAME} -l ${ARG_LIBRARIES}
            COMMENT "Generating CFFI wrapper for ${target_name}")

endfunction()