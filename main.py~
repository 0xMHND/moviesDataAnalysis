IN_FILE = "movies.dat"
OUT_FILE = "temp"

import sys
import numpy as np
import re #regexp
import matplotlib.pyplot as plt

title = []
movie_date = []
date_re = re.compile("\([^\d]*(\d+)[^\d]*\)") #get numbers between '()'


'''''''''''''''''''''''''''
   parse IN_FILE into movie, title genre
   e.g.
   moveie :: title :: genre
   1919::Madeline (1998)::Children's|Comedy

'''''''''''''''''''''''''''
try:
    with open(IN_FILE) as f:
        for line in f:
            line = line.strip()
            line_sp = line.split("::")
            movie, title_local, genre = line_sp
            title.append(title_local)

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
    plot + Configration

'''''''''''''''''''''''''''

x = np.arange(min_yr, max_yr+1, 1);
y = movie_year_cnt
plt.bar(x, y,)
plt.ylabel("number of movies")
plt.tight_layout()

plt.show()
