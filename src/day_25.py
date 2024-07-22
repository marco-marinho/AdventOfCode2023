from util import get_data
from itertools import chain

import numpy as np


def main():
    lines = get_data('../data/Day25.txt')
    data = [line.replace(":", "").split(" ") for line in lines]
    indexes = {name: index for index, name in enumerate(set(chain(*data)))}

    laplacian = np.zeros((len(indexes), len(indexes)))
    for line in data:
        head = line[0]
        for tail in line[1:]:
            laplacian[indexes[head], indexes[tail]] = -1
            laplacian[indexes[tail], indexes[head]] = -1

    for column in range(laplacian.shape[1]):
        laplacian[column, column] = -np.sum(laplacian[:, column])

    vals, vecs = np.linalg.eigh(laplacian)
    sorted_vecs = vecs[:, vals.argsort()]

    ans = sum(sorted_vecs[:, 1] > 0) * sum(sorted_vecs[:, 1] < 0)
    print("Task 01:", ans)


if __name__ == '__main__':
    main()
