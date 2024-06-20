from itertools import count
from typing import Generator

import numpy as np

from util import get_board


def walk(position, previous, board, nodes):
    steps = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
    count = 0
    while tuple(*position) not in nodes.keys():
        possibilities = steps + position
        for possibility in possibilities:
            if (possibility != previous).any() and board[possibility[0], possibility[1]] != b"#":
                previous = position
                position = np.atleast_2d(possibility)
                count += 1
                break
    return tuple(*position), count + 1


class Node:
    counter: Generator[int, None, None] = count()

    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.neighbors: dict[str, tuple[Node, int]] = {}
        self.id = next(Node.counter)

    def connect(self, board, node_dict):
        arr_pos = np.array([self.position])
        if board[self.position[0] - 1, self.position[1]] != b"#":
            neighbor, distance = walk(arr_pos + [-1, 0], arr_pos, board, node_dict)
            self.neighbors["up"] = (node_dict[neighbor], distance)
        if board[self.position[0] + 1, self.position[1]] != b"#":
            neighbor, distance = walk(arr_pos + [1, 0], arr_pos, board, node_dict)
            self.neighbors["down"] = (node_dict[neighbor], distance)
        if board[self.position[0], self.position[1] - 1] != b"#":
            neighbor, distance = walk(arr_pos + [0, -1], arr_pos, board, node_dict)
            self.neighbors["left"] = (node_dict[neighbor], distance)
        if board[self.position[0], self.position[1] + 1] != b"#":
            neighbor, distance = walk(arr_pos + [0, 1], arr_pos, board, node_dict)
            self.neighbors["right"] = (node_dict[neighbor], distance)

    def trim(self):
        to_remove = []
        for direction, (neighbor, distance) in self.neighbors.items():
            if len(neighbor.neighbors) <= 3 and len(self.neighbors) <= 3 and direction in ["up", "left"]:
                to_remove.append(direction)
        for direction in to_remove:
            del self.neighbors[direction]


def traverse(current: Node, target: Node, visited: list[int], cost: int):
    if current == target:
        yield cost
    for neighbor, distance in current.neighbors.values():
        if visited[neighbor.id]:
            continue
        visited[neighbor.id] = 1
        yield from traverse(neighbor, target, visited, cost + distance)
        visited[neighbor.id] = 0


if __name__ == "__main__":
    board = get_board("../data/Day23.txt", fill="#")
    end = (board.shape[0] - 2, board.shape[1] - 3)
    node_set = {(1, 2): Node((1, 2)), end: Node(end)}
    candidates = np.asarray(np.where(board == b"v")).T
    for candidate in candidates:
        if board[candidate[0] - 1, candidate[1] - 1] == b">" or board[candidate[0] - 1, candidate[1] + 1] == b">":
            node_set[(candidate[0] - 1, candidate[1])] = Node((candidate[0] - 1, candidate[1]))
        else:
            node_set[(candidate[0] + 1, candidate[1])] = Node((candidate[0] + 1, candidate[1]))
    for node in node_set.values():
        node.connect(board, node_set)
    for node in node_set.values():
        node.trim()

    end_node = node_set[end]
    visited = [1, *([0] * 100)]
    t2 = max(traverse(node_set[(1, 2)], end_node, visited, 0))
    for node in node_set.values():
        node.neighbors.pop("up", None)
        node.neighbors.pop("left", None)
    visited = [1, *([0] * 100)]
    t1 = max(traverse(node_set[(1, 2)], end_node, visited, 0))
    print("Task 01:", t1)
    print("Task 02:", t2)
