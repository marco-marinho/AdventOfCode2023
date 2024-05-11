import re

from util import get_data


def str_to_num(istr: str) -> int:
    match istr:
        case "1" | "one":
            return 1
        case "2" | "two":
            return 2
        case "3" | "three":
            return 3
        case "4" | "four":
            return 4
        case "5" | "five":
            return 5
        case "6" | "six":
            return 6
        case "7" | "seven":
            return 7
        case "8" | "eight":
            return 8
        case "9" | "nine":
            return 9
        case _:
            raise ValueError("Invalid Input")


def task1(data: list[str]) -> int:
    filtered = [re.sub(r"\D", "", entry) for entry in data]
    numbers = [int(entry[0]) * 10 + int(entry[-1]) for entry in filtered]
    return sum(numbers)


def task2(data: list[str]) -> int:
    pattern = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
    tokens = [re.findall(pattern, entry) for entry in data]
    numbers = [str_to_num(entry[0]) * 10 + str_to_num(entry[-1]) for entry in tokens]
    return sum(numbers)


def main():
    data = get_data("../data/Day01.txt")
    print("Task 01:", task1(data))
    print("Task 02:", task2(data))


if __name__ == "__main__":
    main()
