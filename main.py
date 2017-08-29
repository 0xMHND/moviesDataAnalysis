IN_FILF_MOVIES = "movies.dat"
IN_FILE_USERS = "users.dat"
IN_FILE_RATINGS = "ratings.dat"


import sys
import numpy as np
import re #regexp
import matplotlib.pyplot as plt

title = []
scientist = []
movie_date = []

date_re = re.compile("\([^\d]*(\d+)[^\d]*\)") #get numbers between '()'

usr = {}
users = []
sci_users = []

'''''''''''''''''''''''''''
   parse users.dat 
   e.g.
   UserID::Gender::Age::Occupation::Zip-code

'''''''''''''''''''''''''''
try:
    with open(IN_FILE_USERS) as f:
        for line in f:
            line = line.strip()
            line_sp = line.split("::")
            usr['id'], usr['gender'], usr['age'], usr['occupation'], zipCode = line_sp
            users.append(usr.copy())
            if usr['occupation'] == "15":
                sci_users.append(usr.copy())

except IOError:
    print("Cannot open file")
    sys.exit(1)

male_cnt, female_cnt = 0,0;
for i, usr in enumerate(sci_users):
    if usr['gender'] =='F':
        female_cnt += 1
    elif usr['gender'] =='M':
        male_cnt += 1

min_sci_age = min(int(s['age']) for s in sci_users)
max_sci_age = max(int(s['age']) for s in sci_users)
print("males ", male_cnt, "females ", female_cnt)
print("max age ", max_sci_age, "min age ", min_sci_age)

sci_per_age = [0]*(max_sci_age-min_sci_age + 1)
cnt = 0 
for i, val in enumerate(sci_users):
    try:
        sci_per_age[int(val['age']) - min_sci_age] += 1
    except:
        print("error adding scientist age to sci_per_age")
        pass


'''''''''''''''''''''''''''
   parse IN_FILE_MOVIES into movie, title genre
   e.g.
   moveie :: title :: genre
   1919::Madeline (1998)::Children's|Comedy

'''''''''''''''''''''''''''
movie = {}
movies = []
try:
    with open(IN_FILF_MOVIES) as f:
        for line in f:
            line = line.strip()
            line_sp = line.split("::")
            movie['m_id'], movie['title'], movie['genre'] = line_sp
            movies.append(movie.copy())
            title.append(movie['title'])

except IOError:
    print("Cannot open file")
    sys.exit(1)

'''''''''''''''''''''''''''
   get movies' release year.

'''''''''''''''''''''''''''
for i, val in enumerate(title):
    date = re.findall(date_re, title[i])
    if(len(date)>1):
        movie_date.append(int(date[-1]))
    else:
        movie_date.append(int(date[0]))
	
min_yr = min(int(s) for s in movie_date)
max_yr = max(int(s) for s in movie_date)
print("minimum = ", min_yr)
print("maximum = ", max_yr)


'''''''''''''''''''''''''''
   count number of moveis/year 

'''''''''''''''''''''''''''
movie_year_cnt = [0]*(max_yr-min_yr + 1)
cnt = 0 
for i, val in enumerate(movie_date):
    try:
        movie_year_cnt[val-min_yr] += 1
    except:
        print("%d - ERROR ()()()" %cnt)
        cnt += 1
        pass


'''''''''''''''''''''''''''
   parse IN_FILE_RATINGS
   e.g.
   UserID::MovieID::Rating::Timestamp
   6040::3334::5::960971875

'''''''''''''''''''''''''''
movie_rated = {}
ratings = []
try:
    with open(IN_FILE_RATINGS) as f:
        for line in f:
            line = line.strip()
            line_sp = line.split("::")
            movie_rated['u_id'], movie_rated['movieID'], movie_rated['rating'], movie_rated['timestamp'] = line_sp
            ratings.append(movie_rated.copy())
except IOError:
    print("Cannot open file")
    sys.exit(1)

sorted_ratings = sorted(ratings , key=lambda k: int(k['movieID'])) 
temp_cnt = 0
total_rating = 0
temp_movie = "nn"
weighted_movie_rate = {}
w_movies_ratings = []
for i in sorted_ratings:
    if i['movieID'] != temp_movie and temp_cnt!=0:
        weighted_movie_rate['id'] = temp_movie
        weighted_movie_rate['rating'] = total_rating/temp_cnt
        temp_cnt = 0
        temp_movie = i['movieID']
        total_rating = 0
        w_movies_ratings.append(weighted_movie_rate.copy())
    else:
        temp_movie = i['movieID']
        total_rating += int( i['rating'] )
        temp_cnt += 1
    
for i,w in enumerate(w_movies_ratings):
    print("id[",i,"] : " ,w)
    if i == 1000:
        break
'''''''''''''''''''''''''''
    plot + Configration

'''''''''''''''''''''''''''
'''
plt.subplot(221)
x = np.arange(min_yr, max_yr+1, 1);
y = movie_year_cnt
plt.bar(x, y,)
plt.tight_layout()
plt.title("nubmer of movies per year")

plt.subplot(222)
x = np.arange(min_sci_age, max_sci_age+1, 1);
y = sci_per_age
plt.bar(x, y)
plt.title(" scientists age dist.")

plt.subplot(223)

'''
#x = np.arange(0,3951, 1)
y = [m['rating'] for m in w_movies_ratings]
'''
for i, val in enumerate(y):
    print("id[",i,"] : " ,val)
    '''
x = range(len(y))
plt.plot(x, y, "ro")
plt.title("movies' ratings")

plt.show()
