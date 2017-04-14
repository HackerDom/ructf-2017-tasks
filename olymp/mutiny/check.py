#!/usr/bin/env python3

import math
import random


DESIRED_PROBABILITY = 0.01


def generate_constants(id):
    random.seed(id)
    mixer_count = random.randint(5, 10)
    voter_count = random.randint(1000, 2000)
    return mixer_count, voter_count


def calc_min_audits(n, m, p):
    return math.ceil(m * (1 - (1 - p) ** (1 / m)) ** (1 / n) - 1)


def check_for_id(id, answer):
    mixer_count, voter_count = generate_constants(id)
    return answer == str(calc_min_audits(mixer_count, voter_count, DESIRED_PROBABILITY))


def check(attempt, context):
    id = attempt.participant.id
    if check_for_id(id, attempt.answer):
        return Checked(True)

    potential_plagiarists = CheckedPlagiarist.get_potential_plagiarists(attempt.participant)
    for participant in potential_plagiarists:
        if check_for_id(participant.id, attempt.answer):
            return CheckedPlagiarist(False, participant)

    return Checked(False)


if __name__ == "__main__":
    id = input("Id: ")
    answer = input("Answer: ")

    print(check_for_id(id, answer))
