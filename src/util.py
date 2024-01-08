from typing import Any, Self, Iterable
from dataclasses import dataclass

import numpy as np
from numpy import ndarray, dtype


def get_data(ipath: str) -> list[str]:
    with open(ipath, encoding="utf8") as ifile:
        return [entry.strip() for entry in ifile.readlines()]


def get_board(ipath: str) -> ndarray[Any, dtype[str]]:
    with open(ipath, encoding="utf8") as ifile:
        data = [entry.strip() for entry in ifile.readlines()]
        rows = len(data[0]) + 2
        cols = len(data) + 2
        oboard = np.full((rows, cols), ".", dtype="|S1")
        oboard[1:-1, 1:-1] = np.array([list(row) for row in data])
        return oboard


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def reversed(self) -> Self:
        return Point(-self.x, -self.y)

    @classmethod
    def from_iterable(cls, iterable: Iterable[int]) -> Self:
        return cls(*iterable)
