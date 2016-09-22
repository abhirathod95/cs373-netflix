from io import StringIO
from unittest import main, TestCase

from Netflix import netflix_read, netflix_print, netflix_solve, rmse

# ------------
# TestCollatz
# -----------


class TestNetflix (TestCase):

	##########
	## Read ##
	##########

	# Check if it reads movie ids correctly
	# Should just ignore it (return -1) and save it internally
	def test_read_1(self):
		line = '2:'
		num = netflix_read(line)
		self.assertEqual(num, -1)

	# Check if it reads customer ids correctly
	# Should return the customer id as an int
	def test_read_2(self):
		line = '100'
		num = netflix_read(line)
		self.assertEqual(num, 100)

	# check for lower range range for movie ids
	def test_read_3(self):
		line = '0'
		num = netflix_read(line)
		self.assertEqual(num , -1)

	# check the upper range for movie ids
	def test_read_4(self):
		line = '17771:'
		num = netflix_read(line)
		self.assertEqual(num, -1)

	# check lower bounds of customer ids
	def test_read_5(self):
		line = '0:'
		num = netflix_read(line)
		self.assertEqual(num, -1)

	# check upper bounds of customer ids
	def test_read_5(self):
		line = '2649430'
		num = netflix_read(line)
		self.assertEqual(num, -1)

	# check invalid input (non numeric characters)
	def test_read_6(self):
		line = 'adsabdaca;2324'
		num = netflix_read(line)
		self.assertEqual(num, -1)

	def test_read_7(self):
		line = 'adsabdaca:'
		num = netflix_read(line)
		self.assertEqual(num, -1)



	##########
	## RMSE ##
	##########
	def test_rmse_1(self):
		ans = rmse([1,2,4,5], [1,2,3,4,5,6,7])
		self.assertEqual(ans, 0)

	def test_rmse_2(self):
		ans = rmse([1,2,3,4], [])
		self.assertEqual(ans, 0)

	def test_rmse_3(self):
		ans = rmse([], [1,2,3,4])
		self.assertEqual(ans, 0)

	def test_rmse_4(self):
		ans = rmse([],[])
		self.assertEqual(ans, 0)

	def test_rmse_5(self):
		ans = rmse(None, None)
		self.assertEqual(ans, 0)

	def test_rmse_6(self):
		ans = rmse([1,2,3,4],[1,2,3,4])
		self.assertEqual(ans, 0)

	def test_rmse_7(self):
		ans = rmse([1,2,3,4], [5,6,7,8])
		self.assertEqual(ans, 4.0)

if __name__ == "__main__":
    main()