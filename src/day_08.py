import numpy as np

from util import get_data


def parse():
    data = get_data("../data/Day08.txt")
    commands = [1 if entry == "R" else 0 for entry in data[0]]
    instructions = {line[0:3]: (line[7:10], line[12:15]) for line in data[2:]}
    return commands, instructions


def run(commands, instructions):
    states = [state for state in instructions.keys() if state[-1] == "A"]
    size_comm = len(commands)
    steps = []
    for state in states:
        idx = 0
        while state[-1] != "Z":
            state = instructions[state][commands[idx % size_comm]]
            idx += 1
        steps.append(idx)
    return steps[states.index("AAA")], np.lcm.reduce(steps, dtype=np.uint64)


def main():
    first, second = run(*parse())
    print("Task 01:", first)
    print("Task 02:", second)


if __name__ == "__main__":
    main()
