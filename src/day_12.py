import util
from functools import lru_cache


def parse_solution(solution: str) -> list[int]:
    return list(map(int, solution.split(',')))


@lru_cache(maxsize=None)
def solve(puzzle: str, solutions: tuple[int], blocked: bool):
    solved = len(solutions) == 0
    if solved and "#" not in puzzle:
        return 1
    if (solved and "#" in puzzle) or solutions[0] > len(puzzle):
        return 0

    match (puzzle[0], blocked):
        case "#", True:
            return 0
        case "#", False:
            if '.' not in puzzle[:solutions[0]]:
                return solve(puzzle[solutions[0]:], solutions[1:], True)
            else:
                return 0
        case ".", _:
            return solve(puzzle[1:], solutions, False)
        case "?", True:
            return solve(puzzle[1:], solutions, False)
        case "?", False:
            acc = 0
            if '.' not in puzzle[:solutions[0]]:
                acc += solve(puzzle[solutions[0]:], solutions[1:], True)
            acc += solve(puzzle[1:], solutions, False)
            return acc


if __name__ == '__main__':
    data = util.get_data("../data/Day12.txt")
    puzzles, solutions = zip(*[parts for line in data
                               for parts in [line.split(" ")]])
    solutions = list(map(parse_solution, solutions))

    acc = 0
    for a, b in zip(puzzles, solutions):
        res = solve(a, tuple(b), False)
        acc += res
    print("Task 01:", acc)
    acc = 0
    for a, b in zip(puzzles, solutions):
        res = solve("?".join([a] * 5), tuple(b * 5), False)
        acc += res
    print("Task 02:", acc)
