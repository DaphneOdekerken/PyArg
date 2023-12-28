import unittest

import py_arg.abstract_argumentation.canonical_constructions.canonical_af. \
    canonical_cf as canonical_cf
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_conflict_sensitive, is_incomparable, is_tight, \
    contains_empty_set, is_non_empty
from py_arg.abstract_argumentation.canonical_constructions.canonical_af \
    import construct_af_adm, construct_af_grd
from py_arg.abstract_argumentation.canonical_constructions.canonical_af \
    import construct_af_stb
from py_arg.abstract_argumentation.generators. \
    abstract_argumentation_framework_generator \
    import AbstractArgumentationFrameworkGenerator
from py_arg.abstract_argumentation.semantics import get_grounded_extension, \
    get_stable_extensions, get_admissible_sets


class TestCanonicalConstructions(unittest.TestCase):

    def test_grd_construction(self):
        af = AbstractArgumentationFrameworkGenerator(9, 8).generate()
        es_original = {
            frozenset(get_grounded_extension.get_grounded_extension(af))}
        af_cf = canonical_cf.apply(es_original)
        es_new = {
            frozenset(get_grounded_extension.get_grounded_extension(af_cf))}

        self.assertEqual(es_original, es_new)
        self.assertEqual(len(es_new), 1)

    def test_adm_construction(self):
        af = AbstractArgumentationFrameworkGenerator(5, 5).generate()
        es_original = get_admissible_sets.get_admissible_sets(af)
        af_adm = construct_af_adm.apply(es_original)
        es_new = get_admissible_sets.get_admissible_sets(af_adm)

        self.assertTrue(is_conflict_sensitive(es_original) and
                        contains_empty_set(es_original) and
                        is_non_empty(es_original))
        self.assertEqual(es_original, es_new)

    def test_grd_construction_small(self):
        af = AbstractArgumentationFrameworkGenerator(5, 5).generate()
        es_original = {
            frozenset(get_grounded_extension.get_grounded_extension(af))}
        af_grd = construct_af_grd.apply(es_original)
        es_new = {
            frozenset(get_grounded_extension.get_grounded_extension(af_grd))}

        self.assertEqual(es_original, es_new)

    def test_stb_construction(self):
        af = AbstractArgumentationFrameworkGenerator(5, 5).generate()
        es_original = get_stable_extensions.get_stable_extensions(af)
        af_stb = construct_af_stb.apply(es_original)
        es_new = get_stable_extensions.get_stable_extensions(af_stb)

        self.assertTrue(is_incomparable(es_original) and is_tight(es_original))
        self.assertEqual(es_original, es_new)
