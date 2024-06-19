from util import get_board
import numpy as np


def walk(position, previous, board, nodes):
    steps = np.array([(1, 0), (-1, 0), (0, 1), (0, -1)])
    count = 0
    while tuple(*position) not in nodes:
        possibilities = steps + position
        for possibility in possibilities:
            if (possibility != previous).any() and board[possibility[0], possibility[1]] != b"#":
                previous = position
                position = np.atleast_2d(possibility)
                count += 1
                break
    return position, count + 1


class Node:

    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.neighbors: list[tuple[Node, int, bool]] = []

    def __hash__(self):
        return hash(self.position)

    def connect(self, board, nodes):
        print(self.position)
        arr_pos = np.array([self.position])
        if board[self.position[0] - 1, self.position[1]] != b"#":
            neighbor, distance = walk(arr_pos + [-1, 0], arr_pos, board, nodes)
            self.neighbors.append((neighbor, distance, False))
        if board[self.position[0] + 1, self.position[1]] != b"#":
            neighbor, distance = walk(arr_pos + [1, 0], arr_pos, board, nodes)
            self.neighbors.append((neighbor, distance, True))
        if board[self.position[0], self.position[1] - 1] != b"#":
            neighbor, distance = walk(arr_pos + [0, -1], arr_pos, board, nodes)
            self.neighbors.append((neighbor, distance, False))
        if board[self.position[0], self.position[1] + 1] != b"#":
            neighbor, distance = walk(arr_pos + [0, 1], arr_pos, board, nodes)
            self.neighbors.append((neighbor, distance, True))


node_set = {(1, 2), (23, 22)}
candidates = np.asarray(np.where(board == b"v")).T
for candidate in candidates:
    if board[candidate[0] - 1, candidate[1] - 1] in [b">", b"<"]:
        node_set.add((candidate[0] - 1, candidate[1]))
    else:
        node_set.add((candidate[0] + 1, candidate[1]))

nodes = [Node(node) for node in node_set]
for node in nodes:
    node.connect(board, node_set)

print(nodes)
