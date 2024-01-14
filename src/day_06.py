import re
from functools import reduce

import numpy as np

from util import get_data


def parse_01() -> list[list[[int]]]:
    data = get_data("../data/Day06.txt")
    parsed = [list(map(int, entry)) for line in data for entry in [re.sub(" +", " ", line).split(" ")[1:]]]
    return parsed


def parse_02() -> list[int]:
    data = get_data("../data/Day06.txt")
    parsed = [reduce(lambda a, b: a + b, re.sub(" +", " ", line).split(" ")[1:]) for line in data]
    return list(map(int, parsed))


def solve(b: int, c: int) -> tuple[float, float]:
    delta = np.sqrt(b**2 - 4 * c)
    return (b - delta) / 2, (b + delta) / 2


def snap(data: tuple[float, float]) -> tuple[int, int]:
    first = data[0] + 1 if np.mod(data[0], 1) == 0 else np.ceil(data[0])
    second = data[1] - 1 if np.mod(data[1], 1) == 0 else np.floor(data[1])
    return first, second


def task_01() -> int:
    times, distances = parse_01()
    acc = 1
    for time, distance in zip(times, distances):
        f, s = snap(solve(time, distance))
        acc *= s - f + 1
    return int(acc)


def task_02() -> int:
    time, distance = parse_02()
    f, s = snap(solve(time, distance))
    return int(s - f + 1)


if __name__ == "__main__":
    print("Task 01:", task_01())
    print("Task 02:", task_02())
