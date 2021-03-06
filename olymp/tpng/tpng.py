#!/usr/bin/env python3

import png
import zlib
import struct
import math
import os
import check


def encode5(string):
	bs = string.encode('ascii')
	num = 0
	for i in range(0, len(bs)):
		num = num * 256 + bs[i]
	return to5array(num)


def to5array(n):
	if n < 5:
		return [n]
	else:
		return to5array(n // 5) + [n % 5]


def write_idat_with_flag(encoded_flag, original_image_file_name, outfile):
	reader = png.Reader(filename=original_image_file_name)
	width, height, pixels, meta = reader.read()
	if height != len(encoded_flag):
		raise Exception(f"Encoded flag length {len(encoded_flag)} is not equal to height {height}")
	scanlines = list(pixels)
	filtered_scanlines = []
	for i in range(0, height):
		filtered_scanlines.append(
			png.filter_scanline(encoded_flag[i], scanlines[i], meta['planes'], scanlines[i - 1] if i > 0 else None))
	compressed = zlib.compress(b''.join(filtered_scanlines))
	png.write_chunk(outfile, b'IDAT', compressed)


def find_list_in_list(mylist, pattern):
	matches = []
	for i in range(len(mylist)):
		if mylist[i] == pattern[0] and mylist[i:i+len(pattern)] == pattern:
			matches.append(i)
	return matches


def insert_flag(flag, original_image_file_name, outfile):
	encoded_flag = encode5(flag)
	original_image_file = open(original_image_file_name, "rb")
	original_image_bytes = original_image_file.read()
	original_image_file.close()
	all_pos = find_list_in_list(original_image_bytes, b'IDAT')
	if len(all_pos) != 1:
		raise Exception(f"IDAT count is {len(all_pos)}")
	pos = all_pos[0]
	outfile.write(original_image_bytes[:pos - 4])
	original_idat_len = struct.unpack("!I", original_image_bytes[pos-4: pos])[0]
	write_idat_with_flag(encoded_flag, original_image_file_name, outfile)
	outfile.write(original_image_bytes[pos + original_idat_len + 8:])
	outfile.close()

'''
import random
def generate_flags():
	random.seed(697)
	prefs = ["Sol", "Ker", "Bot", "Fag", "Tem", "Xab"]
	middles = ["ava", "iri", "olo", "ece", "ihi", "yjy"]
	suffixes = ["kek", "mok", "tok", "sik", "wak", "puk"]
	array = []
	for p in prefs:
		for m in middles:
			for s in suffixes:
				array.append("RuCTF:" + p + m + s)
	random.shuffle(array)
	return array
'''

def generate_original():
	height = 51
	pixels = [[[234, 215, 197] for j in range(0, int(math.ceil(height/3*5)))] for i in range(0, height)]
	png.from_array(pixels , 'RGB').save("original.png")


if __name__ == "__main__":
	generate_original()
	# flags = generate_flags()
	flags = check.flags
	# allFlags = "[" + ', '.join(['"' + f + '"' for f in flags]) + "]"
	script_dir = os.path.dirname(__file__)
	for index, flag in enumerate(flags):
		insert_flag("RuCTF:" + flag, "original.png", open(os.path.join(script_dir, os.path.join("generated", str(index+1).zfill(3) + ".png")), "wb"))
