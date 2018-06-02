import praw

reddit = praw.Reddit(client_id='CLIENT_ID', client_secret="CLIENT_SECRET",
                     password='PASSWORD', user_agent='USERAGENT',
                     username='USERNAME')
reddit.read_only = True

def shitpost():
    submissions = reddit.subreddit('prequelmemes').hot(limit=10)

    for submission in submissions:
        if submission.url:
            return submission.url
    return "ERROR: unable to find a shitpost"