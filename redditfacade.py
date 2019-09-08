import dataloader
import praw
import re

from prawcore import NotFound
from random import randint

subreddit_regex_format = r"^((/?r/)?[a-z]+)$"

reddit = praw.Reddit(client_id=dataloader.reddit_data['client-id'], 
                    client_secret=dataloader.reddit_data['client-secret'],
                    user_agent=dataloader.reddit_data['user-agent'])
reddit.read_only = True

def strip_subreddit_prefix(subreddit : str):
    return subreddit.split(r"/")[-1]

def subreddit_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists

def get_shitpost(subreddit : str):
    stripped_subreddit = strip_subreddit_prefix(subreddit)
    submissions = reddit.subreddit(stripped_subreddit).hot(limit=25)

    shitpost_number = randint(0, 9)
    last_valid_shitpost = ("ERROR: ", "Unable to find shitpost")
    for submission in submissions:
        if submission.url:
            if shitpost_number > 0:
                shitpost_number = shitpost_number - 1
                last_valid_shitpost = (submission.title, submission.url)
            else:
                return last_valid_shitpost
    return last_valid_shitpost

def is_valid_subreddit(subreddit : str):
    return re.match(subreddit_regex_format, subreddit, re.IGNORECASE)
