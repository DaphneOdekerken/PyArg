import unittest

from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator


class TestGenerateArgumentationSystem(unittest.TestCase):
    def test_nr_of_literals_and_rules_correct(self):
        nr_of_literals = 8
        nr_of_rules = 3
        lasg = LayeredArgumentationSystemGenerator(nr_of_literals, nr_of_rules,
                                                   rule_antecedent_distribution={1: 2, 2: 1},
                                                   literal_layer_distribution={0: 5, 1: 2, 2: 1},
                                                   strict_rule_ratio=0.4)
        arg_sys = lasg.generate()
        self.assertEqual(len(arg_sys.language), nr_of_literals)
        self.assertEqual(len(arg_sys.defeasible_rules) + len(arg_sys.strict_rules), nr_of_rules)
