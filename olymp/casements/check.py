#!/usr/bin/env python3

flags = [
	# TODO
]

def get_participant_id(answer):
	if answer in flags:
		return flags.index(answer)
	return None


def check(attempt, context):
	answer_is_for = get_participant_id(attempt.answer)
	if answer_is_for == None:
		return Checked(False)

	if answer_is_for == attempt.participant.id:
		return Checked(True)

	return CheckedPlagiatrist(False, answer_is_for)


if __name__ == "__main__":
	answer = input("Answer: ")

	print(get_participant_id(answer))
