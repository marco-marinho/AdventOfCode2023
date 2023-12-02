from Day02 import task_01, task_02
from util import get_data
import time


class TestDay02:
    def test_task1(self):
        data = get_data("../data/Day02.txt")
        assert task_01(data) == 2913

    def test_task2(self):
        data = get_data("../data/Day02.txt")
        assert task_02(data) == 55593
