import bisect
from dataclasses import dataclass, field
from functools import cache
from itertools import count

import numpy as np

from util import get_data

from itertools import count

counter = count()


@dataclass
class Piece:
    start: np.array
    end: np.array
    supporting: list = field(default_factory=list, repr=False)
    supported: list = field(default_factory=list, repr=False)
    hash_id: int = field(default_factory=lambda: next(counter))

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


@cache
def get_touching(brick: Piece) -> set[Piece]:
    touching = set()
    for other in brick.supported:
        touching.add(other)
        touching.update(get_touching(other))
    return touching


def intersect(first: Piece, second: Piece) -> bool:
    return (max(first.start[0], second.start[0]) <= min(first.end[0], second.end[0])
            and max(first.start[1], second.start[1]) <= min(first.end[1], second.end[1]))


data = [parse_piece(entry) for entry in get_data("../data/Day22.txt")]

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

for idx, brick in enumerate(settled):
    for other in settled[idx + 1:]:
        if intersect(brick, other) and brick.start[2] - 1 == other.end[2]:
            brick.supporting.append(other)
            other.supported.append(brick)
        elif other.end[2] < brick.start[2] - 1:
            break

removable = 0
for brick in settled:
    for other in brick.supported:
        if len(other.supporting) < 2:
            break
    else:
        removable += 1

print(removable)

# for brick in settled:
#     touching = get_touching(brick)
#     fallen = 0
#     for touched in touching:
#         if len(set(touched.supported).intersection(touching)) == len(touched.supported):
#             fallen += 1
#     print(fallen)
