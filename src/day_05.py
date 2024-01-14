import itertools
import re
from dataclasses import dataclass
from typing import Self

from util import get_data


class Slice:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def valid(self) -> bool:
        return self.start <= self.end

    def offset(self, offset) -> Self:
        return Slice(self.start + offset, self.end + offset)

    def get_intersection(self, other: Self) -> tuple[list[Self], list[Self]]:
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        res = [Slice(start, end)]
        rest = [
            Slice(other.start, min(self.start - 1, other.end)),
            Slice(max(self.end + 1, other.start), other.end),
        ]
        return (
            [entry for entry in res if entry.valid()],
            [entry for entry in rest if entry.valid()],
        )

    def __repr__(self) -> str:
        return f"Slice({self.start}, {self.end})"


@dataclass(slots=True)
class Range:
    dest: int
    source: int
    size: int

    def check_next(self, value: int) -> int:
        diff = value - self.source
        if value >= self.source and diff < self.size:
            return self.dest + diff
        return -1

    def get_intersection(self, other: Slice) -> tuple[list[Self], list[Self]]:
        result, reminder = Slice(self.source, self.source + self.size - 1).get_intersection(other)
        result = [entry.offset(self.dest - self.source) for entry in result]
        return result, reminder


def parse_chunk(ilist):
    return list(itertools.batched([int(num) for entry in ilist[1:] for num in entry.split()], 3))


def parse_data():
    data = get_data("../data/Day05.txt")
    seeds = [int(piece) for piece in re.sub(r"[a-z]|:", "", data[0]).strip().split(" ")]
    chunks = [list(group) for k, group in itertools.groupby(data[1:], lambda x: x == "") if not k]
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
        for idx, element in enumerate(maps):
            for entry in element:
                nxt = entry.check_next(curr)
                if nxt != -1:
                    curr = nxt
                    break
        locations.append(curr)
    return min(locations)


def task_02():
    seeds, maps = parse_data()
    seeds_ranges = itertools.batched(seeds, 2)
    unprocessed = [Slice(pair[0], pair[0] + pair[1] - 1) for pair in seeds_ranges]
    processed = []
    for idx, element in enumerate(maps):
        while len(unprocessed) > 0:
            current = unprocessed.pop()
            for entry in element:
                pros, unpr = entry.get_intersection(current)
                if len(pros) > 0:
                    processed += pros
                    unprocessed += unpr
                    break
            else:
                processed.append(current)
        unprocessed = processed
        processed = []
    return min([entry.start for entry in unprocessed])


def main():
    print("Task 01: ", task_01())
    print("Task 02: ", task_02())


if __name__ == "__main__":
    main()
