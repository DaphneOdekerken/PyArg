import unittest

import src.py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_st as canonical_st

from src.py_arg.aba_classes.rule import Rule


class TestCanonicalConstructions(unittest.TestCase):

    def test_canonical_stb(self):
        a = 'a'
        b = 'b'
        c = 'c'
        a_c = 'a_c'
        b_c = 'b_c'
        c_c = 'c_c'
        x_a = 'x_a'
        x_b = 'x_b'
        x_c = 'x_c'
        x_a_c = 'x_a_c'
        x_b_c = 'x_b_c'
        x_c_c = 'x_c_c'

        set_empty = frozenset({})
        set_a = frozenset({a})
        set_b = frozenset({b})
        set_c = frozenset({c})
        set_ab = frozenset({a, b})
        set_ac = frozenset({a, c})
        set_bc = frozenset({b, c})
        set_abc = frozenset({a, b, c})

        es1 = {set_ab, set_ac, set_bc}
        canonical_aba1 = canonical_st.apply(es1)

        self.assertEqual(canonical_aba1.assumptions, {a, b, c})
        self.assertEqual(canonical_aba1.language, {a, b, c, a_c, b_c, c_c})
        self.assertEqual(canonical_aba1.rules, {Rule('', {a, b}, c_c), Rule('', {a, c}, b_c), Rule('', {b, c}, a_c)})
        self.assertEqual(canonical_aba1.contraries, {a: a_c, b: b_c, c: c_c})

