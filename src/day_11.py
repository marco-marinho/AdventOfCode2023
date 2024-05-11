from itertools import combinations

from util import get_board


def calculate_distance(rate):
    data = get_board("../data/Day11.txt")
    double_rows = [i for i in range(1, data.shape[0] - 1) if b"#" not in data[i, :]]
    double_cols = [i for i in range(1, data.shape[1] - 1) if b"#" not in data[:, i]]

    galaxies = [
        (
            i + sum(1 for x in double_rows if i > x) * (rate - 1),
            j + sum(1 for x in double_cols if j > x) * (rate - 1),
        )
        for i, line in enumerate(data)
        for j, c in enumerate(line)
        if c == b"#"
    ]

    distances = [abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in combinations(galaxies, 2)]

    return sum(distances)


if __name__ == "__main__":
    print("Task 01:", calculate_distance(2))
    print("Task 02:", calculate_distance(1000000))
