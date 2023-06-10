import unittest

import py_arg.algorithms.canonical_constructions.canonical_af.canonical_cf as canonical_cf

from py_arg.algorithms.canonical_constructions import check_incomparable, check_tight, check_conf_sens
from py_arg.algorithms.canonical_constructions.canonical_af import construct_af_adm, construct_af_grd, construct_af_stb
from py_arg.algorithms.semantics import get_stable_extensions, get_grounded_extension, get_admissible_sets
from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator \
    import AbstractArgumentationFrameworkGenerator


class TestCanonicalConstructions(unittest.TestCase):

    def test_grd_construction(self):
        af = AbstractArgumentationFrameworkGenerator(9, 8).generate()
        es_original = {frozenset(get_grounded_extension.get_grounded_extension(af))}
        af_cf = canonical_cf.apply(es_original)
        es_new = {frozenset(get_grounded_extension.get_grounded_extension(af_cf))}

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
