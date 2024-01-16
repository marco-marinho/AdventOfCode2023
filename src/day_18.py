from itertools import accumulate, pairwise

from util import get_data

STEP_MAP = {"0": "R", "1": "D", "2": "L", "3": "U"}
DIR_MAP = {"R": (0, 1), "L": (0, -1), "U": (-1, 0), "D": (1, 0)}


def det(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return p1[0] * p2[1] - p1[1] * p2[0]


def parse(line: str) -> tuple[tuple[tuple[int, int], int], tuple[tuple[int, int], int]]:
    direction, steps, hexv = line.split(" ")
    long_steps = int(hexv[2:-2], 16)
    return (DIR_MAP[direction], int(steps)), (DIR_MAP[STEP_MAP[hexv[-2]]], long_steps)


def walk(pos: tuple[int, int], step: tuple[tuple[int, int], int]) -> tuple[int, int]:
    return pos[0] + step[0][0] * step[1], pos[1] + step[0][1] * step[1]


def calculate(steps: list[tuple[str, int]]) -> int:
    corners = accumulate(steps, lambda acc, x: walk(acc, x), initial=(0, 0))
    A = abs(sum(det(*pair) for pair in pairwise(corners))) // 2
    b = sum(step for _, step in steps)
    i = A - b // 2 + 1
    return i + b


if __name__ == "__main__":
    data = get_data("../data/Day18.txt")
    short, long = list(zip(*[parse(line) for line in data]))
    print("Task 01:", calculate(short))
    print("Task 02:", calculate(long))
