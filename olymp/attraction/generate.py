TITLE_TEMPLATES = {
    'en': 'Attraction',
    'ru': 'Аттракцион',
}
STATEMENT_TEMPLATES = {
    'en':
'''
We found an old folder in the archives that dates back to year 1965.
It has a line written in it which we still cannot decypher:

```
It took 5 years to develop this language? Just look at this:

%s
```
''',
    'ru':
    '''
Мы нашли старую папку в нашем архиве, датированную 1965 годом.
Лишь одна запись пока что остается нам непонятной:

```
И этот язык разрабатывали более 5 лет? Вы только посмотрите на это:

%s
```
''',
}

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
    locale = context['locale']

    id = participant.id
    first_param = id
    second_param = int(id ** (3 / 2))
    a = Trac_code(first_param, second_param)
    trac_source = a.get()
    return TaskStatement(TITLE_TEMPLATES[locale],
                         STATEMENT_TEMPLATES[locale] % trac_source,)
