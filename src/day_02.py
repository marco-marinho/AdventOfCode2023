from dataclasses import dataclass

from util import get_data


@dataclass(slots=True)
class GameEntry:
    id: int
    cubes: list[dict[str, int]]

    def is_valid(self, limits: dict[str, int]) -> bool:
        for pull in self.cubes:
            for color, limit in limits.items():
                if color in pull and pull[color] > limit:
                    return False
        return True

    def get_power(self):
        min_possible = {"red": 0, "blue": 0, "green": 0}
        for pull in self.cubes:
            for color, val in pull.items():
                if min_possible[color] < val:
                    min_possible[color] = val
        output = 1
        for value in min_possible.values():
            output *= value
        return output


def parse_line(istr: str):
    parts = istr.split(":")
    game_id = int(parts[0].replace("Game ", ""))
    entries = [part for entry in parts[1].split(";") for part in [entry.strip().split(", ")]]
    olist = []
    for entry in entries:
        olist.append({part[1]: int(part[0]) for val in entry for part in [val.split(" ")]})
    return GameEntry(game_id, olist)


def task_01(lines: list[str]):
    limits = {"red": 12, "blue": 14, "green": 13}
    parsed = [parse_line(line) for line in lines]
    output = 0
    for game in parsed:
        if game.is_valid(limits):
            output += game.id
    return output


def task_02(lines: list[str]):
    parsed = [parse_line(line) for line in lines]
    output = 0
    for game in parsed:
        output += game.get_power()
    return output


def main():
    lines = get_data("../data/Day02.txt")
    print("Task 01: ", task_01(lines))
    print("Task 02: ", task_02(lines))


if __name__ == "__main__":
    main()
