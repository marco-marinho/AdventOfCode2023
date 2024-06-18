import bisect
from dataclasses import dataclass, field
from itertools import count
from typing import ClassVar, Generator

import numpy as np

from util import get_data


@dataclass
class Piece:
    counter: ClassVar[Generator[int, None, None]] = count()
    start: np.array
    end: np.array
    supporting: list = field(default_factory=list, repr=False)
    supported_by: list = field(default_factory=list, repr=False)
    hash_id: int = field(default_factory=lambda: next(Piece.counter))

    def __hash__(self):
        return self.hash_id


def parse_piece(istr: str) -> Piece:
    a, b = [list(map(int, entry.split(","))) for entry in istr.split("~")]
    start = np.zeros(3)
    end = np.zeros(3)
    for i in range(3):
        start[i] = min(a[i], b[i])
        end[i] = max(a[i], b[i])
    return Piece(start, end)


def intersect(first: Piece, second: Piece) -> bool:
    return (max(first.start[0], second.start[0]) <= min(first.end[0], second.end[0])
            and max(first.start[1], second.start[1]) <= min(first.end[1], second.end[1]))


def drop(data: list[Piece]) -> list[Piece]:
    settled = sorted([entry for entry in data if entry.start[2] == 1], key=lambda x: -x.end[2])
    pending = sorted([entry for entry in data if entry.start[2] != 1], key=lambda x: -x.start[2])
    while len(pending) > 0:
        curr = pending.pop()
        z_len = curr.end[2] - curr.start[2]
        for other in settled:
            if intersect(curr, other):
                curr.start[2] = other.end[2] + 1
                curr.end[2] = curr.start[2] + z_len
                break
        else:
            curr.start[2] = 1
            curr.end[2] = 1 + z_len
        bisect.insort(settled, curr, key=lambda x: -x.end[2])
    return settled


def connect_bricks(data: list[Piece]):
    for idx, brick in enumerate(data):
        for other in data[idx + 1:]:
            if intersect(brick, other) and brick.start[2] - 1 == other.end[2]:
                brick.supported_by.append(other)
                other.supporting.append(brick)
            elif other.end[2] < brick.start[2] - 1:
                break


def critical_bricks(data: list[Piece]) -> list[Piece]:
    non_removable = []
    for brick in data:
        for other in brick.supporting:
            if len(other.supported_by) < 2:
                non_removable.append(brick)
                break
    return non_removable


def chain_length(target: Piece) -> int:
    removed = {target.hash_id}
    queue = [target]
    visited = set()
    while queue:
        current = queue.pop()
        if current in visited:
            continue
        visited.add(current)
        for other in current.supporting:
            bisect.insort(queue, other, key=lambda x: -x.end[2])
        if all([other.hash_id in removed for other in current.supported_by]):
            removed.add(current.hash_id)
    return len(removed) - 1


if __name__ == "__main__":
    data = [parse_piece(entry) for entry in get_data("../data/Day22.txt")]
    settled = drop(data)
    connect_bricks(settled)
    non_removable = critical_bricks(settled)
    print("Task 01:", len(settled) - len(non_removable))
    chain = map(chain_length, settled)
    print("Task 02:", sum(chain))
