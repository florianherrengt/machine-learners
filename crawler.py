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

def get_data(sub_name, limit=100):
    results = []

    for submission in reddit.subreddit(sub_name).hot(limit=limit):
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
            'sub': sub_name,
            'contributions': contributions
        })

    return results

# def save_to_file(path = 'output.json', results):
#     with open(path, 'w') as file:
#         json.dump(results, file)