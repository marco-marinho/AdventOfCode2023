import numpy as np
from numba import jit

from util import get_data

try:
    from native.day21_cffi import lib, ffi

    native = True
except ImportError:
    native = False


def parse_to_int(ichar: str):
    match ichar:
        case "#":
            return 0
        case _:
            return 1


@jit(cache=True, fastmath=True)
def step(iboard, ref_board, times):
    output = np.zeros(times)
    steps = ((1, 0), (-1, 0), (0, 1), (0, -1))
    stack = np.argwhere(iboard > 1)
    iboard = ref_board.copy()
    for i in range(times):
        for x, y in stack:
            for dx, dy in steps:
                iboard[x + dx, y + dy] *= 2
        stack = np.argwhere(iboard > 1)
        iboard = ref_board.copy()
        output[i] = len(stack)
    return output


def main():
    data = get_data("../data/Day21.txt")
    board = np.array([[parse_to_int(entry) for entry in line] for line in data], dtype=np.uint32)
    board = np.tile(board, (5, 5))
    board[np.argwhere(board > 1)] = 1
    oboard = board.copy()
    board[board.shape[0] // 2, board.shape[1] // 2] = 2

    if native:
        bptr = ffi.cast("uint32_t *", ffi.from_buffer(board))
        optr = ffi.cast("uint32_t *", ffi.from_buffer(oboard))
        results = np.zeros(65 + 131 * 2, dtype=np.uint32)
        rptr = ffi.cast("uint32_t *", ffi.from_buffer(results))
        lib.day21_step(bptr, optr, board.shape[0], board.shape[1], 65 + 131 * 2, rptr)
    else:
        results = step(board, oboard, 65 + 131 * 2)

    print("Task 01:", int(np.round(results[63])))
    targets = [65 - 1, 65 + 131 - 1, 65 - 1 + 131 * 2]
    poly_coefficients = np.polyfit(*zip(*[(i, element) for i, element in enumerate(results[targets])]), 2)
    print("Task 02:", int(np.round(np.polyval(poly_coefficients, 26501365 // 131))))


if __name__ == "__main__":
    main()
