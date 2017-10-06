
# coding: utf-8

# In[4]:

# %load main.py
import praw
import datetime
from praw.models import MoreComments
from textblob import TextBlob
import nltk
import sys
import numpy



client_id = open("../client_id").read()
client_secret = open("../client_secret").read()
password = open("../password").read()
user_agent = open("../user_agent").read()
username = open("../username").read()


reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent= user_agent,
                     password = password,
                     username = username)



print("US News Top 10 All Time")


def getNews(subreddit, n):
    results=list()
    dic=dict()
    commentDic=dict()
    for submission in reddit.subreddit(subreddit).top(limit=n):
        tempList=list()
        tempList.append(submission.fullname)
        tempList.append(submission.title)
        tempList.append(datetime.datetime.fromtimestamp(submission.created))
        tempList.append(submission.score)
        tempList.append(submission.url)
        tempList.append(submission.comments.list())
        commentDicTemp=dict()
        for comment in submission.comments:
            if isinstance(comment, MoreComments):
                continue
            else:
                commentDicTemp[comment.id]=comment.body
                commentDic[comment.id]=comment.body
        tempList.append(commentDicTemp)
        dic[submission.id]=tempList
    results.append(dic)
    results.append(commentDic)
    return results


startTime = datetime.datetime.now()

resultsUS = getNews("news",10)
usNews = resultsUS[0]
usComments = resultsUS[1]

resultsWorld = getNews("worldnews",10)
worldNews = resultsWorld[0]
worldComments = resultsWorld[1]

endTime = datetime.datetime.now()

print(startTime)
print(endTime)
#10 records ~80 seconds
#100 records ~800 seconds
print((endTime-startTime).seconds)

print(resultsUS)
print(usNews)
print(usComments)


#Step 1: Sentiment Analysis & Descriptive Stats

usSent = list()
worldSent = list()

for k in usNews:
    print(k)
    title = usNews[k][1]
    n = TextBlob(title)
    print(n)
    print(n.sentiment.polarity)
    usSent.append(n.sentiment.polarity)

for k in worldNews:
    print(k)
    title = worldNews[k][1]
    n = TextBlob(title)
    print(n)
    print(n.sentiment.polarity)
    worldSent.append(n.sentiment.polarity)

usSentAvg = sum(usSent) / float(len(usSent))
worldSentAvg = sum(worldSent) / float(len(worldSent))

print("US")
print(usSentAvg)
print(min(usSent))
print(max(usSent))

print("World")
print(worldSentAvg)
print(min(worldSent))
print(max(worldSent))

#also get standard deviation
#and more general descriptive stats
#visualize

#Step 2: LSA

#Step 3: By Time Analysis

#Step 4: Visualization - Word Clouds and others
#benchmark vs random word sample

#Step 5 (Bonus): Comment stuff AND/OR title classifications unsupervised



# In[35]:

#LSA part
usNews_titles = []
for k in usNews:
    usNews_titles.append(usNews[k][1])


# In[ ]:

import nltk
nltk.download('all')


# In[61]:

def LSA(title_list):
    words = []
    for i in title_list:
        words += i.split()
    filtered_words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]
    terms = {}
    for j in filtered_words:
            if j not in terms:
                terms[j] = 1
            else:
                terms[j] += 1
    return terms


# In[62]:

LSA(usNews_titles)


# In[59]:




# In[56]:




# In[57]:




# In[58]:



