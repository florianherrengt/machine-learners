# Reddit recommendation

## Getting started

### Generate dataset

`REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... REDDIT_USER_AGENT=... python crawler.py`

### Show the graph

`python graph.py`

## Server

https://lit-forest-34240.herokuapp.com

`REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... REDDIT_USER_AGENT=... FLASK_APP=server.py FLASK_DEBUG=1 flask run -h 0.0.0.0`

Then go to `http://0.0.0.0:5000/help`