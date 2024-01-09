from itertools import groupby

import numpy as np
from numpy.typing import NDArray

from util import get_data


def find_reflection(block: NDArray[int], max_residual: int = 0) -> int:
    for i in range(1, block.shape[0]):
        flipped = np.flip(block[:i], axis=0)
        original = block[i:]
        size = min(flipped.shape[0], original.shape[0])
        residual = np.sum(np.abs(flipped[:size] - original[:size]))
        if residual == max_residual:
            return i
    return -1


def get_points(block: NDArray[int], max_residual: int = 0) -> int:
    res = find_reflection(block, max_residual)
    if res != -1:
        return 100 * res
    return find_reflection(block.T, max_residual)


if __name__ == "__main__":
    data = get_data("../data/Day13.txt")
    blocks = [np.array(list(list(b.replace(".", "0").replace("#", "1")) for b in block), dtype=np.int8)
              for k, block in groupby(data, lambda x: x == "") if not k]
    points_1 = sum(get_points(block, 0) for block in blocks)
    points_2 = sum(get_points(block, 1) for block in blocks)
    print("Task 1:", points_1)
    print("Task 2:", points_2)
