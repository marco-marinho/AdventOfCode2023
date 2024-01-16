from collections import defaultdict

import numpy as np

from util import get_data

CARD_STR = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

HAND_STR: dict[tuple, int] = {
    (5,): 6,
    (4, 1): 5,
    (3, 2): 4,
    (3, 1, 1): 3,
    (2, 2, 1): 2,
    (2, 1, 1, 1): 1,
    (1, 1, 1, 1, 1): 0,
}


def parse():
    data = get_data("../data/Day07.txt")
    hands, bets = zip(*[(line[0], line[1]) for entry in data for line in [entry.split(" ")]])
    return hands, bets


def parse_hand(hand: str, task_num: int = 1):
    if task_num == 2:
        CARD_STR["J"] = 1
    counts = defaultdict(lambda: 0)
    offset = 1e8
    score = 0
    jokers = 0
    for card in hand:
        if task_num == 2 and card == "J":
            jokers += 1
        else:
            counts[card] += 1
        score += CARD_STR[card] * offset
        offset /= 100
    hand_key = sorted(counts.values(), key=lambda x: -x)
    if hand_key:
        hand_key[0] += jokers
    else:
        hand_key = [5]
    score += HAND_STR[tuple(hand_key)] * 1e10
    return score


def reorder(ilist: list, order: np.ndarray):
    return [ilist[i] for i in order]


def task(task_num: int):
    hands, bets = parse()
    parsed_hands = [parse_hand(hand, task_num) for hand in hands]
    order = np.argsort(parsed_hands)
    score = [int(i[0]) * i[1] for i in zip(reorder(bets, order), range(1, len(bets) + 1))]
    return sum(score)


if __name__ == "__main__":
    print("Task 01:", task(1))
    print("Task 02:", task(2))
