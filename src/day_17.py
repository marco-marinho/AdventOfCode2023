from heapq import heappush, heappop
import multiprocessing as mp

import numpy as np

from util import get_data


def are_inverse(a, b):
    return (
        (a == b"r" and b == b"l") or (a == b"l" and b == b"r") or (a == b"u" and b == b"d") or (a == b"d" and b == b"u")
    )


def dijkstras(board: np.array, min: int, max: int):
    queue = []
    heappush(queue, (board[0, 1], ((0, 1), b"r", 1)))
    heappush(queue, (board[1, 0], ((1, 0), b"d", 1)))
    movements = [((-1, 0), b"d"), ((0, 1), b"r"), ((1, 0), b"u"), ((0, -1), b"l")]
    visited = set()
    while len(queue) > 0:
        cost, state = heappop(queue)
        if state in visited:
            continue
        visited.add(state)
        if state[0][0] == board.shape[0] - 1 and state[0][1] == board.shape[1] - 1 and state[2] >= min:
            return cost
        for movement in movements:
            next_pos = (state[0][0] + movement[0][0], state[0][1] + movement[0][1])
            count = 1 if state[1] != movement[1] else state[2] + 1
            if (
                (state[2] < min and state[1] != movement[1])
                or are_inverse(state[1], movement[1])
                or count > max
                or next_pos[0] < 0
                or next_pos[0] >= board.shape[0]
                or next_pos[1] < 0
                or next_pos[1] >= board.shape[1]
            ):
                continue
            heappush(queue, (cost + board[next_pos[0], next_pos[1]], ((next_pos[0], next_pos[1]), movement[1], count)))
    return -1


if __name__ == "__main__":
    data = get_data("../data/Day17.txt")
    board = np.array([list(line) for line in data], dtype=int)
    with mp.Pool(mp.cpu_count()) as p:
        result = p.starmap(dijkstras, [(board, 1, 3), (board, 4, 10)])
    print("Task 01:", result[0])
    print("Task 02:", result[1])
