import praw
import datetime
from praw.models import MoreComments
from textblob import TextBlob
import sys
import numpy


client_id = open("client_id").read()
client_secret = open("client_secret").read()
password = open("password").read()
user_agent = open("user_agent").read()
username = open("username").read()


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

resultsUS = getNews("news",20)
usNews = resultsUS[0]
usComments = resultsUS[1]

# resultsWorld = getNews("worldnews",1)
# worldNews = resultsWorld[0]
# worldComments = resultsWorld[1]

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

# for k in worldNews:
#     print(k)
#     title = worldNews[k][1]
#     n = TextBlob(title)
#     print(n)
#     print(n.sentiment.polarity)
#     worldSent.append(n.sentiment.polarity)

usSentAvg = sum(usSent) / float(len(usSent))
# worldSentAvg = sum(worldSent) / float(len(worldSent))

print("US")
print(usSentAvg)
print(min(usSent))
print(max(usSent))

# print("World")
# print(worldSentAvg)
# print(min(worldSent))
# print(max(worldSent))

#also get standard deviation
#and more general descriptive stats
#visualize

#Step 2: LSA

#Step 3: By Time Analysis
print(usNews)

#first do with us, then do with world
before_trump = list()
after_trump = list()
#nov 8 2016
winning_date = datetime.datetime.strptime('20161108', "%Y%m%d")
#cutoff at may 20
todays_date = datetime.datetime.strptime('20170520', "%Y%m%d")
#194 days difference between winning date and may20 = 20160428
start_date = datetime.datetime.strptime('20160428', "%Y%m%d")

print(winning_date)
print(todays_date)
print(start_date)

for news_key in usNews:
    timeStamp = (usNews[news_key][2])
    if timeStamp >= winning_date and timeStamp <= todays_date:
        #append to after trump
        after_trump.append(usNews[news_key])
    elif timeStamp >= start_date and timeStamp < winning_date:
        #append to before trump
        before_trump.append(usNews[news_key])
    #else do nothing, out of sample range

print(after_trump)
print(len(after_trump))
print(before_trump)
print(len(before_trump))

#just the titles
after_trump_titles_only=list()
for l in after_trump:
    after_trump_titles_only.append(l[1])
before_trump_titles_only=list()
for l in before_trump:
    before_trump_titles_only.append(l[1])

print(after_trump_titles_only)
print(before_trump_titles_only)

#Step 4: Visualization - Word Clouds and others
#benchmark vs random word sample

#Step 5 (Bonus): Comment stuff AND/OR title classifications unsupervised

