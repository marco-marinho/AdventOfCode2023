import re

from util import get_data


str_num_mapping = {
    '1': 1, 'one': 1,
    '2': 2, 'two': 2,
    '3': 3, 'three': 3,
    '4': 4, 'four': 4,
    '5': 5, 'five': 5,
    '6': 6, 'six': 6,
    '7': 7, 'seven': 7,
    '8': 8, 'eight': 8,
    '9': 9, 'nine': 9,
}


def task1(data: list[str]) -> int:
    filtered = [re.sub(r"\D", "", entry) for entry in data]
    numbers = [int(entry[0]) * 10 + int(entry[-1]) for entry in filtered]
    return sum(numbers)


def task2(data: list[str]) -> int:
    pattern = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
    tokens = [re.findall(pattern, entry) for entry in data]
    numbers = [str_num_mapping[entry[0]] * 10 + str_num_mapping[entry[-1]] for entry in tokens]
    return sum(numbers)


def main():
    data = get_data("../data/Day01.txt")
    print("Task 01:", task1(data))
    print("Task 02:", task2(data))


if __name__ == "__main__":
    main()
