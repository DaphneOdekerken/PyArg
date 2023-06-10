import unittest

import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_cf as canonical_cf
import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_st as canonical_st
import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_ucl as canonical_ucl
import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_com as canonical_com
import py_arg.algorithms.canonical_constructions.canonical_abaf.canonical_adm as canonical_adm
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_cf as construct_abaf_cf
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_st as construct_abaf_st
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_com as construct_abaf_com
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_adm as construct_abaf_adm
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_prf as construct_abaf_prf
import py_arg.algorithms.canonical_constructions.canonical_abaf.construct_abaf_naive as construct_abaf_naive

import py_arg.algorithms.canonical_constructions.aux_operators as aux
from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes.instantiated_argument import InstantiatedArgument
from py_arg.aba_classes.rule import Rule

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat

import py_arg.algorithms.canonical_constructions.check_contains_empty as check_contains_empty
import py_arg.algorithms.canonical_constructions.check_downward_closed as check_downward_closed
import py_arg.algorithms.canonical_constructions.check_dcl_tight as check_dcl_tight
import py_arg.algorithms.canonical_constructions.check_intersection_in as check_intersection_in
import py_arg.algorithms.canonical_constructions.check_union_closed as check_union_closed
import py_arg.algorithms.canonical_constructions.check_incomparable as check_incomparable
import py_arg.algorithms.canonical_constructions.check_tight as check_tight
import py_arg.algorithms.canonical_constructions.check_com_closed as check_com_closed
import py_arg.algorithms.canonical_constructions.check_set_com_closed as check_set_com_closed
import py_arg.algorithms.canonical_constructions.check_conf_sens as check_conf_sens
import py_arg.algorithms.canonical_constructions.check_set_conf_sens as check_set_conf_sens


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

