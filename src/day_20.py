from collections import deque, defaultdict

import numpy as np

from util import get_data


class Output:

    def receive(self, *_) -> None:
        return None

    def state(self):
        return tuple()


class FlipFlop:

    def __init__(self):
        self._state = False

    def receive(self, _: str, pulse: bool) -> bool | None:
        if pulse == 1:
            return None
        self._state = not self._state
        return self._state

    def state(self):
        return self._state,


class Conjunction:

    def __init__(self, connections: list[str]):
        self.connections = {connection: False for connection in connections}

    def receive(self, emitter: str, pulse: bool) -> bool:
        self.connections[emitter] = pulse
        return not all(self.connections.values())

    def state(self):
        return (value for value in self.connections.values())


def parse(istr: str):
    name, targets = istr.split(" -> ")
    match name[0]:
        case "%":
            return name[1:], (FlipFlop(), targets.split(", "))
        case "&":
            return name[1:], (Conjunction([]), targets.split(", "))
        case _:
            return name[:], (None, targets.split(", "))


def get_nodes():
    data = get_data("../data/Day20.txt")
    nodes = defaultdict(lambda: (Output(), []))
    nodes.update({node: target for line in data for node, target in [parse(line)]})
    nodes["output"] = (Output(), [])
    conjunctions = [name for name, node in nodes.items() if isinstance(node[0], Conjunction)]
    for name, (_, targets) in nodes.items():
        for target in targets:
            if target in conjunctions:
                nodes[target][0].connections[name] = False
    start_nodes = nodes["broadcaster"][1]
    del nodes["broadcaster"]
    return nodes, start_nodes


def simulate(starting: list[str], limit: int, nodes: dict):
    counts = []
    seen = set()
    for _ in range(limit):
        count = [1, 0]
        signals = deque([("broadcaster", target, False) for target in starting])
        while len(signals) > 0:
            transmitter, target, signal = signals.popleft()
            count[signal] += 1
            n_signal = nodes[target][0].receive(transmitter, signal)
            if n_signal is None:
                continue
            for n_target in nodes[target][1]:
                signals.append((target, n_target, n_signal))
        state = tuple(state for node in nodes.values() for state in node[0].state())
        if state in seen:
            return counts, len(seen)
        seen.add(state)
        counts.append(count.copy())
        count.clear()
    return counts, None


def task_01():
    nodes, start_nodes = get_nodes()
    counts, _ = simulate(start_nodes, 1000, nodes)
    low, high = zip(*counts)
    return sum(low) * sum(high)


def task_02():
    nodes, start_nodes = get_nodes()
    cycles = [cycles for name in start_nodes for _, cycles in [simulate([name], 10000, nodes)]]
    return np.lcm.reduce(cycles, dtype=np.uint64)


def main():
    print("Task 1:", task_01())
    print("Task 2:", task_02())


if __name__ == "__main__":
    main()
