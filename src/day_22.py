import bisect
from dataclasses import dataclass

import numpy as np

from util import get_data


@dataclass
class Piece:
    start: np.array
    end: np.array


def parse_piece(istr: str) -> Piece:
    a, b = [list(map(int, entry.split(","))) for entry in istr.split("~")]
    start = np.zeros(3)
    end = np.zeros(3)
    for i in range(3):
        start[i] = min(a[i], b[i])
        end[i] = max(a[i], b[i])
    return Piece(start, end)


data = [parse_piece(entry) for entry in get_data("../data/Day22.txt")]
# data = sorted(data, key=lambda x: x.end[2])

settled = sorted([entry for entry in data if entry.start[2] == 1], key=lambda x: -x.end[2])
pending = sorted([entry for entry in data if entry.start[2] != 1], key=lambda x: -x.start[2])

while len(pending) > 0:
    curr = pending.pop()
    z_len = curr.end[2] - curr.start[2]
    for other in settled:
        if (max(curr.start[0], other.start[0]) <= min(curr.end[0], other.end[0])
                and max(curr.start[1], other.start[1]) <= min(curr.end[1], other.end[1])):
            curr.start[2] = other.end[2] + 1
            curr.end[2] = curr.start[2] + z_len
            break
    else:
        curr.start[2] = 1
        curr.end[2] = 1 + z_len
    bisect.insort(settled, curr, key=lambda x: -x.end[2])
    print(settled)

print(settled)
print(pending)
