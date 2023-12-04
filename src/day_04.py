import re
from util import get_data


def get_intersection(data: list[str]):
    split = [[part[0], part[1]] for line in data
             for entry in [line.split(":")]
             for part in [entry[1].split("|")]]
    intersection = [0] * len(split)
    for idx, entry in enumerate(split):
        win = {int(entry) for entry in re.sub(" +", " ", entry[0].strip()).split(" ")}
        mine = {int(entry) for entry in re.sub(" +", " ", entry[1].strip()).split(" ")}
        intersection[idx] = len(win.intersection(mine))
    return intersection


def task_01(intersection: list[int]):
    points = 0
    for entry in intersection:
        if entry >= 1:
            points += 2 ** (entry - 1)
    return points


def task_02(intersection: list[int]):
    copies = [1] * len(intersection)
    for idx, value in enumerate(copies):
        if value == 0:
            break
        for offset in range(1, intersection[idx] + 1):
            copies[idx + offset] += 1 * value
    return sum(copies)


if __name__ == "__main__":
    data = get_data("../data/Day04.txt")
    intersection = get_intersection(data)

    print("Task 01: ", task_01(intersection))
    print("Task 02: ", task_02(intersection))
