from datetime import datetime
from typing import Optional

import networkx as nx

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.generators.\
    abstract_argumentation_framework_generator import ALPHABET
from py_arg.abstract_argumentation.generators.enforce_prob_cycle import \
    enforce_prob_cycle
from py_arg.abstract_argumentation.generators.generate_directed_graph import \
    generate_directed_graph


class WattsStrogatz:
    def __init__(self, nr_of_arguments: int, prob_edge_rewiring: float,
                 prob_cycle: float, nr_join_neighbours: int,
                 seed: int = None):
        self.nr_of_arguments = nr_of_arguments
        self.prob_edge_rewiring = prob_edge_rewiring
        self.prob_cycle = prob_cycle
        self.nr_join_neighbours = nr_join_neighbours
        self.seed = seed
        self.last_generated_nx_graph = None

        if not (0 <= self.prob_edge_rewiring <= 1.0):
            raise ValueError(
                'The probability for rewiring an edge must lie in the interval'
                ' [0,1]')
        if not (0 <= self.prob_cycle <= 1.0):
            raise ValueError(
                'The Probability of argument being in a cycle must lie in the '
                'interval [0,1]')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i) for i in
                                   range(self.nr_of_arguments)]

    def generate(self,
                 name: Optional[str] = None) -> AbstractArgumentationFramework:
        """
        Generate a Watts-Strogatz small-world graph.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_WS_Generated' + datetime.now().strftime(
                '%d/%m/%Y,%H:%M:%S')

        watts_strogatz_graph = nx.watts_strogatz_graph(
            n=self.nr_of_arguments, k=self.nr_join_neighbours,
            p=self.prob_edge_rewiring, seed=self.seed)
        directed_edges = []
        # Choose edge direction at random
        directed_watts_strogatz_graph = generate_directed_graph(
            watts_strogatz_graph, directed_edges)
        self.last_generated_nx_graph = directed_watts_strogatz_graph

        edge_list = list(directed_watts_strogatz_graph.edges())

        #
        enforce_prob_cycle(self.nr_of_arguments, self.prob_cycle,
                           directed_watts_strogatz_graph, edge_list)

        # Construct arguments
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        # Map node ids from networkx graph to arguments
        node_id_to_argument_map = dict(
            zip(sorted(directed_watts_strogatz_graph.nodes), arguments))

        defeats = [Defeat(node_id_to_argument_map[defeat[0]],
                          node_id_to_argument_map[defeat[1]]) for defeat in
                   watts_strogatz_graph.edges]

        return AbstractArgumentationFramework(name, arguments, defeats)
