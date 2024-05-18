.PHONY: all build clean

all: build

build:
ifeq ($(OS),Windows_NT)
	cmake -G "Visual Studio 17 2022" -B build lib
	cmake --build build --config Release --target install
else
	cmake -G Ninja -Bbuild lib -D CMAKE_BUILD_TYPE=Release
	cmake --build build --target install
endif

clean:
	rm -fr build
	rm -f src/native/*.so src/native/*.pyd src/native/*.dll
	rm -f lib/day21_cffi.*