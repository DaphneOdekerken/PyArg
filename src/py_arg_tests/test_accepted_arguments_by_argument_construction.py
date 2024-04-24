import pathlib
import unittest

from py_arg.experiments.experiment_get_accepted_arguments import \
    get_accepted_formulas_for_file

RESOURCE_DIR = pathlib.Path.cwd() / 'resources'


class TestASPICAcceptedArguments(unittest.TestCase):
    def test_example_file(self):
        file_path = str(RESOURCE_DIR / 'aspic_lp_example.lp')
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'democratic_last_link', 'Complete', 'skeptical')
        self.assertEqual(py_arg_result, ['a', 'b', 'c', 'x', 'y', 'z'])

        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'elitist_last_link', 'Complete', 'skeptical')
        self.assertEqual(py_arg_result, ['a', 'b', 'c', 'nx', 'x', 'y', 'z'])

    def test_with_support_cycle(self):
        file_path = str(RESOURCE_DIR / 'aspic_support_cycle.lp')
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'democratic_last_link', 'Complete', 'skeptical')
        self.assertEqual(py_arg_result, ['a', 'b', 'c'])

    def test_no_stable_extensions(self):
        # If there are no (stable) extensions, all arguments are skeptically
        # accepted.
        file_path = str(RESOURCE_DIR / 'no_stable_extensions.lp')
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'democratic_last_link', 'Stable', 'skeptical')
        self.assertEqual(py_arg_result, ['a', 'b', 'c', 'na'])

        # For complete semantics, this is no issue.
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'democratic_last_link', 'Complete', 'skeptical')
        self.assertEqual(py_arg_result, [])
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'democratic_last_link', 'Complete', 'credulous')
        self.assertEqual(py_arg_result, ['b', 'c'])

    def test_transitivity_fix(self):
        file_path = str(RESOURCE_DIR / 'aspic_transitive_preference_test.lp')
        py_arg_result = get_accepted_formulas_for_file(
            file_path, 'elitist_last_link', 'Grounded', 'skeptical')
        self.assertEqual(py_arg_result, ['a', 'x', 'y'])
