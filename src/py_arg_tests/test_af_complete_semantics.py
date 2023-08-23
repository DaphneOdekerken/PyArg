import unittest

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.semantics.get_complete_extensions import get_complete_extensions


class TestAFCompleteSemantics(unittest.TestCase):
    def test_af_complete_semantics(self):
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        arguments = [b, c, d]
        defeats = [Defeat(b, c), Defeat(c, d), Defeat(d, c)]
        af = AbstractArgumentationFramework('af', arguments, defeats)
        ces = get_complete_extensions(af)
        self.assertEqual(len(ces), 1)
        self.assertTrue(frozenset({b, d}) in ces)
        self.assertFalse(frozenset({b}) in ces)
