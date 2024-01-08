from copy import copy

from util import get_data, Point

links = {"|": {Point(-1, 0), Point(1, 0)},
         "-": {Point(0, -1), Point(0, 1)},
         "L": {Point(-1, 0), Point(0, 1)},
         "7": {Point(0, -1), Point(1, 0)},
         "J": {Point(-1, 0), Point(0, -1)},
         "F": {Point(1, 0), Point(0, 1)},
         "S": {Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)}}


def det(p1: Point, p2: Point) -> int:
    return p1.x * p2.y - p1.y * p2.x


def find_start(idata: list[str]):
    line = next(i for i, v in enumerate(idata) if "S" in v)
    col = idata[line].index("S")
    return line, col


def step(idata: list[str], pos: Point, direction: Point):
    next_pos = pos + direction
    next_tile = idata[next_pos.x][next_pos.y]
    if pos not in [next_pos + change for change in links[next_tile]]:
        return None, None
    if next_tile in ["J", "F", "7", "L"]:
        next_direction = list(links[next_tile] - {direction.reversed()})[0]
    else:
        next_direction = direction
    return next_pos, next_direction


def get_loop(idata: list[str], start_pos: Point, start_direction: Point):
    pos = copy(start_pos)
    direction = copy(start_direction)
    visited = set()
    edges = []
    while pos is not None and pos not in visited:
        visited.add(pos)
        if idata[pos.x][pos.y] in ["S", "J", "F", "7", "L"]:
            edges.append(pos)
        pos, direction = step(idata, pos, direction)
    if pos is None or pos != start_pos:
        return set(), edges
    return visited, edges


if __name__ == "__main__":
    data = get_data("../data/Day10.txt")
    start_pos = Point.from_iterable(find_start(data))
    directions = [Point(0, 1), Point(0, -1), Point(-1, 0), Point(1, 0)]
    for direction in directions:
        coords, edges = get_loop(data, start_pos, direction)
        if len(coords) > 0:
            b = len(coords) // 2
            print("Task 01:", b)
            edges.append(edges[0])
            A2 = 0
            for i in range(len(edges) - 1):
                A2 += det(edges[i], edges[i + 1])
            i = abs(A2)//2 - b + 1
            print("Task 02:", i)
            break

