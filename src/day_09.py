from functools import reduce

import numpy as np

from util import get_data


def parse():
    data = get_data("../data/Day09.txt")
    return [list(map(int, entry)) for line in data for entry in [line.split(" ")]]


def interpolate(idata: list[int]) -> tuple[int, int]:
    end = len(idata)
    end_vals = []
    start_vals = []
    while idata[:end].count(0) != end:
        end_vals.append(idata[end - 1])
        start_vals.append(idata[0])
        for idx in range(end - 1):
            idata[idx] = idata[idx + 1] - idata[idx]
        end -= 1
    start_vals.append(0)
    return sum(end_vals), reduce(lambda a, b: b - a, start_vals[::-1])


if __name__ == "__main__":
    lines = parse()
    t1, t2 = list(zip(*[interpolate(entry) for entry in lines]))
    print("Task 01:", sum(t1))
    print("Task 02:", sum(t2))
