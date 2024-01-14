import re
from util import get_data


def get_intersection(data: list[str]):
    def _get_intersection(first: str, second: str):
        win = {int(entry) for entry in re.sub(" +", " ", first.strip()).split(" ")}
        mine = {int(entry) for entry in re.sub(" +", " ", second.strip()).split(" ")}
        return len(win.intersection(mine))

    split = [_get_intersection(*part) for line in data for entry in [line.split(":")] for part in [entry[1].split("|")]]
    return split


def task_01(intersection: list[int]):
    points = 0
    for entry in intersection:
        if entry >= 1:
            points += 2 ** (entry - 1)
    return points


def task_02(intersection: list[int]):
    copies = [1] * len(intersection)
    for idx, value in enumerate(copies):
        for offset in range(1, intersection[idx] + 1):
            copies[idx + offset] += 1 * value
    return sum(copies)


def main():
    data = get_data("../data/Day04.txt")
    intersection = get_intersection(data)

    print("Task 01: ", task_01(intersection))
    print("Task 02: ", task_02(intersection))


if __name__ == "__main__":
    main()
