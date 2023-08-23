import unittest

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


class TestAFFromScratch(unittest.TestCase):
    def test_three_argument_example(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        arguments = [a, b, c]
        defeats = [Defeat(a, b), Defeat(b, a), Defeat(b, c)]
        af = AbstractArgumentationFramework('af', arguments, defeats)
        self.assertListEqual(af.get_incoming_defeat_arguments(a), [b])
        self.assertListEqual(af.get_incoming_defeat_arguments(b), [a])
        self.assertListEqual(af.get_incoming_defeat_arguments(c), [b])
