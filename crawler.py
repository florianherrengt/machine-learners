import praw
import numpy as np
import json
import logging
import os


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger = logging.getLogger('prawcore')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                     user_agent=os.environ['REDDIT_USER_AGENT'])

results = []

for submission in reddit.subreddit('learnpython').hot():
    authors = np.array([])
    for comment in submission.comments.list():
        try:
            authors = np.append(authors, comment.author)
        except:
            pass
    authors = list(set(authors))
    contributions = []
    for author in authors:
        try:
            contributions.append({
                'username': author.name,
                'subs': list(set([comment.subreddit.display_name for comment in author.comments.new()]))
            })
        except:
            pass
    results.append({
        'threadId': submission.id,
        'sub': 'learnpython',
        'contributions': contributions
    })

with open('output.json', 'w') as file:
    json.dump(results, file)