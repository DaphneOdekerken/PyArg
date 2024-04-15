import unittest

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.classes.rule import Rule
from py_arg.assumption_based_argumentation.semantics import \
    get_preferred_extensions


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

        aba_framework = AssumptionBasedArgumentationFramework(assumptions,
                                                              rules, language,
                                                              contraries)
        # Get preferred extensions
        extensions = get_preferred_extensions.get_preferred_extensions(
            aba_framework)
        self.assertSetEqual(extensions,
                            {frozenset({'dirty_hands', 'no_fork'})})
