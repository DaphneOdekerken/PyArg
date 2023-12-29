from datetime import datetime
from typing import Optional

import networkx as nx

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.generators.\
    abstract_argumentation_framework_generator import ALPHABET


class ErdosRenyiGenerator:
    """
    Edgar N. Gilbert "Random graphs." The Annals of Mathematical Statistics
    30.4 (1959): 1141-1144.
    """
    def __init__(self, nr_of_arguments: int, prob_edge: float,
                 is_directed: bool = True, seed: int = None):
        self.nr_of_arguments = nr_of_arguments
        self.prob_edge = prob_edge
        self.is_directed = is_directed
        self.seed = seed
        self.last_generated_nx_graph = None

        if not (0 < self.prob_edge <= 1.0):
            raise ValueError(
                'The probability for an edge must lie in the interval ]0,1]')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i) for i in
                                   range(self.nr_of_arguments)]

    def generate(self,
                 name: Optional[str] = None) -> AbstractArgumentationFramework:
        """
        Generate a new random graph Erdős-Rényi graph.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_ER_Generated' + datetime.now().strftime(
                '%d/%m/%Y,%H:%M:%S')

        erdos_reny_graph = nx.erdos_renyi_graph(self.nr_of_arguments,
                                                self.prob_edge, seed=self.seed,
                                                directed=self.is_directed)
        self.last_generated_nx_graph = erdos_reny_graph
        # Construct arguments
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        # Map node ids from networkx graph to arguments
        node_id_to_argument_map = dict(
            zip(sorted(erdos_reny_graph.nodes), arguments))

        defeats = [Defeat(node_id_to_argument_map[defeat[0]],
                          node_id_to_argument_map[defeat[1]]) for defeat in
                   erdos_reny_graph.edges]

        return AbstractArgumentationFramework(name, arguments, defeats)
