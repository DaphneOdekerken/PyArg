import random

import networkx as nx


def enforce_prob_cycle(nr_of_arguments, prob_cycle, graph, edge_list):
    while nx.number_strongly_connected_components(graph) >= nr_of_arguments * \
            (1.00 - prob_cycle):
        edge = random.choice(edge_list)
        if (edge[1], edge[0]) in graph.edges:
            continue
        graph.add_edge(edge[1], edge[0])
