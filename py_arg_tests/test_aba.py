import unittest

from typing import Set, FrozenSet

from py_arg.aba_classes.rule import Rule, Atom
from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes.instantiated_argument import InstantiatedArgument
from py_arg.abstract_argumentation_classes import argument, defeat, abstract_argumentation_framework

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


class TestABA(unittest.TestCase):

    def test_instantiation(self):
        a = Atom('a')
        a_c = Atom('a_c')
        b = Atom('b')
        b_c = Atom('b_c')
        c = Atom('c')
        c_c = Atom('c_c')
        d = Atom('d')
        d_c = Atom('d_c')
        p = Atom('p')
        q = Atom('q')
        s = Atom('s')
        t = Atom('t')

        assumptions = {a, b, c, d}
        atoms = {a, a_c, b, b_c, c, c_c, d, d_c, p, q, s, t}
        contraries = {a: a_c, b: b_c, c: c_c, d: d_c}

        r_1 = Rule('', {p}, a_c)
        r_2 = Rule('', {q, s, b}, p)
        r_3 = Rule('', {c}, s)
        r_4 = Rule('', {d}, s)
        r_5 = Rule('', set(), q)
        rules = {r_1, r_2, r_3, r_4, r_5}

        aba = ABAF(assumptions, rules, atoms, contraries)
        af = aba.generate_af()

        a_to_a = InstantiatedArgument('', {a}, a)
        b_to_b = InstantiatedArgument('', {b}, b)
        c_to_c = InstantiatedArgument('', {c}, c)
        d_to_d = InstantiatedArgument('', {d}, d)
        bc_to_a_c = InstantiatedArgument('', {b, c}, a_c)
        bd_to_a_c = InstantiatedArgument('', {b, d}, a_c)
        expected_args = {a_to_a, b_to_b, c_to_c, d_to_d, bc_to_a_c, bd_to_a_c}

        d1 = Defeat(bc_to_a_c, a_to_a)
        d2 = Defeat(bd_to_a_c, a_to_a)
        expected_defeats = {d1, d2}

        self.assertEqual(set(af.arguments), expected_args)
        self.assertEqual(set(af.defeats), expected_defeats)