# import unittest
#
# from py_arg.abstract_argumentation_classes.argument import Argument
# from py_arg.incomplete_argumentation_classes.argument_incomplete_argumentation_framework import \
#     ArgumentIncompleteArgumentationFramework
# from py_arg.abstract_argumentation_classes.defeat import Defeat
# from py_arg.algorithms.relevance import \
#     get_relevant_uncertain_arguments_for_removing_from_pg
#
#
# class TestRelevanceInIncompleteArgumentationFrameworks(unittest.TestCase):
#     def test1(self):
#         arguments = {name: Argument(name) for name in 'ABC'}
#         defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['AB', 'BA', 'CB']]
#         certain_arguments = [argument for name, argument in arguments.items() if name in 'AC']
#         uncertain_arguments = [argument for name, argument in arguments.items() if name in 'B']
#         iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
#         relevant_arguments = get_relevant_uncertain_arguments_for_removing_from_pg(arguments['A'], iac)
#         self.assertNotIn(arguments['A'], relevant_arguments)
#         self.assertNotIn(arguments['B'], relevant_arguments)
#         self.assertNotIn(arguments['C'], relevant_arguments)
#
#     def test2(self):
#         arguments = {name: Argument(name) for name in 'ABC'}
#         defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['AB', 'BA', 'CB', 'BC']]
#         certain_arguments = [argument for name, argument in arguments.items() if name in 'AC']
#         uncertain_arguments = [argument for name, argument in arguments.items() if name in 'B']
#         iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
#         relevant_arguments = get_relevant_uncertain_arguments_for_removing_from_pg(arguments['A'], iac)
#         self.assertNotIn(arguments['A'], relevant_arguments)
#         self.assertIn(arguments['B'], relevant_arguments)
#         self.assertNotIn(arguments['C'], relevant_arguments)
#
#     def test3(self):
#         arguments = {name: Argument(name) for name in 'ABCD'}
#         defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['BA', 'CB', 'DC']]
#         certain_arguments = [argument for name, argument in arguments.items() if name in 'AC']
#         uncertain_arguments = [argument for name, argument in arguments.items() if name in 'BD']
#         iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
#         relevant_arguments = get_relevant_uncertain_arguments_for_removing_from_pg(arguments['A'], iac)
#         self.assertNotIn(arguments['A'], relevant_arguments)
#         self.assertNotIn(arguments['B'], relevant_arguments)
#         self.assertNotIn(arguments['C'], relevant_arguments)
#         self.assertIn(arguments['D'], relevant_arguments)
#
#     def test4(self):
#         arguments = {name: Argument(name) for name in 'ABC'}
#         defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['AB', 'BA', 'CB']]
#         certain_arguments = [argument for name, argument in arguments.items() if name in 'A']
#         uncertain_arguments = [argument for name, argument in arguments.items() if name in 'BC']
#         iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
#         relevant_arguments = get_relevant_uncertain_arguments_for_removing_from_pg(arguments['A'], iac)
#         self.assertNotIn(arguments['A'], relevant_arguments)
#         self.assertIn(arguments['B'], relevant_arguments)
#         self.assertNotIn(arguments['C'], relevant_arguments)
