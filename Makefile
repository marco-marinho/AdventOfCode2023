.PHONY: all build clean

all: build

build:
	cmake -G Ninja -DCMAKE_BUILD_TYPE=Release -Bbuild lib
	cmake --build build
	cp build/day17_pybind.cpython-*-x86_64-linux-gnu.so src/native

clean:
	rm -fr build
	rm -f src/native/*.so