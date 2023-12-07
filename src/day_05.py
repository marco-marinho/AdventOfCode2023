import itertools
import re
from dataclasses import dataclass
from typing import Self

from util import get_data


class Slice:

    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def offset(self, offset) -> Self:
        return Slice(self.start + offset, self.end + offset)

    def get_intersection(self, other: Self):
        start = max(self.start, other.start)
        end = min(self.end, other.end)

        if start > end:
            return [], [other]
        elif other.start > self.start and other.end < self.end:
            return [Slice(other.start, other.end - 1)], [Slice(self.start, other.start - 1),
                                                         Slice(other.end + 1, self.end)]
        elif other.start <= self.start <= other.end:
            return [Slice(self.start, other.end)], [Slice(other.start, self.start - 1)]
        elif other.start <= self.end <= other.end:
            return [Slice(other.start, self.end)], [Slice(self.end + 1, other.end)]
        else:
            raise ValueError("Invalid slice")

    def __repr__(self):
        return f"Slice({self.start}, {self.end})"


@dataclass(slots=True)
class Range:
    dest: int
    source: int
    size: int

    def check_next(self, value: int):
        diff = value - self.source
        if value >= self.source and diff < self.size:
            return self.dest + diff
        return -1


def parse_chunk(ilist):
    return list(itertools.batched([int(num) for entry in ilist[1:] for num in entry.split()], 3))


def parse_data():
    data = get_data("../data/Day05.txt")
    seeds = [int(piece) for piece in re.sub(r"[a-z]|:", "", data[0]).strip().split(" ")]
    chunks = [list(group) for k, group in
              itertools.groupby(data[1:], lambda x: x == "") if not k]
    parsed = [parse_chunk(chunk) for chunk in chunks]
    maps = [[] for _ in range(7)]
    for idx, part in enumerate(parsed):
        for entry in part:
            maps[idx].append(Range(*entry))
    return seeds, maps


def task_01():
    seeds, maps = parse_data()
    locations = []
    for seed in seeds:
        curr = seed
        for idx in range(7):
            for entry in maps[idx]:
                nxt = entry.check_next(curr)
                if nxt != -1:
                    curr = nxt
                    break
        locations.append(curr)
    return min(locations)


def main():
    print("Task 01: ", task_01())

    alpha = Slice(10, 100)
    beta = Slice(120, 130)
    a, b = alpha.get_intersection(beta)
    print(a, b)


if __name__ == "__main__":
    main()
