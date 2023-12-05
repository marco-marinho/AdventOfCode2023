import re
import itertools
from dataclasses import dataclass
from util import get_data


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
            # noinspection PyTypeChecker
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


if __name__ == "__main__":
    main()
