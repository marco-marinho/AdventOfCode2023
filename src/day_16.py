import multiprocessing as mp

import numpy as np

from util import get_board, Point


def run_once(pos: Point, mov: Point, board: np.ndarray) -> int:
    beams = [(pos, mov)]
    visited = set()
    unique = np.zeros(board.shape)

    while len(beams) > 0:
        pos, mov = beams.pop()
        key = (pos.x, pos.y, mov.x, mov.y)
        if key in visited or pos.x < 0 or pos.x >= board.shape[0] or pos.y < 0 or pos.y >= board.shape[1]:
            continue
        visited.add(key)
        unique[pos.x, pos.y] = 1
        square = board[pos.x, pos.y]
        match square, mov:
            case b"\\", _:
                nmov = Point(mov.y, mov.x)
                beams.append((pos + nmov, nmov))
            case b"/", _:
                nmov = Point(-mov.y, -mov.x)
                beams.append((pos + nmov, nmov))
            case b"-", Point(1, 0) | Point(-1, 0):
                beams.append((pos + Point(0, -1), Point(0, -1)))
                beams.append((pos + Point(0, 1), Point(0, 1)))
            case b"|", Point(0, 1) | Point(0, -1):
                beams.append((pos + Point(-1, 0), Point(-1, 0)))
                beams.append((pos + Point(1, 0), Point(1, 0)))
            case _:
                beams.append((pos + mov, mov))
    return np.count_nonzero(unique)


if __name__ == "__main__":
    board = get_board("../data/Day16.txt")
    board = board[1:-1, 1:-1]
    print("Task 01:", run_once(Point(0, 0), Point(0, 1), board))
    with mp.Pool(mp.cpu_count()) as p:
        left = p.starmap(run_once, [(Point(x, 0), Point(0, 1), board) for x in range(board.shape[0])])
        right = p.starmap(
            run_once,
            [(Point(x, board.shape[1] - 1), Point(0, -1), board) for x in range(board.shape[0])],
        )
        top = p.starmap(run_once, [(Point(0, y), Point(1, 0), board) for y in range(board.shape[1])])
        bottom = p.starmap(
            run_once,
            [(Point(board.shape[0] - 1, y), Point(-1, 0), board) for y in range(board.shape[1])],
        )
    print("Task 02:", max(left + right + top + bottom))
