from collections import defaultdict
from functools import reduce

from util import get_data


def hash_str(istr: str) -> int:
    return reduce(lambda acc, x: (acc + ord(x)) * 17 % 256, istr, 0)


def task_1(data: list[str]) -> int:
    return sum(hash_str(istr) for istr in data)


def task_2(data: list[str]) -> int:
    boxes = defaultdict(dict)
    for entry in data:
        if entry[-1] == "-":
            boxes[hash_str(entry[:-1])].pop(entry[:-1], None)
        else:
            boxes[hash_str(entry[:-2])][entry[:-2]] = int(entry[-1])
    return sum((key + 1) * (idx + 1) * val for key in boxes for idx, val in enumerate(boxes[key].values()))


if __name__ == "__main__":
    data = get_data("../data/Day15.txt")[0].split(",")
    print("Task 01:", task_1(data))
    print("Task 02:", task_2(data))
