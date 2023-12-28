import unittest

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    construct_af_cf import construct_argumentation_framework_conflict_free
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_downward_closed, is_tight
from py_arg.abstract_argumentation.generators.\
    abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg.abstract_argumentation.semantics.get_conflict_free_extensions \
    import get_conflict_free_extensions


class TestCanonicalConstructions(unittest.TestCase):
    def test_cf_ext(self):
        af = AbstractArgumentationFrameworkGenerator(9, 8).generate()
        es = get_conflict_free_extensions(af)
        af_cf = construct_argumentation_framework_conflict_free(es)
        es_new = get_conflict_free_extensions(af_cf)

        self.assertTrue(is_downward_closed(es))
        self.assertTrue(is_tight(es))
        self.assertTrue(is_downward_closed(es_new))
        self.assertTrue(is_tight(es_new))
        self.assertEqual(es, es_new)
