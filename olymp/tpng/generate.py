TITLE_TEMPLATES = {
    'en': 'Flag',
    'ru': 'Флаг',
}
STATEMENT_TEMPLATES = {
    'en':
'''
Under the influence of the sun radiation, the flag was rendered colorless. What country this flag belonged to?

P.S. Don't try to find this country on the map.
''',
    'ru':
'''
Под влиянием солнечной радиации, с флага исчезли все цвета. Флаг какой страны это был?

P.S. Не пытайтесь найти эту страну на карте.
''',
}


def generate(context):
	participant = context['participant']
	locale = context['locale']
	task = context['task']

	private_files = sorted(TaskFile.get_private_files(task), key=lambda task_file: task_file.name)
	private_file = private_files[participant.id]
	TaskFile.copy_file_for_participant(private_file, participant, "flag.png")

	return TaskStatement(TITLE_TEMPLATES[locale], STATEMENT_TEMPLATES[locale])
