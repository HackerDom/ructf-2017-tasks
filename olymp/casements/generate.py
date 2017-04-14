#!/usr/bin/env python3

from collections import Counter

TITLE_TEMPLATES = {
    'en': 'Broken mars rover',
    'ru': 'Сломанных марсоход',
}
STATEMENT_TEMPLATES = {
    'en':
'''
We just got [an access](212.193.68.254:61004) to one of the mars
rovers, which recently endured a severe sandstorm. As a result, disk with
the data was damanged. We're mostly interested in one particular piece
of data. During the analysis, it was discovered that the identifier
of this piece of data has the following frequency table:

`
%s
`

Please help us recover the piece of data we're interested in.
''',
    'ru':
'''
Мы получили [доступ](212.193.68.254:61004) к одному из марсоходов,
который недавно попал в сильную песчанную бурю, из-за чего диск с данными
был поврежден. Нам больше всего интересует определенная часть информации.
Мы смогли установить, что идентификатор интересующей нас информации обладает
следующей таблицей частот:

`
%s
`

Помогите восстановить интересующую нас част информации.
''',
}


flag_ids = [
	# TODO
]


def generate_frequency_table(flag_id):
	return sorted(dict(Counter(flag_id)).items(), key=lambda t: t[1], reverse=True)

def pretty_print_frequency_table(flag_id, frequency_table):
	return "\n".join("%s: %.2lf%%" % (t[0], t[1] / len(flag_id) * 100) for t in frequency_table)


def generate(context):
	participant = context['participant']
	locale = context['locale']

	flag_id = flag_ids[participant.id]
	frequencies = generate_frequency_table(flag_id)
	frequency_table_str = pretty_print_frequency_table(flag_id, frequencies)

	return TaskStatement(TITLE_TEMPLATES[locale], STATEMENT_TEMPLATES[locale] % frequency_table_str)

if __name__ == "__main__":
	flag_id = input("flag_id: ")
	print(pretty_print_frequency_table(flag_id, generate_frequency_table(flag_id)))
