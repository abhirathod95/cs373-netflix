import sys
import pickle
import requests
from numpy import mean, sqrt, square, subtract

curr_mov_id = -1
actual = []
predicted = []
actual_custmovid = None
avgcust_custid = None
avgmov_movid = None

def init_caches():
	"""
	The function initializes all the caches (from the internet) used in this program 
	"""
	global actual_custmovid, avgcust_custid, avgmov_movid
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
	global curr_mov_id
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
		return -1
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
		return int(line)


def rmse(act, pred):
	"""
	Calculates the rmse of all the actual and predicted values stored so far
	Returns a float 
	"""

	# Make sure the params are lists
	assert(type(act) == list)
	assert(type(pred) == list)

	# If either of the lists are empty, set them to list of zeros
	# of size the other list. If both are empty, return 0
	if not act or not pred:
		if act and not pred:
			pred = [0 for x in act]
		elif pred and not act:
			act = [0 for x in pred]
		else:
			return 0

	return sqrt(mean(square(subtract(act, pred))))

def netflix_eval(customer_id):
	# Add in the actual value to the actual array so that we can calculate rmse later
	global actual, predicted
	actual.append(actual_custmovid[(customer_id, curr_mov_id)])
	return -1

def netflix_print(w, i):
	"""
	print three ints
	w a writer
	i the movie id
	j the customer id
	"""
	w.write(str(i) + " " + str(curr_mov_id) + " " + "\n")

def netflix_solve(r, w):
	"""
	r a reader
	w a writer
	"""
	global actual, predicted
	init_caches()
	for s in r:
		i = netflix_read(s)
		if i != -1 and curr_mov_id != -1:
			netflix_print(w, i)
	#calculated_rmse = rmse(actual, predicted)
	#print('RMSE: {0:.2f}'.format(calculated_rmse))