import sys
import pickle
import requests
from numpy import mean, sqrt, square, subtract

curr_mov_id = -1
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
			return (-1, None)
		# Make sure its within a valid range for movie ids
		if num < 1 or num > 17770:
			return (-1, None)
		curr_mov_id = num
		movie = True
		return (num, True)
	else:
		line = line.strip()
		# Make sure its an int 
		try:
			num = int(line)
		except Exception as e:
			return (-1, None)
		# Make sure that its within the range of the customer ids
		if num < 1 or num > 2649429:
			return (-1, None)
		return (num, False)


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
	ans = '{0:.2f}'.format(int(ans*100)/float(100))
	return float(ans)

def netflix_eval(customer_id):
	# Add in the actual value to the actual array so that we can calculate rmse later
	global actual, predicted

	try:
		avg_mov_rating = avgmov_movid[curr_mov_id]
		avg_cust_rating = avgcust_custid[customer_id]

		pred = (avg_cust_rating + avg_mov_rating) / 2
	except Exception as e:
		return -1

	pred = '{0:.2f}'.format(int(pred*100)/float(100))
	pred = float(pred)

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
	else:
		w.write(str(i) + "\n")

def netflix_solve(r, w):
	"""
	r a reader
	w a writer
	"""
	global actual, predicted
	for s in r:
		i, movie = netflix_read(s)
		if i != -1 and curr_mov_id != -1:
			if not movie:
				i = netflix_eval(i)
			if i != -1:
				netflix_print(w, movie, i)
	calculated_rmse = rmse(actual, predicted)
	print('RMSE: {0:.2f}'.format(calculated_rmse))