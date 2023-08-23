import unittest

from py_arg.aba_classes.rule import Rule
from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes.semantics import get_preferred_extensions


class TestABALasagneExample(unittest.TestCase):
    def test_aba_lasagne_example(self):
        language = {'happy',
                    'eating',
                    'good_food',
                    'not_eating',
                    'no_fork',
                    'dirty_hands',
                    'fork',
                    'clean_hands'}
        rules = {Rule('Rule1', {'good_food', 'eating'}, 'happy'),
                 Rule('Rule2', set(), 'good_food'),
                 Rule('Rule3', {'no_fork', 'dirty_hands'}, 'not_eating')}
        assumptions = {'eating', 'no_fork', 'dirty_hands'}
        contraries = {'eating': 'not_eating',
                      'no_fork': 'fork',
                      'dirty_hands': 'clean_hands'}

        aba_framework = ABAF(assumptions, rules, language, contraries)
        # Get preferred extensions
        extensions = get_preferred_extensions.apply(aba_framework)
        self.assertSetEqual(extensions, {frozenset({'dirty_hands', 'no_fork'})})