import os
import crawler
import graph
from flask import Flask, jsonify, request
import psutil

print('REDDIT_CLIENT_ID', os.environ['REDDIT_CLIENT_ID'])
print('REDDIT_CLIENT_SECRET', os.environ['REDDIT_CLIENT_SECRET'])
print('REDDIT_USER_AGENT', os.environ['REDDIT_USER_AGENT'])

app = Flask(__name__)

@app.route('/graph/<sub>')
def graph_endpoint(sub):
    """Get graph based on subreddit. ?limit=int for the number of threads to crawl"""
    limit = request.args.get('limit')
    limit = int(request.args.get('limit')) if limit else 100
    data = crawler.get_data(sub, limit=limit)
    results = graph.get_heighest_weight_neighbour(
        graph.create_graph(data), sub, 10)
    return jsonify(results)

@app.route('/healthcheck')
def healthcheck():
    """Print health information"""
    return jsonify({
        'status': 'ok',
        'cpu_percent': psutil.cpu_percent(),
        'virtual_memory': psutil.virtual_memory()
    })

@app.route('/help', methods = ['GET'])
def help():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)