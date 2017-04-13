class Trac_check():
    def __init__(self, first, second, request):
        self.first = first
        self.second = second
        self.request = request
        self.n = 10
        self.mem = dict()

    # X - количество шагов. Сверить с заданием
    def counting(self, X):
        if X in self.mem:
            return self.mem[X]

        if X > 1:
            value = self.first + self.counting(X-1) + self.counting(X-2)
        else:
            value = self.second

        self.mem[X] = value
        return value

    def check(self):
        return self.request == str(self.counting(self.n))


def check_for_id(id, answer):
    first = id
    second = int(id ** (3 / 2))
    return Trac_check(first, second, answer).check()

def check(attempt, context):
    if check_for_id(attempt.participant.id, attempt.answer):
        return Checked(True)

    potential_plagiarists = CheckedPlagiarist.get_potential_plagiarists(attempt.participant)
    for participant in potential_plagiarists:
        if check_for_id(participant.id, attempt.answer):
            return CheckedPlagiarist(False, participant)

    return Checked(False)
