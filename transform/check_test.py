import unittest
import check

full_flag = 'FLAGIUDVVHMKHFFLVWGMWHBGSQAIOUHKOPVQBHXNRANDECXXIXWNLHICGOCWTBPS'
flag_len = 64


class TestCheck(unittest.TestCase):
	def test_full_transform_only(self):
		bytes = full_flag.encode('ascii')
		self.assertTrue(check.check_full_transform(bytes))

	def test_full_transform_wrong_flag(self):
		wrong_flag = 'W' + full_flag[1:]
		bytes = wrong_flag.encode('ascii')
		self.assertFalse(check.check_full_transform(bytes))

	def test_full_transform_empty(self):
		bytes = ''.encode('ascii')
		self.assertFalse(check.check_full_transform(bytes))

	def test_full_transform_small(self):
		bytes = full_flag[:10].encode('ascii')
		self.assertFalse(check.check_full_transform(bytes))

	def test_full_transform_0(self):
		bytes = (full_flag + '\0').encode('ascii')
		self.assertTrue(check.check_full_transform(bytes))

	def test_full_transform_0abraka(self):
		bytes = (full_flag + '\0').encode('ascii')
		self.assertTrue(check.check_full_transform(bytes))

	def test_full_transform_n(self):
		bytes = (full_flag + '\nabraka').encode('ascii')
		self.assertTrue(check.check_full_transform(bytes))

	def test_full_transform_r(self):
		bytes = (full_flag + '\rabraka').encode('ascii')
		self.assertTrue(check.check_full_transform(bytes))

	def test_full_transform_long(self):
		bytes = (full_flag + '\0' + 20*'\x01').encode('ascii')
		self.assertFalse(check.check_full_transform(bytes))

	def test_full_transform_len(self):
		bytes = (full_flag + '\0' + 7*'\1' + '\x40' + 'abraka').encode('ascii') # 40h = 64d
		self.assertTrue(check.check_full_transform(bytes))

	def test_bwt_revert(self):
		self.assertEqual(check.bwt_revert('L', 1), 'L')

	# 'LQ' and 'LQR' are not correct bwt result

	def test_bwt_revert3(self):
		result = check.bwt_revert('LQRH', 4)
		rotations = check.string_rotations('RQLH')
		self.assertTrue(result in rotations)

	def test_bwt(self):
		self.assertEqual(check.bwt('RQLH', 4), 'LQRH')

	def test_check_partial_transform_L(self):
		bytes = ('L\x00' + 71*'\x01').encode('ascii')
		self.assertTrue(check.check_partial_transform(bytes))

	def test_check_partial_transform_RQLH(self):
		bytes = ('RQLH\x00' + 68*'\x04').encode('ascii')
		self.assertTrue(check.check_partial_transform(bytes))

	def test_check_partial_transform_RQHK(self):
		bytes = ('RQHL\x00' + 68*'\x04').encode('ascii')
		self.assertFalse(check.check_partial_transform(bytes))

	def test_check_partial_transform_QQ(self):
		bytes = ('QQ\x00' + 70*'\x02').encode('ascii')
		self.assertFalse(check.check_partial_transform(bytes))

	def test_check_partial_transform(self):
		bytes = ''.encode('ascii')
		self.assertFalse(check.check_partial_transform(bytes))


if __name__ == '__main__':
	unittest.main()