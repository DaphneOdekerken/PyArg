import unittest

from typing import Set, FrozenSet

from py_arg.aba_classes.rule import Rule, Atom
from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes import instantiated_argument
from py_arg.abstract_argumentation_classes import argument, defeat, abstract_argumentation_framework

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat

import py_arg.aba_classes


class TestCanonicalConstructions(unittest.TestCase):

    def test_properties(self):
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

        aba.generate_af()
