import praw
import datetime

from praw.models import MoreComments
from textblob import TextBlob
import pandas as pd
import nltk
import sys
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from collections import Counter
import re, string

client_id = open("client_id").read()
client_secret = open("client_secret").read()
password = open("password").read()
user_agent = open("user_agent").read()
username = open("username").read()

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     password=password,
                     username=username)

nltk.download('all')




def getNews(subreddit, n):
    results = list()
    dic = dict()
    # commentDic=dict()
    for submission in reddit.subreddit(subreddit).top(limit=n):
        tempList = list()
        tempList.append(submission.fullname)
        tempList.append(re.sub('[%s]' % re.escape(string.punctuation), '', str.lower(submission.title)))
        tempList.append(datetime.datetime.fromtimestamp(submission.created))
        tempList.append(submission.score)
        tempList.append(submission.url)
        # tempList.append(submission.comments.list())
        # commentDicTemp=dict()
        # for comment in submission.comments:
        #     if isinstance(comment, MoreComments):
        #         continue
        #     else:
        #         commentDicTemp[comment.id]=comment.body
        #         commentDic[comment.id]=comment.body
        # tempList.append(commentDicTemp)
        dic[submission.id] = tempList
    results.append(dic)
    # results.append(commentDic)
    return results


startTime = datetime.datetime.now()

resultsUS = getNews("news", 999)
usNews = resultsUS[0]
# usComments = resultsUS[1]

resultsWorld = getNews("worldnews", 999)
worldNews = resultsWorld[0]
# worldComments = resultsWorld[1]

endTime = datetime.datetime.now()

print(startTime)
print(endTime)
# 10 records ~80 seconds
# 100 records ~800 seconds
print((endTime - startTime).seconds)

# Step 1: Sentiment Analysis & Descriptive Stats

usSent = list()
worldSent = list()

for k in usNews:
    # print(k)
    title = usNews[k][1]
    n = TextBlob(title)
    # print(n)
    # print(n.sentiment.polarity)
    usSent.append(n.sentiment.polarity)

for k in worldNews:
    # print(k)
    title = worldNews[k][1]
    n = TextBlob(title)
    # print(n)
    # print(n.sentiment.polarity)
    worldSent.append(n.sentiment.polarity)

usSentAvg = sum(usSent) / float(len(usSent))
worldSentAvg = sum(worldSent) / float(len(worldSent))

UsSubScore = list()
for i in usNews:
    n = (usNews[i][3])
    UsSubScore.append(n)

WorldSubScore = list()
for i in worldNews:
    n = (worldNews[i][3])
    WorldSubScore.append(n)

# print("US")
# print(usSentAvg)
# print(min(usSent))
# print(max(usSent))
#
# print("World")
# print(worldSentAvg)
# print(min(worldSent))
# print(max(worldSent))
#
print(len(UsSubScore))
print(len(WorldSubScore))
print(len(usSent))
print(len(worldSent))
News = pd.DataFrame(
    {'World News': worldSent,
     'US News': usSent,
     'World Post Score': WorldSubScore,
     'US Post Score': UsSubScore
     })

# Descriptive Statistics
print(News.describe())


# Step 2: LSA


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


usNews_titles = []
for k in usNews:
    usNews_titles.append(usNews[k][1])
usLSA = LSA(usNews_titles)
print(usLSA)

worldNews_titles = []
for k in worldNews:
    worldNews_titles.append(worldNews[k][1])
worldLSA = LSA(worldNews_titles)
print(worldLSA)

# Step 3: By Time Analysis
print(usNews)

# first do with us, then do with world
before_trump = list()
after_trump = list()
# nov 8 2016
winning_date = datetime.datetime.strptime('20161108', "%Y%m%d")
# cutoff at may 20
todays_date = datetime.datetime.strptime('20170520', "%Y%m%d")
# 194 days difference between winning date and may20 = 20160428
start_date = datetime.datetime.strptime('20160428', "%Y%m%d")

print(winning_date)
print(todays_date)
print(start_date)

for news_key in usNews:
    timeStamp = (usNews[news_key][2])
    if timeStamp >= winning_date and timeStamp <= todays_date:
        # append to after trump
        after_trump.append(usNews[news_key])
    elif timeStamp >= start_date and timeStamp < winning_date:
        # append to before trump
        before_trump.append(usNews[news_key])
        # else do nothing, out of sample range

print(len(after_trump))
print(len(before_trump))

# just the titles
after_trump_titles_only = list()
for l in after_trump:
    after_trump_titles_only.append(l[1])
before_trump_titles_only = list()
for l in before_trump:
    before_trump_titles_only.append(l[1])

# By Time Analysis For World
before_trump_world = list()
after_trump_worldl = list()

# before and after, sentiment analysis.

# BT = before trump
# AT = after trump

ATusSent = list()

for k in after_trump_titles_only:
    title = k
    n = TextBlob(title)
    ATusSent.append(n.sentiment.polarity)

score = list()
for k in after_trump:
    n = k[3]
    score.append(n)

AT = pd.DataFrame({
    "After Trump News Sentiment": ATusSent,
    "After Trump Score": score
})

# After Trump Descriptive Statistics on Sentiment
print(AT.describe())

afterTrumpLSA = LSA(after_trump_titles_only)
print(afterTrumpLSA)

BTusSent = list()

for k in before_trump_titles_only:
    title = k
    n = TextBlob(title)
    BTusSent.append(n.sentiment.polarity)

score = list()
for k in before_trump:
    n = k[3]
    score.append(n)

BT = pd.DataFrame({
    "Before Trump News Sentiment": BTusSent,
    "Before Trump Score": score
})

print(BT.describe())

beforeTrumpLSA = LSA(before_trump_titles_only)
print(beforeTrumpLSA)


# Step 4: Visualization - Word Clouds and others
# benchmark vs random word sample

#########wordcloud#########
# input a txt file of our words here instead of a new hope

# takes list of strings
# outputs wordclouds
def buildWordcloud(t):
    samp = t
    text = " ".join(samp)
    # use the reddit picture i send you here, only png works i think
    alice_coloring = np.array(Image.open("redditicon.png"))
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
    #makes the picture bigger
    plt.figure( figsize=(20,10) )
    #gives the wordcloud the same colors as pictures
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.show()


# buildWordcloud(usNews_titles)
# buildWordcloud(worldNews_titles)
#
# buildWordcloud(before_trump_titles_only)
# buildWordcloud(after_trump_titles_only)

#####barplot########

def getTopN(d, n):
    temp = dict(Counter(d).most_common(n))
    keylist = list()
    freqlist = list()
    for k in temp:
        keylist.append(k)
        freqlist.append(temp[k])
    return keylist, freqlist


def barplot(names, freqs, title):
    x_pos = np.arange(len(names))
    plt.figure(figsize=(20, 10))
    plt.bar(x_pos, freqs, color='#FFC222', align='center', alpha=0.5, width=.5)
    plt.xticks(x_pos, names)
    plt.ylabel('Frequency')
    plt.title(title)
    plt.show()

usNames, usFreq = getTopN(usLSA,15)
barplot(usNames,usFreq,"US Top 15 Title Frequencies")

worldNames, worldFreq = getTopN(worldLSA,15)
barplot(worldNames,worldFreq,"World Top 15 Title Frequencies")

beforeTrumpNames, beforeTrumpFreq = getTopN(beforeTrumpLSA,15)
barplot(beforeTrumpNames,beforeTrumpFreq,"Before Trump (US) Top 15 Title Frequencies")

afterTrumpNames, afterTrumpFreq = getTopN(afterTrumpLSA,15)
barplot(afterTrumpNames,afterTrumpFreq,"After Trump (US) Top 15 Title Frequencies")

# Step 5 (Bonus): Comment stuff AND/OR title classifications unsupervised

