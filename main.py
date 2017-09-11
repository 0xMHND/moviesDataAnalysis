IN_FILF_MOVIES = "movies.dat"
IN_FILE_USERS = "users.dat"
IN_FILE_RATINGS = "ratings.dat"

RATING_LIMIT    = 4.7 #out of 5
NUM_RATINGS     = 2 
AGE_GROUP1      = "1"
AGE_GROUP18     = "18"
AGE_GROUP25     = "25"
AGE_GROUP35     = "35"
AGE_GROUP45     = "45"
AGE_GROUP50     = "50"
AGE_GROUP56     = "56"

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

for i, val in enumerate(movies):
    if (i+1) != int(val['m_id']):
        movie['m_id'] = str(i+1)
        movie['title'] = "NONE"
        movie['genre'] = "NONE"
        movies.insert(i, movie.copy())

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

'''''''''''''''''''''''''''
   count number of movies/year 

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
sci_ratings = []
try:
    with open(IN_FILE_RATINGS) as f:
        for line in f:
            line = line.strip()
            line_sp = line.split("::")
            movie_rated['u_id'], movie_rated['movieID'], movie_rated['rating'], movie_rated['timestamp'] = line_sp
            ratings.append(movie_rated.copy())
            for u in sci_users:
                if (movie_rated['u_id'] == u['id']) and (u['age']==AGE_GROUP56) and (u['gender']=='M'): 
                    sci_ratings.append(movie_rated.copy())
except IOError:
    print("Cannot open file")
    sys.exit(1)

sorted_ratings = sorted(sci_ratings , key=lambda k: int(k['movieID'])) 

temp_cnt = 0
total_rating = 0
temp_movie_id = "nn"
weighted_movie_rate = {}
w_movies_ratings = []
for i in sorted_ratings:
    if int(i['movieID']) != temp_movie_id and temp_cnt!=0:
        if temp_cnt>NUM_RATINGS:  #MORE THAN 4 VOTES
            weighted_movie_rate['id'] = temp_movie_id
            weighted_movie_rate['rating'] = total_rating/temp_cnt
            temp_movie_id = i['movieID']
            w_movies_ratings.append(weighted_movie_rate.copy())
        total_rating = 0
        temp_cnt = 0
    else:
        temp_movie_id = int(i['movieID'])
        total_rating += int( i['rating'] )
        temp_cnt += 1

'''''''''''''''''''''''''''''''''''''''''
Fill in the gaps of unrated movies.

'''''''''''''''''''''''''''''''''''''''''
for i, w in enumerate(w_movies_ratings):
    if (i+1) != int(w['id']):
        weighted_movie_rate['id'] = (i+1)
        weighted_movie_rate['rating'] = np.nan
        w_movies_ratings.insert(i, weighted_movie_rate.copy())


print("++++++++++++++++++ best movies* +++++++++++++++++++")
for i, w in enumerate(w_movies_ratings):
    if w['rating'] > RATING_LIMIT:
        print( movies[w['id']]['title'])

print("\n*more than {2} rated above {0} by Group (Scientist) Age {1}+ (male)".format(RATING_LIMIT, AGE_GROUP56,  NUM_RATINGS) )
'''''''''''''''''''''''''''
    plot + Configration

'''''''''''''''''''''''''''
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

plt.subplot(212)
y = [m['rating'] for m in w_movies_ratings]
x = range(len(y))
plt.plot(x, y, "ro")
plt.title("movies' ratings")

plt.show()
