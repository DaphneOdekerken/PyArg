import unittest

import py_arg.abstract_argumentation.semantics.get_conflict_free_extensions as get_conflict_free_extensions

import py_arg.abstract_argumentation.canonical_constructions.canonical_af.construct_af_cf as construct_af_cf
from py_arg.abstract_argumentation.canonical_constructions import check_tight
from py_arg.abstract_argumentation.canonical_constructions import check_downward_closed
from py_arg.abstract_argumentation.generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator


class TestCanonicalConstructions(unittest.TestCase):

    def test_cf_ext(self):
        af = AbstractArgumentationFrameworkGenerator(9, 8).generate()
        es = get_conflict_free_extensions.apply(af)
        af_cf = construct_af_cf.apply(es)
        es_new = get_conflict_free_extensions.apply(af_cf)

        self.assertTrue(check_downward_closed.apply(es))
        self.assertTrue(check_tight.apply(es))
        self.assertTrue(check_downward_closed.apply(es_new))
        self.assertTrue(check_tight.apply(es_new))
        self.assertEqual(es, es_new)
