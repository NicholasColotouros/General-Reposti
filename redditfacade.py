import dataloader
import praw
import re

from random import randint

reddit = praw.Reddit(client_id=dataloader.redditData['client-id'], 
                    client_secret=dataloader.redditData['client-secret'],
                    user_agent=dataloader.redditData['user-agent'])
reddit.read_only = True


def GetShitpost():
    submissions = reddit.subreddit('prequelmemes').hot(limit=25)

    shitpostNumber = randint(0, 9)
    for submission in submissions:
        if submission.url: # no self posts
            if shitpostNumber > 0:
                shitpostNumber = shitpostNumber - 1
            else:
                return (submission.title, submission.url)
    return "ERROR: unable to find a shitpost"