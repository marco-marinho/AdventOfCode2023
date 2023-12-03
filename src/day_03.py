import re
from dataclasses import dataclass

import numpy as np

from util import get_board, get_data


@dataclass(slots=True)
class Number:
    value: int
    row: int
    col: int
    size: int

    def check_valid(self, symbols: list[(int, int)]) -> bool:
        for symbol in symbols:
            s_row, s_col = symbol
            if (self.row - 1 <= s_row <= self.row + 1) and (self.col - 1 <= s_col <= self.col + self.size):
                return True
        return False


def find_numbers(data: list[str]) -> list[Number]:
    pattern = re.compile(r"\d+")
    output = []
    for row, line in enumerate(data):
        for match in re.finditer(pattern, line):
            number = Number(int(match.group()), row + 1, match.start() + 1, len(match.group()))
            output.append(number)
    return output


def find_symbols(board: np.ndarray[str]) -> list[(int, int)]:
    rows, cols = board.shape
    output = []
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if not (b"0" <= board[row, col] <= b"9" or board[row, col] == b"."):
                output.append((row, col))
    return output


def find_gears(board: np.ndarray[str]) -> list[(int, int)]:
    rows, cols = board.shape
    output = []
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if board[row, col] == b"*":
                output.append((row, col))
    return output


def task_01(numbers: list[Number], symbols: list[(int, int)]):
    acc = 0
    for number in numbers:
        if number.check_valid(symbols):
            acc += number.value
    return acc


def task_02(numbers: list[Number], gears: list[(int, int)]):
    acc = 0
    for gear in gears:
        vals = []
        for number in numbers:
            if number.check_valid([gear]):
                vals.append(number.value)
        if len(vals) == 2:
            acc += vals[0] * vals[1]
    return acc


if __name__ == "__main__":
    board = get_board("../data/Day03.txt")
    data = get_data("../data/Day03.txt")

    symbols = find_symbols(board)
    numbers = find_numbers(data)
    gears = find_gears(board)

    print("Task 01: ", task_01(numbers, symbols))
    print("Task 02: ", task_02(numbers, symbols))
