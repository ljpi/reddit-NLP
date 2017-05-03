import praw

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
for submission in reddit.subreddit('USNEWS').top(limit=10):
    print(submission.title)


print("World News Top 10 All Time")
for submission in reddit.subreddit('worldnews').top(limit=10):
    print(submission.title)