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
	def test_read_1(self):
		line = '2:'
		num = netflix_read(line)
		self.assertEqual(num, 2)

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

    # -----
    # print
    # -----
	def test_print_1(self):
	    w = StringIO()
	    netflix_print(w,1, 1)
	    self.assertEqual(w.getvalue(), "1:\n")

	def test_print_2(self):
	    w = StringIO()
		netflix_print(w,0, 1232)
	    self.assertEqual(w.getvalue(), "1232\n")

	def test_print_3(self):
	    w = StringIO()
	    netflix_print(w ,0, 123)
		self.assertEqual(w.getvalue(), "123\n")

	    # -----
	    # solve
	    # -----

	def test_solve_1(self):
	    r = StringIO("")
		w = StringIO()
	    netflix_solve(r, w)
		self.assertEqual(w.getvalue(), "RMSE: 0")

	def test_solve_2(self):
		r = StringIO("10343:\n887364 \n")
		w = StringIO()
		netflix_solve(r, w)
	    self.assertEqual(w.getvalue(), "10343\n3.2\nRMSE: 0.2\n")

	def test_solve_3(self):
	    r = StringIO("12033: \n 1010799 1649947")
		w = StringIO()
		netflix_solve(r, w)
		self.assertEqual(w.getvalue(), "12033:\n2.2\n2.61\nRMSE: 0\n")


if __name__ == "__main__":
    main()
