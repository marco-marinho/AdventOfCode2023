from Day01 import task1, task2
from util import get_data


class TestDay01:
    def test_task1(self):
        data = get_data("../data/Day01.txt")
        assert task1(data) == 54953

    def test_task2(self):
        data = get_data("../data/Day01.txt")
        assert task2(data) == 53868
