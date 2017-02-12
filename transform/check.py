flag_len = 64
flag_hash = "LQRHQTIOENUDHSFAWCBWKLUVBHAGXMHFNFHGAWXGKIBOSVNPGWIOVPDLVMXCXHIC"
flag = 'FLAGIUDVVHMKHFFLVWGMWHBGSQAIOUHKOPVQBHXNRANDECXXIXWNLHICGOCWTBPS'
length_byte_num = 73


def bwt(string, length):
	buffer = ''.join([string[i % length] for i in range(0, length * 2 - 1)])
	sorted = [i for i in range(0, length)]
	for i in range(0, length):
		for j in range(length - 1, i, -1):
			if buffer[sorted[j - 1]: sorted[j - 1] + length] > buffer[sorted[j]: sorted[j] + length]:
				tmp = sorted[j - 1]
				sorted[j - 1] = sorted[j]
				sorted[j] = tmp
	result = ''.join([buffer[sorted[i] + length - 1] for i in range(0, length)])
	return result


def bwt_revert(string, length):  # may return trash if input is not valid bft result
	bytes = [ord(c) for c in string]
	c = [0 for _ in range(0, 256)]
	p = [None for _ in range(0, length)]
	for i in range(0, length):
		p[i] = c[bytes[i]]
		c[bytes[i]] += 1
	d = [0 for _ in range(0, 256)]
	for i in range(1, 256):
		d[i] = d[i - 1] + c[i - 1]
	t = [None for _ in range(0, length)]
	for i in range(0, length):
		t[i] = d[bytes[i]] + p[i]
	result_bytes = [None for _ in range(0, length)]
	last_byte_position = length - 1
	for i in range(length - 1, -1, -1):
		result_bytes[i] = bytes[last_byte_position]
		last_byte_position = t[last_byte_position]
	result_chars = [chr(n) for n in result_bytes]
	result_str = ''.join(result_chars)
	return result_str


def string_rotations(string):
	return [string[i:] + string[0:i] for i in range(0, len(string))]


def check_full_transform(bytes):
	if len(bytes) < flag_len:
		return False
	rotations = string_rotations(flag)
	for r in rotations:
		founded = True
		for i in range(0, flag_len):
			if ord(r[i]) != bytes[i]:
				founded = False
				break
		if founded:
			if len(bytes) == flag_len:
				return True
			if bytes[flag_len] == ord('\r') or bytes[flag_len] == ord('\n'):
				return True
			if bytes[flag_len] == 0 and (len(bytes) < length_byte_num or bytes[length_byte_num - 1] == flag_len):
				return True
			return False
	return False


def check_partial_transform(bytes):
	zero_index = bytes.find(0)
	if not 0 < zero_index < flag_len:
		return False
	if len(bytes) < length_byte_num or bytes[length_byte_num - 1] != zero_index:
		return False
	string = ''.join([chr(bytes[i]) for i in range(0, zero_index)])
	bwt_result = bwt(string, zero_index)
	if flag_hash.startswith(bwt_result):
		return True
	return False


def check(bytes):
	if check_full_transform(bytes):
		return True
	if check_partial_transform(bytes):
		return True
	return False


def main():
	filename = "solution"
	f = open(filename, "rb")
	bytes = f.read()
	print("True" if check(bytes) else "False")


if __name__ == "__main__":
	main()
