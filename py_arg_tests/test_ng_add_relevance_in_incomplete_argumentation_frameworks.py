import unittest

from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.incomplete_argumentation_classes.argument_incomplete_argumentation_framework import \
    ArgumentIncompleteArgumentationFramework
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.relevance import \
    get_relevant_uncertain_arguments_for_adding_to_ng


class TestRelevanceInIncompleteArgumentationFrameworks(unittest.TestCase):
    def test1(self):
        arguments = {name: Argument(name) for name in 'ABCD'}
        defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['AB', 'BA', 'BC', 'CB', 'DB']]
        certain_arguments = [argument for name, argument in arguments.items() if name in 'AB']
        uncertain_arguments = [argument for name, argument in arguments.items() if name in 'CD']
        iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
        relevant_arguments = get_relevant_uncertain_arguments_for_adding_to_ng(arguments['A'], iac)
        self.assertNotIn(arguments['A'], relevant_arguments)
        self.assertNotIn(arguments['C'], relevant_arguments)
        self.assertIn(arguments['D'], relevant_arguments)

    def test2(self):
        arguments = {name: Argument(name) for name in 'ABCDE'}
        defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['AB', 'BA', 'CB', 'CD', 'DC', 'ED']]
        certain_arguments = [argument for name, argument in arguments.items() if name in 'ABD']
        uncertain_arguments = [argument for name, argument in arguments.items() if name in 'CE']
        iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
        relevant_arguments = get_relevant_uncertain_arguments_for_adding_to_ng(arguments['A'], iac)
        self.assertNotIn(arguments['A'], relevant_arguments)
        self.assertNotIn(arguments['B'], relevant_arguments)
        self.assertIn(arguments['C'], relevant_arguments)
        self.assertNotIn(arguments['D'], relevant_arguments)
        self.assertIn(arguments['E'], relevant_arguments)

    def test3(self):
        arguments = {name: Argument(name) for name in 'ABCDE'}
        defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['AB', 'BA', 'CB', 'CD', 'DC', 'ED']]
        certain_arguments = [argument for name, argument in arguments.items() if name in 'ABC']
        uncertain_arguments = [argument for name, argument in arguments.items() if name in 'DE']
        iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
        relevant_arguments = get_relevant_uncertain_arguments_for_adding_to_ng(arguments['A'], iac)
        self.assertNotIn(arguments['A'], relevant_arguments)
        self.assertNotIn(arguments['B'], relevant_arguments)
        self.assertNotIn(arguments['C'], relevant_arguments)
        self.assertNotIn(arguments['D'], relevant_arguments)
        self.assertIn(arguments['E'], relevant_arguments)

    def test4(self):
        arguments = {name: Argument(name) for name in 'ABCD'}
        defeats = [Defeat(arguments[t[0]], arguments[t[1]]) for t in ['AB', 'BA', 'CB', 'CD', 'DC']]
        certain_arguments = [argument for name, argument in arguments.items() if name in 'ABD']
        uncertain_arguments = [argument for name, argument in arguments.items() if name in 'C']
        iac = ArgumentIncompleteArgumentationFramework('', certain_arguments, uncertain_arguments, defeats)
        relevant_arguments = get_relevant_uncertain_arguments_for_adding_to_ng(arguments['A'], iac)
        self.assertNotIn(arguments['A'], relevant_arguments)
        self.assertNotIn(arguments['B'], relevant_arguments)
        self.assertNotIn(arguments['C'], relevant_arguments)
        self.assertNotIn(arguments['D'], relevant_arguments)
