import pathlib
import unittest

from py_arg.abstract_argumentation.semantics.acceptance_strategy import \
    AcceptanceStrategy
from py_arg.experiments.experiment_get_accepted_arguments import \
    get_accepted_formulas_for_file

RESOURCE_DIR = pathlib.Path.cwd() / 'resources'


class TestASPICAcceptedArguments(unittest.TestCase):
    def test_example_file(self):
        file_path = str(RESOURCE_DIR / 'aspic_lp_example.lp')
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'democratic_last_link', 'Complete',
            AcceptanceStrategy.SKEPTICAL)
        self.assertEqual(py_arg_result, ['a', 'b', 'c', 'x', 'y', 'z'])

        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'elitist_last_link', 'Complete',
            AcceptanceStrategy.SKEPTICAL)
        self.assertEqual(py_arg_result, ['a', 'b', 'c', 'nx', 'x', 'y', 'z'])

    def test_with_support_cycle(self):
        file_path = str(RESOURCE_DIR / 'aspic_support_cycle.lp')
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'democratic_last_link', 'Complete',
            AcceptanceStrategy.SKEPTICAL)
        self.assertEqual(py_arg_result, ['a', 'b', 'c'])
