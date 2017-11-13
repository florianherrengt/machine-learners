import praw
import sys
import numpy as np
import json
import logging
import os
from tqdm import tqdm


# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# logger = logging.getLogger('prawcore')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(handler)

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
                    # 'threads': list(set([comment. for comment in author.comments.new()]))
                })
            except:
                pass
        results.append({
            'threadId': submission.id,
            'sub': sub_name,
            'contributions': contributions
        })

    return results

def save_to_file(results, path='output.json'):
    with open(path, 'w') as file:
        json.dump(results, file)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        raise Exception('You need to pass a sub as first argument')
    sub = sys.argv[1]
    if (sub is None):
        raise Exception('You need to pass a sub as first argument')

    save_to_file(get_data(sub))