import sys
import pickle
import requests
from numpy import mean, sqrt, square, subtract

curr_mov_id = -1
actual = []
predicted = []

# Get all the caches that we need
bytes = requests.get(
    'http://www.cs.utexas.edu/users/fares/netflix-caches/snm2235-jml4759-actualCustomerRating.pickle').content
actual_custmovid = pickle.loads(bytes)
bytes = requests.get(
    'http://www.cs.utexas.edu/users/fares/netflix-caches/snm2235-jml4759-averageCustomerRating.pickle').content
avgcust_custid = pickle.loads(bytes)
bytes = requests.get(
    'http://www.cs.utexas.edu/users/fares/netflix-caches/snm2235-jml4759-averageMovieRating.pickle').content
avgmov_movid = pickle.loads(bytes)


base_all_mov = 0
base_all_cust = 0

# Go through all the mean ratings for all movies and find the mean of means
for rating in avgmov_movid.values():
    base_all_mov += rating
base_all_mov = base_all_mov / len(avgmov_movid.values())

# Go through all the mean ratings for all customer ratings and find the mean of means
for rating in avgcust_custid.values():
    base_all_cust += rating
base_all_cust = base_all_cust / len(avgcust_custid.values())

# Create a baseline to check how far the customer/movie deviates from the average
baseline = (base_all_mov + base_all_cust) / 2


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
        return 0

    # If either of the lists are empty, return 0
    if not act or not pred:
        return 0

    if len(act) != len(pred):
        return 0

    ans = sqrt(mean(square(subtract(act, pred))))
    ans = '{0:.2f}'.format(int(ans * 100) / float(100))
    return float(ans)


def netflix_eval(customer_id):
    """
    Takes in a float/int that is the customer id
    Uses calculations to predict what the customer would rate the movie that we are on and is
    stored in curr_mov_id
    Returns a 1 decimal place that is the predicted value for this customer id
    """
    # Add in the actual value to the actual array so that we can calculate
    # rmse later
    global actual, predicted

    try:
    	# Subtract the mean movie rating from the base movie rating (mean of means) to 
    	# get the offset of how this movie compares to all the other movies
        mov_offset = base_all_mov - avgmov_movid[curr_mov_id]
        # Subtract the mean customer rating from the base customer rating (mean of means) to 
    	# get the offset of how this customer compares to all the other customers
        cust_offset = base_all_cust - avgcust_custid[customer_id]

        # Predict the baseline and subtract the offsets
        pred = baseline - cust_offset - mov_offset
    except Exception as e:
        return -1

    # We want it in 1 decimal format
    pred = '{0:.1f}'.format(int(pred * 100) / float(100))
    pred = float(pred)
    actual.append(actual_custmovid[(customer_id, curr_mov_id)])
    predicted.append(pred)

    return pred


def netflix_print(w, movieFlag, i):
    """
    print movie id with colon or customer id
    w a writer
    movieFlag is a boolean that tells us if we are printing a movie id or not
    i is the id
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
    w.write('RMSE: {0:.2f}'.format(calculated_rmse))
