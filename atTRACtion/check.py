class Trac_check():
    def __init__(self, first, second, request):
        self.first = first
        self.second = second
        self.request = request
        self.n = 10

    # X - количество шагов. Сверить с заданием
    def counting(self, X):
        if X > 1:
            return (self.first + self.counting(X-1)) + self.counting(X-2)
        else:
            return self.second

        pass

    def Truc_check(self):
        return self.request == "RuCTF_" + str(self.counting(self.n))


def check(attempt, context):
    first = int(attempt.participant.id)
    second = int(attempt.participant.id**(3/2))
    request = str(attempt.answer)

    a = Trac_check(first, second, request)
    if a.Truc_check():
        return Checked(True)
    else:
        return Checked(False)
        #  return CheckedPlagiarist(False)  # проверки на спысывание пока нет




if __name__ == "__main__":
    first = 242222425
    second = 10000001
    request = "RuCTF_22205573489"
    a = Trac_check(first, second, request)
    print(a.Truc_check())
