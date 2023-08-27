import unittest

import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_st as canonical_st
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_cf as construct_abaf_cf
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_com as construct_abaf_com
from py_arg.algorithms.canonical_constructions.canonical_abaf import construct_abaf_adm
import py_arg.algorithms.canonical_constructions.check_intersection_in as check_intersection_in
import py_arg.algorithms.canonical_constructions.check_union_closed as check_union_closed
import py_arg.algorithms.canonical_constructions.check_set_com_closed as check_set_com_closed
import py_arg.algorithms.canonical_constructions.check_downward_closed as check_downward_closed
import py_arg.algorithms.canonical_constructions.aux_operators as aux

from py_arg.aba_classes.semantics import get_complete_extensions as get_complete_extensions
from py_arg.aba_classes.semantics import get_conflict_free_extensions as get_conflict_free_extensions, \
    get_stable_extensions as get_stable_extensions, get_admissible_extensions as get_admissible_extensions

from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes.instantiated_argument import InstantiatedArgument
from py_arg.aba_classes.rule import Rule

from py_arg.abstract_argumentation_classes.defeat import Defeat

import py_arg.algorithms.canonical_constructions.check_contains_empty as check_contains_empty


class TestCanonicalConstructions(unittest.TestCase):

    def test_instantiation(self):
        a = 'a'
        a_c = 'a_c'
        b = 'b'
        b_c = 'b_c'
        c = 'c'
        c_c = 'c_c'
        d = 'd'
        d_c = 'd_c'
        p = 'p'
        q = 'q'
        s = 's'
        t = 't'

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

    def test_properties(self):
        a = 'a'
        b = 'b'
        c = 'c'

        set_empty = frozenset({})
        set_a = frozenset({a})
        set_b = frozenset({b})
        set_c = frozenset({c})
        set_ab = frozenset({a, b})
        set_ac = frozenset({a, c})
        set_bc = frozenset({b, c})
        set_abc = frozenset({a, b, c})

        es1 = set()
        es1_ucl = {set_empty}
        es1_reduced = es1
        self.assertFalse(check_union_closed.apply(es1))
        self.assertEqual(aux.ucl(es1), es1_ucl)
        self.assertFalse(check_contains_empty.apply(es1))
        self.assertFalse(check_intersection_in.apply(es1))
        self.assertEqual(aux.reduce(es1), es1_reduced)
        self.assertTrue(check_downward_closed.apply(es1))

        es2 = {set_empty}
        es2_ucl = es2
        es2_reduced = es2
        self.assertTrue(check_union_closed.apply(es2))
        self.assertEqual(aux.ucl(es2), es2_ucl)
        self.assertTrue(check_contains_empty.apply(es2))
        self.assertTrue(check_intersection_in.apply(es2))
        self.assertEqual(aux.reduce(es2), es2_reduced)
        self.assertTrue(check_downward_closed.apply(es2))

        es3 = {set_ab}
        es3_ucl = {set_empty, set_ab}
        es3_reduced = {frozenset()}
        self.assertFalse(check_union_closed.apply(es3))
        self.assertEqual(aux.ucl(es3), es3_ucl)
        self.assertFalse(check_contains_empty.apply(es3))
        self.assertTrue(check_intersection_in.apply(es3))
        self.assertEqual(aux.reduce(es3), es3_reduced)
        self.assertFalse(check_downward_closed.apply(es3))

        es4 = {set_empty, set_a, set_b, set_ab}
        es4_ucl = es4
        es4_reduced = es4
        self.assertTrue(check_union_closed.apply(es4))
        self.assertEqual(aux.ucl(es4), es4_ucl)
        self.assertTrue(check_contains_empty.apply(es4))
        self.assertTrue(check_intersection_in.apply(es4))
        self.assertEqual(aux.reduce(es4), es4_reduced)
        self.assertTrue(check_downward_closed.apply(es4))

        es5 = {set_c, set_abc, set_bc, set_ac}
        es5_ucl = {set_empty, set_c, set_abc, set_bc, set_ac}
        es5_reduced = {set_empty, set_ab, set_b, set_a}
        self.assertFalse(check_union_closed.apply(es5))
        self.assertEqual(aux.ucl(es5), es5_ucl)
        self.assertFalse(check_contains_empty.apply(es5))
        self.assertTrue(check_intersection_in.apply(es5))
        self.assertEqual(aux.reduce(es5), es5_reduced)
        self.assertFalse(check_downward_closed.apply(es5))

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
        self.assertEqual(get_stable_extensions.apply(canonical_aba1), es1)

        es2 = {set_a, set_b, set_c}
        canonical_aba2 = canonical_st.apply(es2)
        self.assertEqual(canonical_aba2.assumptions, {a, b, c})
        self.assertEqual(canonical_aba2.language, {a, b, c, a_c, b_c, c_c})
        self.assertEqual(canonical_aba2.rules, {Rule('', {a}, b_c), Rule('', {a}, c_c),
                                                Rule('', {b}, a_c), Rule('', {b}, c_c),
                                                Rule('', {c}, a_c), Rule('', {c}, b_c)})
        self.assertEqual(canonical_aba2.contraries, {a: a_c, b: b_c, c: c_c})
        self.assertEqual(get_stable_extensions.apply(canonical_aba2), es2)

    def test_canonical_cf(self):
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

        es1 = {set_empty, set_a, set_b, set_c, set_ab}
        aba = construct_abaf_cf.apply(es1)
        es_n = get_conflict_free_extensions.apply(aba)
        self.assertEqual(es1, es_n)

        es2 = {set_empty, set_a, set_b, set_c, set_ab, set_ac, set_bc}
        aba = construct_abaf_cf.apply(es2)
        es_n = get_conflict_free_extensions.apply(aba)
        self.assertEqual(es2, es_n)

    def test_canonical_adm(self):
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

        es1 = {set_empty, set_c, set_ab, set_abc}
        canonical_aba1 = construct_abaf_adm.apply(es1)
        canonical_aba1.reduce()
        es_n = get_admissible_extensions.apply(canonical_aba1)

        self.assertEqual(es1, es_n)

    def test_canonical_com(self):
        a = 'a'
        b = 'b'
        c = 'c'
        d = 'd'
        a_c = 'a_c'
        b_c = 'b_c'
        c_c = 'c_c'
        d_c = 'd_c'
        x_a = 'x_a'
        x_b = 'x_b'
        x_c = 'x_c'
        x_d = 'x_d'
        x_a_c = 'x_a_c'
        x_b_c = 'x_b_c'
        x_c_c = 'x_c_c'
        x_d_c = 'x_d_c'

        set_empty = frozenset({})
        set_a = frozenset({a})
        set_b = frozenset({b})
        set_c = frozenset({c})
        set_d = frozenset({d})
        set_ab = frozenset({a, b})
        set_ac = frozenset({a, c})
        set_ad = frozenset({a, d})
        set_bc = frozenset({b, c})
        set_bd = frozenset({b, d})
        set_cd = frozenset({c, d})
        set_abc = frozenset({a, b, c})
        set_abd = frozenset({a, b, d})
        set_acd = frozenset({a, c, d})
        set_bcd = frozenset({b, c, d})
        set_abcd = frozenset({a, b, c, d})

        es1 = {set_empty, set_c, set_d, set_cd, set_ab, set_abc}

        self.assertTrue(check_set_com_closed.apply(es1))
        self.assertTrue(check_intersection_in.apply(es1))
        canonical_aba1 = construct_abaf_com.apply(es1)
        canonical_aba1.reduce()
        es_n = get_complete_extensions.apply(canonical_aba1)

        self.assertEqual(es1, es_n)

        es2 = {set_empty, set_c}

        self.assertTrue(check_set_com_closed.apply(es2))
        self.assertTrue(check_intersection_in.apply(es2))
        canonical_aba2 = construct_abaf_com.apply(es2)
        canonical_aba2.reduce()
        es_n = get_complete_extensions.apply(canonical_aba2)

        self.assertEqual(es2, es_n)

        es3 = {set_c}

        self.assertTrue(check_set_com_closed.apply(es3))
        self.assertTrue(check_intersection_in.apply(es3))
        canonical_aba3 = construct_abaf_com.apply(es3)
        canonical_aba3.reduce()
        es_n = get_complete_extensions.apply(canonical_aba3)

        self.assertEqual(es3, es_n)
