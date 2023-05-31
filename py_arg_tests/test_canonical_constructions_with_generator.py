import unittest

from typing import Set, FrozenSet

import py_arg.algorithms.semantics.get_stable_extensions as get_stable_extensions

import py_arg.algorithms.canonical_constructions.canonical_cf as canonical_cf
import py_arg.algorithms.canonical_constructions.canonical_st as canonical_st
import py_arg.algorithms.canonical_constructions.canonical_def as canonical_def

import py_arg.algorithms.canonical_constructions.aux_operators as aux_operators

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat

from py_arg.algorithms.canonical_constructions import check_incomparable, check_tight, check_downward_closed, \
    check_downward_closed, check_com_closed, check_set_com_closed, check_conf_sens, check_set_conf_sens
from py_arg.algorithms.canonical_constructions import construct_af_cf, construct_af_adm, construct_af_grd, \
    construct_af_stb, construct_af_naive, construct_af_stage
from py_arg.algorithms.semantics import get_stable_extensions, get_ideal_extension, get_preferred_extensions, \
    get_semistable_extensions, get_complete_extensions, get_grounded_extension, get_admissible_sets, get_eager_extension
from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator \
    import AbstractArgumentationFrameworkGenerator


class TestCanonicalConstructions(unittest.TestCase):

    def test_grd_construction(self):
        af = AbstractArgumentationFrameworkGenerator(9, 8).generate()
        es_original = set({frozenset(get_grounded_extension.get_grounded_extension(af))})
        af_cl = canonical_cf.apply(es_original)
        es_new = set({frozenset(get_grounded_extension.get_grounded_extension(af_cl))})

        self.assertEqual(es_original, es_new)
        self.assertEqual(len(es_new), 1)

    def test_adm_construction(self):
        af = AbstractArgumentationFrameworkGenerator(5, 5).generate()
        es_original = get_admissible_sets.get_admissible_sets(af)
        af_adm = construct_af_adm.apply(es_original)
        es_new = get_admissible_sets.get_admissible_sets(af_adm)

        self.assertTrue(check_conf_sens.apply(es_original) and frozenset() in es_original)
        self.assertEqual(es_original, es_new)

    def test_grd_construction(self):
        af = AbstractArgumentationFrameworkGenerator(5, 5).generate()
        es_original = {frozenset(get_grounded_extension.get_grounded_extension(af))}
        af_grd = construct_af_grd.apply(es_original)
        es_new = {frozenset(get_grounded_extension.get_grounded_extension(af_grd))}

        self.assertEqual(es_original, es_new)

    def test_stb_construction(self):
        af = AbstractArgumentationFrameworkGenerator(5, 5).generate()
        es_original = get_stable_extensions.get_stable_extensions(af)
        af_stb = construct_af_stb.apply(es_original)
        es_new = get_stable_extensions.get_stable_extensions(af_stb)

        self.assertTrue(check_incomparable.apply(es_original) and check_tight.apply(es_original))
        self.assertEqual(es_original, es_new)
