import unittest

from src.py_arg_tests.modgil_prakken_aij_tests import get_argumentation_theory


class TestRecomputeArguments(unittest.TestCase):
    def test_nr_arguments_update(self):
        arg_theory = get_argumentation_theory()
        self.assertEqual(len(arg_theory.all_arguments), 8)
        old_ordinary_premises = arg_theory.knowledge_base_ordinary_premises.copy()

        # Add -a to the ordinary premises.
        arg_theory.add_to_knowledge_base_ordinary_premises(arg_theory.argumentation_system.language['-a'])
        self.assertEqual(len(arg_theory.all_arguments), 9)

        # Go back to the old situation.
        arg_theory.knowledge_base_ordinary_premises = old_ordinary_premises
        self.assertEqual(len(arg_theory.all_arguments), 8)
