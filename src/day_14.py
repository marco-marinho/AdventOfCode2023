import numpy as np
from numba import njit

from util import get_board


@njit(cache=True)
def move(data):
    for i in range(data.shape[1]):
        buff = data[:, i]
        p = n = 0
        for j in range(data.shape[0]):
            if buff[j] == b"O":
                n += 1
            elif buff[j] == b"#":
                buff[p: p + n] = b"O"
                buff[p + n: j] = b"."
                p = j + 1
                n = 0
        if n > 0:
            buff[p: p + n] = b"O"
            buff[p + n:] = b"."


def calc_load(data):
    return sum(np.count_nonzero(row == b"O") * (data.shape[0] - i) for i, row in enumerate(data))


def cycle(data):
    move(data)
    move(data.T)
    move(data[::-1, :])
    move(data.T[::-1, :])


def task_01(data):
    cdata = data.copy()
    move(cdata)
    return calc_load(cdata)


def task_02(data):
    cdata = data.copy()
    seen = {}
    target = 1000000000
    repeat_len = 0
    i = 0

    while i < target:
        cycle(cdata)
        i += 1
        if repeat_len == 0 and cdata.data.tobytes() in seen:
            repeat_len = i - seen[cdata.data.tobytes()]
            i += repeat_len * ((target - i) // repeat_len)
        elif repeat_len == 0:
            seen[cdata.data.tobytes()] = i
    return calc_load(cdata)


def main():
    data = get_board("../data/Day14.txt")
    data = data[1:-1, 1:-1]
    print("Task 1:", task_01(data))
    print("Task 2:", task_02(data))


if __name__ == "__main__":
    main()
