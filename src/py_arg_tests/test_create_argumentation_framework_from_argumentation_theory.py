import unittest

from py_arg_tests.modgil_prakken_aij_tests import get_argumentation_theory


class TestArgumentationFrameworkFromArgumentationTheory(unittest.TestCase):
    def test_get_nr_of_arguments(self):
        arg_theory = get_argumentation_theory()
        af = arg_theory.create_abstract_argumentation_framework('af')
        self.assertEqual(len(af.arguments), 8)

    def test_get_nr_of_defeats(self):
        arg_theory = get_argumentation_theory()
        af = arg_theory.create_abstract_argumentation_framework('af')
        self.assertEqual(len(af.defeats), 5)

    def test_get_nr_of_attacks(self):
        arg_theory = get_argumentation_theory(include_d=True, include_e=True)
        saf = arg_theory.create_structured_argumentation_framework('af')
        self.assertEqual(len(saf.attacks), 10)

    def test_get_argumentation_framework(self):
        arg_theory = get_argumentation_theory()
        af = arg_theory.create_abstract_argumentation_framework('af')
        arg_for_r = af.get_argument('r (ordinary premise)')
        self.assertEqual(arg_for_r.name, 'r (ordinary premise)')
        defeaters_of_r = af.get_incoming_defeat_arguments(arg_for_r)
        self.assertEqual(len(defeaters_of_r), 1)
        self.assertEqual(defeaters_of_r[0].name, '-r (ordinary premise)')
        defeated_by_r = af.get_incoming_defeat_arguments(arg_for_r)
        self.assertEqual(len(defeated_by_r), 1)
        self.assertEqual(defeated_by_r[0].name, '-r (ordinary premise)')
        arg_for_not_r = af.get_argument('-r (ordinary premise)')
        defeated_by_not_r = af.get_outgoing_defeat_arguments(arg_for_not_r)
        self.assertEqual(len(defeated_by_not_r), 3)
