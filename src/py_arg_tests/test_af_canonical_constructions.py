import unittest

import py_arg.abstract_argumentation.semantics.get_stable_extensions as \
    get_stable_extensions
import py_arg.abstract_argumentation.canonical_constructions.check_com_closed \
    as check_com_closed
import py_arg.abstract_argumentation.canonical_constructions.\
    check_set_com_closed as check_set_com_closed
import py_arg.abstract_argumentation.canonical_constructions.\
    check_set_conf_sens as check_set_conf_sens

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_cf import get_canonical_cf_framework
from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_def import conjunctive_defense_formula, \
    disjunctive_defence_formula, get_canonical_def_framework
from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_st import get_canonical_st_framework
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_conflict_sensitive, is_tight

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.canonical_constructions import \
    aux_operators


class TestCanonicalConstructions(unittest.TestCase):
    def test_properties(self):
        one = frozenset({'a'})
        two = frozenset({'a', 'b'})
        three = frozenset({'a', 'c'})
        four = frozenset({'b', 'c'})

        es = {one, two, three}
        es2 = {four, two, three}

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
        print(aux_operators.downward_closure(es))
        print('incomparable')
        print(is_incomparable(es))
        print('set_conf_sens')
        print(check_set_conf_sens.apply(es))
        print('conf_sens')
        print(is_conflict_sensitive(es))
        print('com_closed')
        print(check_com_closed.apply(es))
        print('set_com_closed')
        print(check_set_com_closed.apply(es))
        print('tight')
        print(is_tight(es))

        print('tight2')
        print(is_tight(es2))

    def test_construct_af(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        def1 = Defeat(a, b)
        def2 = Defeat(a, c)
        def3 = Defeat(b, c)

        af = AbstractArgumentationFramework('', arguments=[a, b, c],
                                            defeats=[def1, def2, def3])
        print(af.arguments)
        for defeat in af.defeats:
            print(defeat.from_argument.name + ' attacks ' +
                  defeat.to_argument.name)

    def test_cf_construction(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')

        one = frozenset({})
        two = frozenset({a})
        three = frozenset({b, c})
        four = frozenset({a, c, d})

        es = {one, two, three, four}

        af_cf = get_canonical_cf_framework(es)
        print(af_cf.arguments)
        for defeat in af_cf.defeats:
            print(defeat.from_argument.name + ' attacks ' +
                  defeat.to_argument.name)

    def test_sem_stb(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        def1 = Defeat(a, b)
        def2 = Defeat(b, a)
        def3 = Defeat(b, c)

        af = AbstractArgumentationFramework('', arguments=[a, b, c],
                                            defeats=[def1, def2, def3])

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

        es = {one, two, three, four}

        af = get_canonical_st_framework(es)
        print(af.arguments)
        for defeats in af.defeats:
            print(defeats.from_argument.name + ' attacks ' +
                  defeats.to_argument.name)

    def test_defence_formula(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')

        one = frozenset({})
        two = frozenset({a})
        three = frozenset({b, c})
        four = frozenset({a, c, d})

        es = {one, two, three, four}

        cnf = conjunctive_defense_formula(es, a)
        dnf = disjunctive_defence_formula(es, a)
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

        es = {one, two, three, four}

        af = get_canonical_def_framework(es)

        print(af.arguments)
        for defeat in af.defeats:
            print(defeat.from_argument.name + ' attacks ' +
                  defeat.to_argument.name)
