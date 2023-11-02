import random
from datetime import datetime
from typing import Optional
import networkx as nx

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class AbstractArgumentationFrameworkGenerator:
    def __init__(self, nr_of_arguments: int, nr_of_defeats: int, allow_self_defeats: bool = True):
        """
        Construct a generator for making random AbstractArgumentationFramework objects.

        :param nr_of_arguments: The desired number of arguments.
        :param nr_of_defeats: The desired number of defeats.
        :param allow_self_defeats: Boolean indicating whether or not to allow self-defeats.
        """
        self.nr_of_arguments = nr_of_arguments
        self.nr_of_defeats = nr_of_defeats
        self.allow_self_defeats = allow_self_defeats

        if self.allow_self_defeats:
            if self.nr_of_defeats > self.nr_of_arguments * self.nr_of_arguments:
                raise ValueError('The number of defeats cannot be so high.')
        else:
            if self.nr_of_defeats > self.nr_of_arguments * (self.nr_of_arguments - 1):
                raise ValueError('The number of defeats cannot be so high.')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i) for i in range(self.nr_of_arguments)]

    def generate(self, name: Optional[str] = None) -> AbstractArgumentationFramework:
        """
        Generate a new AbstractArgumentationFramework.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.

        >>> generator = AbstractArgumentationFrameworkGenerator(3, 4, True)
        >>> af = generator.generate('MyAF')
        >>> len(af.arguments)
        3
        >>> len(af.defeats)
        4
        >>> af.name
        'MyAF'
        >>> generator = AbstractArgumentationFrameworkGenerator(1, 2, True)
        Traceback (most recent call last):
            ...
        ValueError: The number of defeats cannot be so high.
        >>> generator = AbstractArgumentationFrameworkGenerator(1, 1, False)
        Traceback (most recent call last):
            ...
        ValueError: The number of defeats cannot be so high.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_Generated' + datetime.now().strftime('%d/%m/%Y,%H:%M:%S')

        # Construct arguments and randomly generate defeats.
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        defeats = []
        while len(defeats) < self.nr_of_defeats:
            defeat_from = random.choice(arguments)
            defeat_to = random.choice(arguments)
            if defeat_from != defeat_to or self.allow_self_defeats:
                # Self-defeat is not a problem here
                candidate_defeat = Defeat(defeat_from, defeat_to)
                if candidate_defeat not in defeats:
                    # This is a new defeat, so we can add it.
                    defeats.append(candidate_defeat)

        return AbstractArgumentationFramework(name, arguments, defeats)
    

class ErdosRenyiGenerator:
    def __init__(self, nr_of_arguments: int, prob_edge: float, is_directed: bool = True, seed: int = None):
        self.nr_of_arguments = nr_of_arguments
        self.prob_edge = prob_edge
        self.is_directed = is_directed
        self.seed = seed
        self.last_generated_nx_graph = None

        
        if not (0 < self.prob_edge <= 1.0):
            raise ValueError('The probability for an edge must lie in the interval ]0,1]')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i) for i in range(self.nr_of_arguments)]
    
    def generate(self, name: Optional[str] = None) -> AbstractArgumentationFramework:
        """
        Generate a new random graph Erdős-Rényi graph.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_ER_Generated' + datetime.now().strftime('%d/%m/%Y,%H:%M:%S')

        erdos_reny_graph = nx.erdos_renyi_graph(self.nr_of_arguments, self.prob_edge, seed=self.seed, directed=self.is_directed)
        self.last_generated_nx_graph = erdos_reny_graph
        # Construct arguments
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        # Map node ids from networkx graph to arguments
        node_id_to_argument_map = dict(zip(sorted(erdos_reny_graph.nodes),arguments))

        defeats = [ Defeat(node_id_to_argument_map[defeat[0]],node_id_to_argument_map[defeat[1]]) for defeat in erdos_reny_graph.edges]
        
        return AbstractArgumentationFramework(name, arguments, defeats)

class WattsStrogatz:
    def __init__(self, nr_of_arguments: int, prob_edge_rewiring: float,prob_cycle: float, nr_join_neighbours: int, seed: int = None):
        self.nr_of_arguments = nr_of_arguments
        self.prob_edge_rewiring = prob_edge_rewiring
        self.prob_cycle = prob_cycle
        self.nr_join_neighbours = nr_join_neighbours
        self.seed = seed
        self.last_generated_nx_graph = None

        
        if not (0 <= self.prob_edge_rewiring <= 1.0):
            raise ValueError('The probability for rewiring an edge must lie in the interval [0,1]')
        if not (0 <= self.prob_cycle <= 1.0):
            raise ValueError('The Probability of argument being in a cycle must lie in the interval [0,1]')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i) for i in range(self.nr_of_arguments)]
    
    def generate(self, name: Optional[str] = None) -> AbstractArgumentationFramework:
        """
        Generate a Watts-Strogatz small-world graph.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_WS_Generated' + datetime.now().strftime('%d/%m/%Y,%H:%M:%S')

        watts_strogatz_graph = nx.watts_strogatz_graph(n=self.nr_of_arguments, k=self.nr_join_neighbours, p=self.prob_edge_rewiring, seed=self.seed)
        directed_edges = []
        # Choose edge direction at random
        directed_watts_strogatz_graph = generate_directed_graph(watts_strogatz_graph,directed_edges)
        self.last_generated_nx_graph = directed_watts_strogatz_graph

        edge_list = list(directed_watts_strogatz_graph.edges())
       
        # 
        enforce_prob_cycle(self.nr_of_arguments,self.prob_cycle,directed_watts_strogatz_graph, edge_list)
        
        # Construct arguments
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        # Map node ids from networkx graph to arguments
        node_id_to_argument_map = dict(zip(sorted(directed_watts_strogatz_graph.nodes),arguments))

        defeats = [ Defeat(node_id_to_argument_map[defeat[0]],node_id_to_argument_map[defeat[1]]) for defeat in watts_strogatz_graph.edges]
        
        return AbstractArgumentationFramework(name, arguments, defeats)
    

class BarabasiAlbert:
    def __init__(self, nr_of_arguments: int,  nr_attach_node_to: int,prob_cycle: float, seed: int = None):
        self.nr_of_arguments = nr_of_arguments
        self.prob_cycle = prob_cycle
        self.nr_attach_node_to = nr_attach_node_to
        self.seed = seed
        self.last_generated_nx_graph = None

        
        if not (0 <= self.prob_cycle <= 1.0):
            raise ValueError('The Probability of argument being in a cycle must lie in the interval [0,1]')

        

        if not self.nr_attach_node_to >=1 and self.nr_attach_node_to < self.nr_of_arguments:
            raise ValueError('Barabási–Albert network must have nr_attach_node_to >= 1 and nr_attach_node_to < nr_of_arguments')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i) for i in range(self.nr_of_arguments)]
    
    def generate(self, name: Optional[str] = None) -> AbstractArgumentationFramework:
        """
        Generate a Watts-Strogatz small-world graph.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_BA_Generated' + datetime.now().strftime('%d/%m/%Y,%H:%M:%S')

        barabasi_albert_graph = nx.barabasi_albert_graph(n=self.nr_of_arguments, m=self.nr_attach_node_to, seed=self.seed)
        directed_edges = []
        # Choose edge direction at random
        directed_barabasi_albert_graph = generate_directed_graph(barabasi_albert_graph, directed_edges)
        self.last_generated_nx_graph = directed_barabasi_albert_graph

        edge_list = list(directed_barabasi_albert_graph.edges())
       
        # 
        enforce_prob_cycle(self.nr_of_arguments,self.prob_cycle,directed_barabasi_albert_graph, edge_list)
        
        # Construct arguments
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        # Map node ids from networkx graph to arguments
        node_id_to_argument_map = dict(zip(sorted(directed_barabasi_albert_graph.nodes),arguments))

        defeats = [ Defeat(node_id_to_argument_map[defeat[0]],node_id_to_argument_map[defeat[1]]) for defeat in barabasi_albert_graph.edges]
        
        return AbstractArgumentationFramework(name, arguments, defeats)

def enforce_prob_cycle(nr_of_arguments,prob_cycle, graph, edge_list):
    while nx.number_strongly_connected_components(graph) >= nr_of_arguments * (1.00 - prob_cycle):
        edge = random.choice(edge_list)
        if (edge[1],edge[0]) in graph.edges:
            continue
        graph.add_edge(edge[1],edge[0])

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

