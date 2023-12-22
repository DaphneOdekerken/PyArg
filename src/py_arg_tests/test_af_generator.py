import unittest
import networkx as nx

from py_arg.abstract_argumentation.generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg.abstract_argumentation.generators.barbasi_albert_generator import BarabasiAlbert
from py_arg.abstract_argumentation.generators.watts_strogatz_generator import WattsStrogatz
from py_arg.abstract_argumentation.generators.erdos_renyi_generator import ErdosRenyiGenerator


class TestAFGenerator(unittest.TestCase):
    def test_af_generator(self):
        generator = AbstractArgumentationFrameworkGenerator(3, 3, True)
        af = generator.generate()
        self.assertEqual(len(af.arguments), 3)
        self.assertEqual(len(af.defeats), 3)

    def test_erdos_renyi_generator(self):
        generator = ErdosRenyiGenerator(nr_of_arguments=10, prob_edge=0.5, is_directed=True, seed=42)
        af = generator.generate()
        print(generator.last_generated_nx_graph)
        self.assertEqual(len(af.arguments), 10)
        self.assertEqual(len(af.defeats), 46)
        # self.assertEqual(nx.is_directed(generator.last_generated_nx_graph),True)

    def test_wats_strogatz_generator(self):
        generator = WattsStrogatz(nr_of_arguments=10, nr_join_neighbours=5, prob_edge_rewiring=0.5, seed=42,
                                  prob_cycle=0.8)
        af = generator.generate()
        self.assertEqual(len(af.arguments), 10)
        self.assertEqual(len(af.defeats), 20)
        self.assertEqual(nx.is_directed(generator.last_generated_nx_graph), True)

    def test_wats_barabasi_albert_generator(self):
        generator = BarabasiAlbert(nr_of_arguments=10, nr_attach_node_to=5, seed=42, prob_cycle=0.8)
        af = generator.generate()
        self.assertEqual(len(af.arguments), 10)
        self.assertEqual(len(af.defeats), 25)
        self.assertEqual(nx.is_directed(generator.last_generated_nx_graph), True)
