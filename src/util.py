import numpy as np


def get_data(ipath: str) -> list[str]:
    with open(ipath, encoding="utf8") as ifile:
        return [entry.strip() for entry in ifile.readlines()]


def get_board(ipath: str) -> np.ndarray[str]:
    with open(ipath, encoding="utf8") as ifile:
        data = [entry.strip() for entry in ifile.readlines()]
        rows = len(data[0]) + 2
        cols = len(data) + 2
        oboard = np.full((rows, cols), ".", dtype="|S1")
        oboard[1:-1, 1:-1] = np.array([list(row) for row in data])
        return oboard
