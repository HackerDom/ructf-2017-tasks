#!/usr/bin/env python3

from collections import Counter
import random

TITLE_TEMPLATES = {
    'en': 'Captain Election',
    'ru': 'Выборы капитана',
}
STATEMENT_TEMPLATES = {
    'en':
'''
The time has come to elect a new captain on the space ship and {mixer_count}
crew members are running for the position. The rest {voter_count} inhabitants
now have to vote for one of the candidates. Knowing that someone voted
against you or against a candidate you voted for is unpleasant, so everyone
decided to make the voting using
[MixNet](https://en.wikipedia.org/wiki/Mix_network) protocol.

Candidate number _i_ generated a key pair for the asymmetric encryption
algorithm _E<sub>i</sub>_ and then gives their open key to all voters.

Voter, decided to vote for the candidate _x_, generates {mixer_count} numbers
_r<sub>j</sub>_, calculates the function
_E<sub>1</sub>(E<sub>2</sub>(...E<sub>m - 1</sub>(E<sub>m</sub>(_x_ + _r<sub>m</sub>_) + _r<sub>m - 1</sub>_)...))
and gives the result to the first and the second candidates.

The first candidate, when given {voter_count} votes, decrypts them all,
applies a permutation and passes all pieces to the second and the third
candidates. The second candidate decrypts all messages, permutes them and
passes to the third and the fourth candidates. It goes on and on, until the
candidate before the last one passes the information to the last and to
all crew members. Last candidate decrypts messages, applies permutation
and makes results public.

This protocol is vulnerable to cunning candidates who are trying to cheat.
They can change several messages, increasing their odds. In order to prevent
such behavior, it was decided that upon transfer, candidate should prove
that the part of their messages were passed unchanged. All candidates are
equal, therefore it doesn't make sense to ask for a different number of
checks for different candidates.

Some of the crew members are troubled by this decision. If there's a
leak and all communications get in the hands of the wrong person, there's
a chance that this person will be able to trace the link between some
person and a vote.

Finally everyone agreed that the probability of tracing someone down
should be less than {percent_chance}%, even if all the communications
are available. For obvious reasons, the person's own vote is not
interesting to trace.

What is the maximal number of votes that can be verifies by the candidate
so that the property above holds? Candidates always act independently.
''',
    'ru':
'''
На космическом корабле пришло время выбирать нового капитана. Выдвинули
свои кандидатуры {mixer_count} членов экипажа. Остальные {voter_count} теперь
должны проголосовать за одну из кандидатур. Так как знание того, что человек
проголовал против тебя в выборах может создать напряженность, было решено
провести голосование с использованием схемы
[MixNet](https://en.wikipedia.org/wiki/Mix_network).

Кандидат номер _i_ генерирует пару ключей для аcсиметричного алгоритма
шифрования _E<sub>i</sub>_, затем отдает открытый ключ всем голосующим.

Голосующий, решивший, что он голосует за кандидата _x_, генерирует
{mixer_count} чисел _r<sub>j</sub>_, вычисляет функцию
_E<sub>1</sub>(E<sub>2</sub>(...E<sub>m - 1</sub>(E<sub>m</sub>(_x_ + _r<sub>m</sub>_) + _r<sub>m - 1</sub>_)...))
и передает ее 1 и 2 кандидатам.

Первый кандидат, получив {voter_count} голосов, расшифровывает все сообщения,
переставляет их случайным образом и передает второму и третьему кандидатам.
Второй кандидат расшифровывает все сообщения, переставляет их случайным
образом и передает третьему и четвертому кандидатам, и т.д. В итоге последний
кандидат расшифровывает изначальные голоса и оглашает результаты публике.
Предпоследний кандидат при этом раскрывает для публики то, что он передал
последнему кандидату.

В такой схеме кандидаты могут схитрить и подменить проходящие через них
сообщения, увеличив количество голосов за себя. Чтобы этого не допустить,
было решено при передаче голосов от кандидата _i_ к кандидату _i + 1_
просить кандидата _i_ доказать подлинность некоторого количества голосов.
Так как все кандидаты равны, всем предлагает проверять одинаковое количество
голосов.

Однако некоторые члены экипажа возмутились: ведь если все коммуникации
попадут в чьи-то руки, то будет шанс, что этот человек для кого-то из экипажа
сможет сказать, за кого тот проголосовал.

В результате бурных дебатов было решено, что вероятность того, что один из
голосущих сможет восстановить чей-то голос при наличии всех
коммуникаций, должна быть меньше {percent_chance}%. Собственный голос,
очевидно, такого человека интересовать не будет.

Какое максимальное количество голосов можно проверять кандидатам, чтобы
данное свойство выполнилось? Кандидаты всегда действуют независимо друг
от друга.
''',
}


DESIRED_PROBABILITY = 0.01


def generate_constants(id):
    random.seed(id)
    mixer_count = random.randint(5, 10)
    voter_count = random.randint(1000, 2000)
    return mixer_count, voter_count


def generate(context):
    participant = context['participant']
    locale = context['locale']

    mixer_count, voter_count = generate_constants(participant.id)

    statement = STATEMENT_TEMPLATES[locale].format(mixer_count=mixer_count,
                                                   voter_count=voter_count + 1,
                                                   percent_chance=DESIRED_PROBABILITY * 100)
    return TaskStatement(TITLE_TEMPLATES[locale], statement)


if __name__ == "__main__":
    id = input("Id: ")

    mixer_count, voter_count = generate_constants(id)
    statement = STATEMENT_TEMPLATES['ru'].format(mixer_count=mixer_count,
                                                 voter_count=voter_count + 1,
                                                 percent_chance=DESIRED_PROBABILITY * 100)
    print(statement)
