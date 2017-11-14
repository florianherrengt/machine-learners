import json

import networkx as nx


def create_graph(data):
    g = nx.Graph()

    for thread in data:
        sub1 = thread['sub']
        g.add_node(sub1)
        for c in thread['contributions']:
            for sub in c['subs']:
                if sub == sub1:
                    continue
                if (sub1, sub) in g.edges():
                    data = g.get_edge_data(sub1, sub)
                    g.add_edge(sub1, sub, key='edge', weight=data['weight'] + 1)
                else:
                    g.add_edge(sub1, sub, key='edge', weight=1)
    return g


def get_heighest_weight_neighbour(graph, node, slice):
    heighest_weight_neighbour = sorted(graph[node].items(), key=lambda elem: elem[1]['weight'],
                                       reverse=True)[:slice]
    response = []
    for elem in heighest_weight_neighbour:
        heighest_weight_node = elem[0]
        heighest_weight = elem[1]['weight']
        response.append((heighest_weight_node, heighest_weight))
    return response

def sub_recommandation(g, node):
    """
    Finds the most similar node to input node for graph
    """
    node_edges = g.edges(node)
    preds = nx.jaccard_coefficient(g, node_edges)
    edge_scores = []
    for u, v, p in preds:
        edge_scores.append({'source': u, 'target': v, 'score': p})
    top_sub = sorted(edge_scores, key=lambda elem: elem['score'])[0]
    return top_sub['target'], top_sub['score']

if __name__ == '__main__':
    with open('output.json') as file:
        data = json.load(file)

    graph = create_graph(data)
    print(get_heighest_weight_neighbour(graph, 'learnpython', 10))
