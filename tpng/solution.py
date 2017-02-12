import png
import tpng
import zlib
import struct


def decode5(filters):
	num = 0
	for i in range(0, len(filters)):
		num = num * 5 + filters[i]
	return to256array(num)


def to256array(n):
	if n < 256:
		return [n]
	else:
		return to256array(n // 256) + [n % 256]


def main(filename):
	width, height, pixels, meta = png.Reader(filename=filename).read()
	image_bytes = open(filename, "rb").read()
	all_idat_pos = tpng.find_list_in_list(image_bytes, b'IDAT')
	if len(all_idat_pos) != 1:
		raise Exception(f"IDAT count is {len(all_idat_pos)}")
	idat_pos = all_idat_pos[0]
	original_idat_len = struct.unpack("!I", image_bytes[idat_pos - 4: idat_pos])[0]
	idat_content = image_bytes[idat_pos + 4: idat_pos + 4 + original_idat_len]
	uncompressed = zlib.decompress(idat_content)
	filter_bytes = [uncompressed[i * (len(uncompressed) // height)] for i in range(0, height)]
	result = decode5(filter_bytes)
	result_str = ''.join(chr(i) for i in result)
	print(f'"{result_str}"')


if __name__ == "__main__":
	main("result.png")
