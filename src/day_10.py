from copy import copy

from util import get_data, Point

links = {"|": {Point(-1, 0), Point(1, 0)},
         "-": {Point(0, -1), Point(0, 1)},
         "L": {Point(-1, 0), Point(0, 1)},
         "7": {Point(0, -1), Point(1, 0)},
         "J": {Point(-1, 0), Point(0, -1)},
         "F": {Point(1, 0), Point(0, 1)},
         "S": {Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)}}


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


def loop_len(idata: list[str], start_pos: Point, start_direction: Point):
    pos = copy(start_pos)
    direction = copy(start_direction)
    visited = set()
    while pos is not None and pos not in visited:
        visited.add(pos)
        pos, direction = step(idata, pos, direction)
    if pos is None or pos != start_pos:
        return -1
    return len(visited)


if __name__ == "__main__":
    data = get_data("../data/Day10.txt")
    start_pos = Point.from_iterable(find_start(data))
    directions = [Point(0, 1), Point(0, -1), Point(-1, 0), Point(1, 0)]
    for direction in directions:
        size = loop_len(data, start_pos, direction)
        if size != -1:
            print(size//2)
            break
