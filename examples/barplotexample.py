
# coding: utf-8

# In[27]:

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

#add in our words here
objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp','Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')

x_pos = np.arange(len(objects))

#add in our frequency
frequency = [10,8,6,40,2,40,10,8,6,40,2,40]

#here you can change the width, i assume a .5 width since we are gona have a lot of words and it looks nicer than a bulkier width?
plt.bar(x_pos, frequency, color='#FFC222', align='center', alpha=0.5, width=.5)

plt.xticks(x_pos, objects)
plt.ylabel('Frequency')
plt.title('Word Frequency for /r/news Subreddit')
 
plt.show()

