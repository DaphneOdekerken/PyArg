from datetime import datetime
from typing import Optional

import networkx as nx

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.generators.\
    abstract_argumentation_framework_generator import ALPHABET
from py_arg.abstract_argumentation.generators.generate_directed_graph import \
    generate_directed_graph
from py_arg.abstract_argumentation.generators.enforce_prob_cycle import \
    enforce_prob_cycle


class BarabasiAlbert:
    """
    Implementation based on networkx of:
    Albert-László Barabási, and Réka Albert. "Emergence of scaling in random
    networks." science 286.5439 (1999): 509-512.
    """
    def __init__(self, nr_of_arguments: int, nr_attach_node_to: int,
                 prob_cycle: float, seed: int = None):
        self.nr_of_arguments = nr_of_arguments
        self.prob_cycle = prob_cycle
        self.nr_attach_node_to = nr_attach_node_to
        self.seed = seed
        self.last_generated_nx_graph = None

        if not (0 <= self.prob_cycle <= 1.0):
            raise ValueError('The Probability of argument being in a cycle '
                             'must lie in the interval [0,1]')

        if not self.nr_attach_node_to >= 1 and \
                self.nr_attach_node_to < self.nr_of_arguments:
            raise ValueError(
                'Barabási–Albert network must have nr_attach_node_to >= 1 and '
                'nr_attach_node_to < nr_of_arguments')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i)
                                   for i in range(self.nr_of_arguments)]

    def generate(self, name: Optional[str] = None) -> \
            AbstractArgumentationFramework:
        """
        Generate a Barabasi-Albert graph.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_BA_Generated' + \
                   datetime.now().strftime('%d/%m/%Y,%H:%M:%S')

        barabasi_albert_graph = nx.barabasi_albert_graph(
            n=self.nr_of_arguments, m=self.nr_attach_node_to,
            seed=self.seed)
        directed_edges = []
        # Choose edge direction at random
        directed_barabasi_albert_graph = generate_directed_graph(
            barabasi_albert_graph, directed_edges)
        self.last_generated_nx_graph = directed_barabasi_albert_graph

        edge_list = list(directed_barabasi_albert_graph.edges())

        #
        enforce_prob_cycle(self.nr_of_arguments, self.prob_cycle,
                           directed_barabasi_albert_graph, edge_list)

        # Construct arguments
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        # Map node ids from networkx graph to arguments
        node_id_to_argument_map = dict(zip(sorted(
            directed_barabasi_albert_graph.nodes), arguments))

        defeats = [Defeat(node_id_to_argument_map[defeat[0]],
                          node_id_to_argument_map[defeat[1]]) for defeat in
                   barabasi_albert_graph.edges]

        return AbstractArgumentationFramework(name, arguments, defeats)
