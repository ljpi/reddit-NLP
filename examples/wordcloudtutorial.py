
# coding: utf-8

# In[2]:

get_ipython().magic('matplotlib inline')


# 
# Image-colored wordcloud
# =======================
# 
# You can color a word-cloud by using an image-based coloring strategy
# implemented in ImageColorGenerator. It uses the average color of the region
# occupied by the word in a source image. You can combine this with masking -
# pure-white will be interpreted as 'don't occupy' by the WordCloud object when
# passed as mask.
# If you want white as a legal color, you can just pass a different image to
# "mask", but make sure the image shapes line up.
# 
# 

# In[24]:

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#put path of where ur files are
d = path.dirname('storm-trooper.gif_595')

# input a txt file of our words here instead of a new hope
text = open(path.join(d, 'a_new_hope.txt')).read()

# use the reddit picture i send you here, only png works i think
alice_coloring = np.array(Image.open(path.join(d, "redditpic.png")))
stopwords = set(STOPWORDS)
#here he added a stop word said because there was a lot of them in the alice text.
#so we can add any stop words that we may see have too high of frequencies here
#stopwords.add("said")

#change the max words and the font size to see what looks best. i wouldnt touch the rest too much lol
wc = WordCloud(width=1200, height=1100, background_color="white", max_words=1000, mask=alice_coloring,
               stopwords=stopwords, max_font_size=100, random_state=42)
# generate word cloud
wc.generate(text)

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)

# show

plt.axis("off")

#makes the picture bigger
plt.figure( figsize=(20,10) )

#gives the wordcloud the same colors as pictures
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")


