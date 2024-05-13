.PHONY: all build clean

all: build

build:
ifeq ($(OS),Windows_NT)
	cmake -G "Visual Studio 17 2022"  -B build lib -DCMAKE_BUILD_TYPE=Release
	cmake --build build --config Release
	cp build/Release/day17_pybind.*.pyd src/native
else
	cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -Bbuild lib
	cmake --build build
	cp build/day17_pybind.cpython-*-x86_64-linux-gnu.so src/native
	cd lib/day21; python build_day21.py
	cp build/libday21.so src/native
	cp lib/day21/day21_cffi.*.so src/native
endif

clean:
	rm -fr build
	rm -f src/native/*.so src/native/*.pyd
	rm lib/day21/day21_cffi.*