from cffi import FFI

ffibuilder = FFI()

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""
    void day21_step(uint32_t *iboard, uint32_t *oboard, int rows, int cols, int nsteps, uint32_t *results);
""")

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
ffibuilder.set_source("day21_cffi",
                      """
                          void day21_step(uint32_t *iboard, uint32_t *oboard, int rows, int cols, int nsteps, uint32_t *results);
                      """,
                      libraries=['day21'],
                      library_dirs=["../../build"],
                      extra_link_args=["-Wl,-rpath,$ORIGIN"])  # library name, for the linker

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
