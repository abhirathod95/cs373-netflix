import sys
import pickle
import requests
from numpy import mean, sqrt, square, subtract

curr_mov_id = -1
movie = False
actual = []
predicted = []

bytes = requests.get('http://www.cs.utexas.edu/users/fares/netflix-caches/snm2235-jml4759-actualCustomerRating.pickle').content
actual_custmovid = pickle.loads(bytes)
bytes = requests.get('http://www.cs.utexas.edu/users/fares/netflix-caches/snm2235-jml4759-averageCustomerRating.pickle').content
avgcust_custid = pickle.loads(bytes)
bytes = requests.get('http://www.cs.utexas.edu/users/fares/netflix-caches/snm2235-jml4759-averageMovieRating.pickle').content
avgmov_movid = pickle.loads(bytes)
	
def netflix_read(line):
	"""
	read the line from input
	line is a string for the current line in the file
	returns an int (the id of the movie; -1 if the line is movie id)
	"""
	global curr_mov_id, movie
	if ':' in line:
		ids = line.split(':')
		# Make sure its an int
		try:
			num = int(ids[0])
		except Exception as e:
			return -1
		# Make sure its within a valid range for movie ids
		if num < 1 or num > 17770:
			return -1
		curr_mov_id = num
		movie = True
		return num
	else:
		line = line.strip()
		# Make sure its an int 
		try:
			num = int(line)
		except Exception as e:
			return -1
		# Make sure that its within the range of the customer ids
		if num < 1 or num > 2649429:
			return -1
		return num


def rmse(act, pred):
	"""
	Calculates the rmse of all the actual and predicted values stored so far
	Returns a float 
	"""

	# Make sure the params are lists
	if(type(act) != list or type(pred) != list): 
		return 0;

	# If either of the lists are empty, return 0
	if not act or not pred:
		return 0;

	if len(act) != len(pred):
		return 0;


	ans = sqrt(mean(square(subtract(act, pred))))
	return round(ans, 2)

def netflix_eval(customer_id):
	# Add in the actual value to the actual array so that we can calculate rmse later
	global actual, predicted

	avg_mov_rating = avgmov_movid[curr_mov_id]
	avg_cust_rating = avgcust_custid[customer_id]

	pred = (avg_cust_rating + avg_mov_rating) / 2
	pred = round(pred, 1)

	actual.append(actual_custmovid[(customer_id, curr_mov_id)])
	predicted.append(pred)

	return pred

def netflix_print(w, movieFlag, i):
	"""
	print three ints
	w a writer
	i the movie id
	j the customer id
	"""
	if movieFlag:
		w.write(str(i) + ":\n")
		movie = False
	else:
		w.write(str(i) + "\n")

def netflix_solve(r, w):
	"""
	r a reader
	w a writer
	"""
	global actual, predicted, movie
	for s in r:
		i = netflix_read(s)
		if i != -1 and curr_mov_id != -1:
			if not movie:
				i = netflix_eval(i)
			netflix_print(w, movie, i)
	calculated_rmse = rmse(actual, predicted)
	print('RMSE: {0:.2f}'.format(calculated_rmse))