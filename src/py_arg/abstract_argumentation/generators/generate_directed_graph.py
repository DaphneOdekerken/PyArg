import random

import networkx as nx


def generate_directed_graph(graph, directed_edges):
    for edge in graph.edges:
        if random.choice([True, False]):
            directed_edges.append((edge[1], edge[0]))
        else:
            directed_edges.append(edge)
    directed_graph = nx.DiGraph()
    directed_graph.add_nodes_from(graph.nodes)
    directed_graph.add_edges_from(directed_edges)
    return directed_graph
