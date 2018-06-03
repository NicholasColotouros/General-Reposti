import dataloader
import praw

reddit = praw.Reddit(client_id=dataloader.redditData['client-id'], 
                    client_secret=dataloader.redditData['client-secret'],
                    user_agent=dataloader.redditData['user-agent'])
reddit.read_only = True


def GetShitPostURL():
    print("===================")
    print(dataloader.redditData['client-id'])
    print(dataloader.redditData['client-secret'])
    print(dataloader.redditData['user-agent'])
    print("===================")
    submissions = reddit.subreddit('prequelmemes').hot(limit=10)

    for submission in submissions:
        if submission.url:
            return submission.url
    return "ERROR: unable to find a shitpost"