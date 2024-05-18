import sys
from cffi import FFI
import argparse
import importlib
from pathlib import Path

ffibuilder = FFI()


def get_libs(lib_folders):
    libs = []
    for folder in map(Path, lib_folders):
        for file in folder.iterdir():
            if file.suffix in [".dll", ".so"]:
                libs.append(file.stem.removeprefix("lib"))
    return libs


def get_headers(header_folders):
    headers = ""
    for folder in map(Path, header_folders):
        for file in folder.iterdir():
            if not file.name.startswith("cdef") and file.suffix == ".h":
                headers += f'#include "{file.name}" \n'
    return headers


def get_cdefs(cdefs_folders):
    cdef = ""
    for folder in map(Path, cdefs_folders):
        for file in folder.iterdir():
            if file.name.startswith("cdef"):
                cdef += open(file, encoding="utf8").read()
    return cdef


if __name__ == "__main__":

    if '.so' in importlib.machinery.EXTENSION_SUFFIXES:
        suffix = '.so'
    elif '.pyd' in importlib.machinery.EXTENSION_SUFFIXES:
        suffix = '.pyd'
    else:
        suffix = '.*'
    parser = argparse.ArgumentParser(description='CFFI Wrapper Builder.')
    parser.add_argument('-L', "--librarydirs", nargs="*",
                        help='Path to folders containing .so/.lib files to link against',
                        type=str, default=["."])
    parser.add_argument('-I', '--includedirs', type=str, default=["includes"],
                        help="Path to folders containing header files to be included", nargs="*")
    parser.add_argument('-N', '--name', type=str, default=None,
                        help="Path to folders containing header files to be included")
    parser.add_argument('-W', '--workingdir', type=str, default=".")
    parser.add_argument("-O", "--outputdir", type=str, default=".")
    parser.add_argument("-D", "--cdefdirs", type=str, default=["."], nargs="*")
    parser.add_argument("-l", "--libraries", type=str, default=None, nargs="*")
    parser.add_argument("-H", "--headers", type=str, default=None, nargs="*")
    args = parser.parse_args()

    ffibuilder.cdef(get_cdefs(args.cdefdirs))

    if args.name is not None and args.libraries is None:
        args.libraries = [args.name]

    if args.libraries is None:
        args.libraries = get_libs(args.librarydirs)

    if args.headers is None:
        args.headers = get_headers(args.includedirs)

    if args.name is None:
        args.name = "_" + args.libraries[0]

    extralinkargs = {"win32": ["/NOIMPLIB", "/NOEXP"], "linux": ["-Wl,-rpath=$ORIGIN"]}
    ffibuilder.set_source(
        args.name,
        args.headers,
        libraries=args.libraries,
        include_dirs=args.includedirs,
        library_dirs=args.librarydirs,
        extra_link_args=extralinkargs[sys.platform]
    )
    ffibuilder.compile(tmpdir=args.workingdir, verbose=True,
                       target=str(Path(args.outputdir).joinpath(args.name + suffix)))
    Path(args.name + ".c").unlink(missing_ok=True)
