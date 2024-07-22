import numpy as np
from numpy.typing import NDArray
from itertools import combinations

from util import get_data

cross = lambda x, y: np.cross(x, y)


def task_01(data: list[tuple[NDArray[np.float64], NDArray[np.float64]]]):
    count = 0
    minx = miny = 200000000000000
    maxx = maxy = 400000000000000
    for first, second in combinations(data, 2):
        p = first[0][:2]
        r = first[1][:2]
        q = second[0][:2]
        s = second[1][:2]
        a = q - p
        b = cross(r, s)
        if b == 0:
            continue
        t = cross(a, s / b)
        u = cross(a, r / b)
        if t < 0 or u < 0:
            continue
        intersection = p + t * r
        if minx <= intersection[0] <= maxx and miny <= intersection[1] <= maxy:
            count += 1
    return count


def task_02(data: list[tuple[NDArray[np.float64], NDArray[np.float64]]]):
    p = data[1][0] - data[0][0]
    r = data[1][1] - data[0][1]
    q = data[2][0] - data[0][0]
    s = data[2][1] - data[0][1]
    t1 = -(cross(p, q) @ s) / (cross(r, q) @ s)
    t2 = -(cross(p, q) @ r) / (cross(p, s) @ r)
    c1 = data[1][0] + t1 * data[1][1]
    c2 = data[2][0] + t2 * data[2][1]
    v = (c2 - c1) / (t2 - t1)
    ans = c1 - t1 * v
    return int(np.sum(ans))


def main():
    lines = get_data("../data/Day24.txt")
    data = [(np.fromstring(first, sep=",", dtype=np.float64), np.fromstring(second, sep=",", dtype=np.float64))
            for line in lines
            for first, second in [line.split("@")]]
    print("Task 01:", task_01(data))
    print("Task 02:", task_02(data))


if __name__ == "__main__":
    main()
