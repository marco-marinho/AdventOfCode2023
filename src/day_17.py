from heapq import heappush, heappop

import numpy as np

try:
    from native.day17_pybind import native_djikstras

    native = True
except ImportError:
    import multiprocessing as mp

    native = False

from util import get_data


def dijkstras(iboard: np.array, imin: int, imax: int):
    queue = []
    inverses = (3, 2, 1, 0)
    heappush(queue, (iboard[0, 1], ((0, 1), 0, 1)))
    heappush(queue, (iboard[1, 0], ((1, 0), 1, 1)))
    movements = (((-1, 0), 2), ((0, 1), 0), ((1, 0), 1), ((0, -1), 3))
    visited = np.full((iboard.shape[0], iboard.shape[1], 4, imax + 1), False)
    while len(queue) > 0:
        cost, state = heappop(queue)
        if visited[state[0][0], state[0][1], state[1], state[2]]:
            continue
        visited[state[0][0], state[0][1], state[1], state[2]] = True
        if state[0][0] == iboard.shape[0] - 1 and state[0][1] == iboard.shape[1] - 1 and state[2] >= imin:
            return cost
        for movement in movements:
            next_pos = (state[0][0] + movement[0][0], state[0][1] + movement[0][1])
            count = 1 if state[1] != movement[1] else state[2] + 1
            if (
                    (state[2] < imin and state[1] != movement[1])
                    or inverses[state[1]] == movement[1]
                    or count > imax
                    or next_pos[0] < 0
                    or next_pos[0] >= iboard.shape[0]
                    or next_pos[1] < 0
                    or next_pos[1] >= iboard.shape[1]
                    or visited[next_pos[0], next_pos[1], movement[1], count]
            ):
                continue
            heappush(queue, (cost + iboard[next_pos[0], next_pos[1]], ((next_pos[0], next_pos[1]), movement[1], count)))
    return -1


def main():
    data = get_data("../data/Day17.txt")
    board = np.array([list(line) for line in data], dtype=np.uint64)
    if native:
        print("Task 01:", native_djikstras(board, 1, 3))
        print("Task 02:", native_djikstras(board, 4, 10))
    else:
        with mp.Pool(2) as p:
            result = p.starmap(dijkstras, [(board, 1, 3), (board, 4, 10)])
        print("Task 01:", result[0])
        print("Task 02:", result[1])


if __name__ == "__main__":
    main()
