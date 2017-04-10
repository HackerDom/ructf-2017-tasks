def generate(context):
	participant = context['participant']

	internal_file_name = str(participant.id + 1) + ".png"
	visible_file_name = "flag.png"

	return TaskStatement('tpng', 'С флага исчезло изображение, определите название несуществующей страны, к которой он относился.' % id)
