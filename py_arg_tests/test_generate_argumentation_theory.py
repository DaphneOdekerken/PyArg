# import unittest
#
# from py_arg.generators.argumentation_system_generators.layered_argumentation_system_generator import \
#     LayeredArgumentationSystemGenerator
# from py_arg.generators.argumentation_theory_generators.argumentation_theory_generator import \
#     ArgumentationTheoryGenerator
#
#
# class TestGenerateArgumentationTheory(unittest.TestCase):
#     def test_nr_of_literals_and_rules_correct(self):
#         nr_of_literals = 8
#         nr_of_rules = 3
#         lasg = LayeredArgumentationSystemGenerator(nr_of_literals, nr_of_rules,
#                                                    rule_antecedent_distribution={1: 2, 2: 1},
#                                                    literal_layer_distribution={0: 5, 1: 2, 2: 1},
#                                                    strict_rule_ratio=0.4)
#         arg_sys = lasg.generate()
#         knowledge_literal_ratio = 0.3
#         axiom_knowledge_ratio = 0.5
#         expected_knowledge_base_size = int(nr_of_literals * knowledge_literal_ratio)
#         expected_nr_of_axioms = int(axiom_knowledge_ratio * expected_knowledge_base_size)
#         expected_nr_of_ordinary_premises = expected_knowledge_base_size - expected_nr_of_axioms
#         atg = ArgumentationTheoryGenerator(arg_sys, knowledge_literal_ratio=knowledge_literal_ratio,
#                                            axiom_knowledge_ratio=axiom_knowledge_ratio)
#         arg_theory = atg.generate()
#         self.assertEqual(len(arg_theory._knowledge_base_axioms), expected_nr_of_axioms)
#         self.assertEqual(len(arg_theory._knowledge_base_ordinary_premises), expected_nr_of_ordinary_premises)
