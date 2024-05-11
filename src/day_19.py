from itertools import groupby

from util import get_data

CHART_TO_INT = {"x": 0, "m": 1, "a": 2, "s": 3}


class Node:
    def __init__(self, istr):
        istr = istr[istr.find("{") + 1:]
        pieces = istr.split(",")
        self.final = pieces[-1][:-1]
        self.branches = [
            (CHART_TO_INT[cond[0]], cond[1], int(cond[2:]), dest)
            for part in pieces[:-1]
            for cond, dest in [part.split(":")]
        ]


def travel(tree: dict[str, Node]):
    queue = [("in", (range(1, 4001), range(1, 4001), range(1, 4001), range(1, 4001)))]
    accept = []
    while len(queue) > 0:
        node_name, state = queue.pop()
        if node_name in ["A", "R"]:
            if node_name == "A":
                accept.append(state)
            continue
        node = tree[node_name]
        f_state = list(state)
        for idx, condition, value, dest in node.branches:
            c_state = f_state.copy()
            start = c_state[idx].start
            end = c_state[idx].stop
            if condition == "<":
                c_state[idx] = range(start, value)
                f_state[idx] = range(value, end)
            else:
                c_state[idx] = range(value + 1, end)
                f_state[idx] = range(start, value + 1)
            queue.append((dest, c_state))
        queue.append((node.final, f_state))
    return accept


def calc_possibilities(conditions: tuple[range, range, range, range]):
    acc = 1
    for entry in conditions:
        acc *= entry.stop - entry.start
    return acc


def valid(entry: tuple[int, int, int, int], acceptable: list[tuple[range, range, range, range]]):
    x, m, a, s = entry
    return any([x in xt and m in mt and a in at and s in st for xt, mt, at, st in acceptable])


if __name__ == "__main__":
    data = get_data("../data/Day19.txt")

    tree, entries = [list(entries) for k, entries in groupby(data, key=lambda x: x == "") if not k]
    tree = {entry[: entry.find("{")]: Node(entry) for entry in tree}
    entries = [
        (int(x[3:]), int(m[2:]), int(a[2:]), int(s[2:-1]))
        for entry in entries
        for x, m, a, s in [entry.split(",")]
    ]
    accept = travel(tree)
    rating = sum(sum(entry) for entry in entries if valid(entry, accept))
    possibilities = sum(calc_possibilities(entry) for entry in accept)
    print("Task 01:", rating)
    print("Task 02:", possibilities)
