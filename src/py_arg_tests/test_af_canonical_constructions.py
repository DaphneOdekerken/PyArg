import unittest

from src import py_arg as get_stable_extensions, py_arg as aux_operators, py_arg as check_incomparable, \
    py_arg as check_tight, py_arg as check_com_closed, py_arg as check_set_com_closed, py_arg as check_conf_sens, \
    py_arg as check_set_conf_sens

import src.py_arg.algorithms.canonical_constructions.canonical_af.canonical_cf as canonical_cf
import src.py_arg.algorithms.canonical_constructions.canonical_af.canonical_st as canonical_st
import src.py_arg.algorithms.canonical_constructions.canonical_af.canonical_def as canonical_def

from src.py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from src.py_arg.abstract_argumentation_classes.argument import Argument
from src.py_arg.abstract_argumentation_classes.defeat import Defeat


class TestCanonicalConstructions(unittest.TestCase):

    def test_properties(self):
        one = frozenset({'a'})
        two = frozenset({'a', 'b'})
        three = frozenset({'a', 'c'})
        four = frozenset({'b', 'c'})

        es = set({one, two, three})
        es2 = set({four, two, three})

        print('init')
        print(es)
        print('bigA')
        print(aux_operators.big_a(es))
        print('bigC')
        print(aux_operators.big_c(frozenset({'b'}), es))
        print('pairs')
        print(aux_operators.pairs(es))
        print('powerset')
        print(aux_operators.powerset(aux_operators.big_a(es)))
        print('bigP')
        print(aux_operators.big_p(es))
        print('dcl')
        print(aux_operators.dcl(es))
        print('incomparable')
        print(check_incomparable.apply(es))
        print('set_conf_sens')
        print(check_set_conf_sens.apply(es))
        print('conf_sens')
        print(check_conf_sens.apply(es))
        print('com_closed')
        print(check_com_closed.apply(es))
        print('set_com_closed')
        print(check_set_com_closed.apply(es))
        print('tight')
        print(check_tight.apply(es))

        print('tight2')
        print(check_tight.apply(es2))

    def test_construct_af(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        def1 = Defeat(a, b)
        def2 = Defeat(a, c)
        def3 = Defeat(b, c)

        af = AbstractArgumentationFramework('', arguments=[a, b, c], defeats=[def1, def2, def3])
        print(af.arguments)
        for defeat in af.defeats:
            print(defeat.from_argument.name + ' attacks ' + defeat.to_argument.name)

    def test_cf_construction(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')

        one = frozenset({})
        two = frozenset({a})
        three = frozenset({b, c})
        four = frozenset({a, c, d})

        es = set({one, two, three, four})

        af_cf = canonical_cf.apply(es)
        print(af_cf.arguments)
        for defeat in af_cf.defeats:
            print(defeat.from_argument.name + ' attacks ' + defeat.to_argument.name)

    def test_sem_stb(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        def1 = Defeat(a, b)
        def2 = Defeat(b, a)
        def3 = Defeat(b, c)

        af = AbstractArgumentationFramework('', arguments=[a, b, c], defeats=[def1, def2, def3])

        stable_ext = get_stable_extensions.get_stable_extensions(af)

        print(stable_ext)

    def test_st_construction(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')

        one = frozenset({})
        two = frozenset({a})
        three = frozenset({b, c})
        four = frozenset({a, c, d})

        es = set({one, two, three, four})

        af = canonical_st.apply(es)
        print(af.arguments)
        for defeats in af.defeats:
            print(defeats.from_argument.name + ' attacks ' + defeats.to_argument.name)

    def test_defence_formula(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')

        one = frozenset({})
        two = frozenset({a})
        three = frozenset({b, c})
        four = frozenset({a, c, d})

        es = set({one, two, three, four})

        cnf = canonical_def.defence_formula(es, a)
        dnf = canonical_def.disjunctive_defence_formula(es, a)
        print(cnf)
        print(dnf)

    def test_canonical_def(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')

        one = frozenset({})
        two = frozenset({a})
        three = frozenset({b, c})
        four = frozenset({a, c, d})

        es = set({one, two, three, four})

        af = canonical_def.apply(es)

        print(af.arguments)
        for defeat in af.defeats:
            print(defeat.from_argument.name + ' attacks ' + defeat.to_argument.name)
