import unittest

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework


a = Argument('a')
b = Argument('b')
c = Argument('c')
d = Argument('d')
e = Argument('e')
ab = Defeat(a, b)
bc = Defeat(b, c)
cb = Defeat(c, b)
dc = Defeat(d, c)
de = Defeat(d, e)
ed = Defeat(e, d)
iaf = IncompleteArgumentationFramework(
    arguments=[b, c, e],
    uncertain_arguments=[a, d],
    defeats=[ab, bc, dc, de, ed],
    uncertain_defeats=[cb]
)


class TestCertainProjection(unittest.TestCase):
    def test_ac_example(self):
        certain_projection = iaf.certain_projection
        self.assertEqual(certain_projection,
                         AbstractArgumentationFramework(
                             arguments=[b, c, e],
                             defeats=[bc]
                         ))


class TestCompletions(unittest.TestCase):
    def test_ac_example_4(self):
        all_completions = iaf.get_all_completions()
        self.assertEqual(len(all_completions), 8)
        af1 = AbstractArgumentationFramework(
            arguments=[a, b, c, d, e],
            defeats=[ab, bc, cb, dc, de, ed]
        )
        self.assertIn(af1, all_completions)
        af2 = AbstractArgumentationFramework(
            arguments=[a, b, c, e],
            defeats=[ab, bc, cb]
        )
        self.assertIn(af2, all_completions)
        af3 = AbstractArgumentationFramework(
            arguments=[a, b, c, d, e],
            defeats=[ab, bc, dc, de, ed]
        )
        self.assertIn(af3, all_completions)
        af4 = AbstractArgumentationFramework(
            arguments=[a, b, c, e],
            defeats=[ab, bc]
        )
        self.assertIn(af4, all_completions)
        af5 = AbstractArgumentationFramework(
            arguments=[b, c, d, e],
            defeats=[bc, cb, dc, de, ed]
        )
        self.assertIn(af5, all_completions)
        af6 = AbstractArgumentationFramework(
            arguments=[b, c, e],
            defeats=[bc, cb]
        )
        self.assertIn(af6, all_completions)
        af7 = AbstractArgumentationFramework(
            arguments=[b, c, d, e],
            defeats=[bc, dc, de, ed]
        )
        self.assertIn(af7, all_completions)
        af8 = AbstractArgumentationFramework(
            arguments=[b, c, e],
            defeats=[bc]
        )
        self.assertIn(af8, all_completions)


class TestPartialCompletions(unittest.TestCase):
    def test_ac_example_9(self):
        all_partial_completions = iaf.get_all_partial_completions()

        self.assertEqual(len(all_partial_completions), 27)
        self.assertIn(iaf, all_partial_completions)
        iaf1 = IncompleteArgumentationFramework(
            arguments=[a, b, c, d, e],
            uncertain_arguments=[],
            defeats=[ab, bc, cb, dc, de, ed],
            uncertain_defeats=[]
        )
        self.assertIn(iaf1, all_partial_completions)

        cert_iaf1 = iaf1.certain_projection
        self.assertEqual(cert_iaf1, AbstractArgumentationFramework(
            arguments=[a, b, c, d, e], defeats=[ab, bc, cb, dc, de, ed]))

        iaf2 = IncompleteArgumentationFramework(
            arguments=[b, c, e],
            uncertain_arguments=[],
            defeats=[bc],
            uncertain_defeats=[]
        )
        self.assertIn(iaf2, all_partial_completions)

        cert_iaf2 = iaf2.certain_projection
        self.assertEqual(cert_iaf2, AbstractArgumentationFramework(
            arguments=[b, c, e], defeats=[bc]))

        iaf3 = IncompleteArgumentationFramework(
            arguments=[a, b, c, e],
            uncertain_arguments=[d],
            defeats=[ab, bc, dc, de, ed],
            uncertain_defeats=[cb]
        )
        self.assertIn(iaf3, all_partial_completions)
        cert_iaf3 = iaf3.certain_projection
        self.assertEqual(cert_iaf3, AbstractArgumentationFramework(
            arguments=[a, b, c, e], defeats=[ab, bc]))
