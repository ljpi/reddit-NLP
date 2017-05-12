import praw
import datetime
from praw.models import MoreComments

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

resultsUS = getNews("news",1)
usNews = resultsUS[0]
usComments = resultsUS[1]

resultsWorld = getNews("worldnews",1)
worldNews = resultsWorld[0]
worldComments = resultsWorld[1]

endTime = datetime.datetime.now()

print(startTime)
print(endTime)
#10 records ~80 seconds
#100 records ~800 seconds
print((endTime-startTime).seconds)
