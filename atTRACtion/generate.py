class Trac_code():
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.n = 10

    def get(self):
        return """#(ds,+1,(#(gb,X,1,(#(ad,#(ad,#(cl,+1,#(su,X,1)),{0}),#(cl,+1,#(su,X,2)))),{1}))))'#(ss,+1,X)'#(ps,RuCTF_#(cl,+1,{2}))'""".format(
            str(self.first), str(self.second), str(self.n))


def generate(context):
    participant = context['participant']
    task = context['task']
    id = str(participant.id)
    first = id
    second = int(id ** (3 / 2))
    a = Trac_code(first, second)
    return TaskStatement('Аттаркцион для %s' % participant,
                         'Мы нашли странную папку в нашем архиве. \n   На ней была надпись:"И этот язык разрабатывали более 5 лет? Пфф. !965г." ' + "\n" + a.get(), )


if __name__ == "__main__":
    first = 242222425
    second = 10000001
    a = Trac_code(first, second)
    print(a.get())
