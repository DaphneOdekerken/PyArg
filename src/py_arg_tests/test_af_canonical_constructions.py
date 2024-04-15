import unittest

from py_arg.abstract_argumentation.canonical_constructions.aux_operators \
    import downward_closure
from py_arg.abstract_argumentation.canonical_constructions.canonical_af. \
    canonical_def import get_cnf_defense_formula, get_defense_formula, \
    get_canonical_def_framework
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_tight, is_conflict_sensitive, is_com_closed
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.semantics.get_admissible_sets import \
    get_admissible_sets
from py_arg.abstract_argumentation.semantics.get_complete_extensions import \
    get_complete_extensions
from py_arg.abstract_argumentation.semantics.get_naive_extensions import \
    get_naive_extensions
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    get_preferred_extensions
from py_arg.abstract_argumentation.semantics.get_semistable_extensions import \
    get_semi_stable_extensions
from py_arg.abstract_argumentation.semantics.get_stable_extensions import \
    get_stable_extensions


class TestCanonicalConstructions(unittest.TestCase):
    def test_example_1_and_2(self):
        # Example 1.
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        set_1 = frozenset({a, b})
        set_2 = frozenset({a, c})
        set_3 = frozenset({b, c})
        extension_set = {set_1, set_2, set_3}
        self.assertTrue(is_incomparable(extension_set))

        # Example 2.
        self.assertFalse(is_tight(extension_set))

        d = Argument('d')
        extension_set = {set_1, set_2, frozenset({b, d}), frozenset({c, d})}
        self.assertTrue(is_tight(extension_set))

    def test_example_3(self):
        # Example 3.
        a_1 = Argument('a1')
        a_2 = Argument('a2')
        a_3 = Argument('a3')
        b_1 = Argument('b1')
        b_2 = Argument('b2')
        b_3 = Argument('b3')
        defeats = [Defeat(x, y) for x, y in
                   [(a_1, b_1), (a_2, b_2), (a_3, b_3),
                    (a_1, a_2), (a_2, a_3), (a_3, a_1),
                    (a_2, a_1), (a_3, a_2), (a_1, a_3)]]
        af = AbstractArgumentationFramework(
            '', [a_1, a_2, a_3, b_1, b_2, b_3], defeats)

        gt_stable = {
            frozenset({a_1, b_2, b_3}),
            frozenset({a_2, b_1, b_3}),
            frozenset({a_3, b_1, b_2})
        }
        stable = get_stable_extensions(af)
        self.assertSetEqual(gt_stable, stable)

        # TODO add test for stage semantics, once implemented.

        gt_naive = gt_stable.union({frozenset({b_1, b_2, b_3})})
        naive = get_naive_extensions(af)
        self.assertSetEqual(gt_naive, naive)

        self.assertTrue(is_tight(stable))

        stable_dcl = downward_closure(stable)
        self.assertFalse(is_tight(stable_dcl))

    def test_example_4(self):
        # Example 4.
        a = Argument('a')
        a_prime = Argument('a_prime')
        b = Argument('b')
        b_prime = Argument('b_prime')
        c = Argument('c')
        d = Argument('d')
        e = Argument('e')
        f = Argument('f')
        arguments = [a, a_prime, b, b_prime, c, d, e, f]
        defeats = [Defeat(x, y) for x, y in [
            (a_prime, a_prime), (a_prime, a), (a, a_prime), (a, c), (c, a),
            (b_prime, b_prime), (b_prime, b), (b, b_prime), (b, d), (d, b),
            (c, d), (d, c), (c, f), (d, f), (f, f), (f, e)
        ]]
        af = AbstractArgumentationFramework('af', arguments, defeats)

        gt_preferred = {
            frozenset({a, b}),
            frozenset({a, d, e}),
            frozenset({b, c, e})
        }
        preferred = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred, preferred)

        semi_stable = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_preferred, semi_stable)

        self.assertTrue(is_conflict_sensitive(preferred))
        self.assertFalse(is_tight(preferred))

    def test_example_5(self):
        # Example 5.
        a = Argument('a')
        b = Argument('b')
        a_prime = Argument('a_prime')
        b_prime = Argument('b_prime')
        c = Argument('c')
        arguments = [a, b, a_prime, b_prime, c]
        defeats = [Defeat(x, y) for x, y in [
            (a, a_prime), (a_prime, a_prime), (a_prime, a), (a_prime, c),
            (b, b_prime), (b_prime, b_prime), (b_prime, b), (b_prime, c)
        ]]
        af = AbstractArgumentationFramework('af', arguments, defeats)

        gt_complete = {
            frozenset({}),
            frozenset({a}),
            frozenset({b}),
            frozenset({a, b, c})
        }
        complete = get_complete_extensions(af)
        self.assertSetEqual(gt_complete, complete)
        self.assertTrue(is_com_closed(complete))
        self.assertFalse(is_conflict_sensitive(complete))

    def test_example_figure_4(self):
        a_1 = Argument('a1')
        a_2 = Argument('a2')
        a_3 = Argument('a3')
        b_1 = Argument('b1')
        b_2 = Argument('b2')
        b_3 = Argument('b3')
        big_e_overline = Argument('-E')
        defeats = [Defeat(x, y) for x, y in
                   [(a_1, b_1), (a_2, b_2), (a_3, b_3),
                    (b_1, a_1), (b_2, a_2), (b_3, a_3),
                    (a_1, a_2), (a_2, a_3), (a_3, a_1),
                    (a_2, a_1), (a_3, a_2), (a_1, a_3),
                    (a_1, big_e_overline), (a_2, big_e_overline),
                    (a_3, big_e_overline), (big_e_overline, big_e_overline)]]
        af = AbstractArgumentationFramework(
            '', [a_1, a_2, a_3, b_1, b_2, b_3, big_e_overline], defeats)

        extension_set = {
            frozenset({a_1, b_2, b_3}),
            frozenset({a_2, b_1, b_3}),
            frozenset({a_3, b_1, b_2})
        }
        stable = get_stable_extensions(af)
        self.assertSetEqual(extension_set, stable)

        # TODO: add test for stage (once implemented).

    def test_example_6_and_7(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        extension_set = {
            frozenset(),
            frozenset({a}),
            frozenset({b, c}),
            frozenset({a, c, d})
        }

        gt_defence_formula_a = {frozenset(), frozenset({c, d})}
        gt_defence_formula_b = {frozenset({c})}
        gt_defence_formula_c = {frozenset({b}), frozenset({a, d})}
        gt_defence_formula_d = {frozenset({a, c})}

        defence_formula_a = get_defense_formula(extension_set, a)
        defence_formula_b = get_defense_formula(extension_set, b)
        defence_formula_c = get_defense_formula(extension_set, c)
        defence_formula_d = get_defense_formula(extension_set, d)

        self.assertSetEqual(gt_defence_formula_a, defence_formula_a)
        self.assertSetEqual(gt_defence_formula_b, defence_formula_b)
        self.assertSetEqual(gt_defence_formula_c, defence_formula_c)
        self.assertSetEqual(gt_defence_formula_d, defence_formula_d)

        gt_cnf_defence_formula_a = set()
        gt_cnf_defence_formula_b = {frozenset({c})}
        gt_cnf_defence_formula_c = {frozenset({a, b}), frozenset({b, d})}
        gt_cnf_defence_formula_d = {frozenset({a}), frozenset({c})}

        cnf_defence_formula_a = get_cnf_defense_formula(extension_set, a)
        cnf_defence_formula_b = get_cnf_defense_formula(extension_set, b)
        cnf_defence_formula_c = get_cnf_defense_formula(extension_set, c)
        cnf_defence_formula_d = get_cnf_defense_formula(extension_set, d)

        self.assertSetEqual(gt_cnf_defence_formula_a, cnf_defence_formula_a)
        self.assertSetEqual(gt_cnf_defence_formula_b, cnf_defence_formula_b)
        self.assertSetEqual(gt_cnf_defence_formula_c, cnf_defence_formula_c)
        self.assertSetEqual(gt_cnf_defence_formula_d, cnf_defence_formula_d)

        canonical_def_framework = get_canonical_def_framework(extension_set)
        self.assertEqual(len(canonical_def_framework.arguments), 9)
        self.assertEqual(len(canonical_def_framework.defeats), 21)
        admissible = get_admissible_sets(canonical_def_framework)
        self.assertSetEqual(admissible, extension_set)

    def test_example_8(self):
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        e = Argument('e')
        f = Argument('f')
        x = Argument('x')
        extension_set = {
            frozenset(), frozenset({a}), frozenset({b}), frozenset({c}),
            frozenset({a, b, c}), frozenset({a, d, e}), frozenset({b, d, f}),
            frozenset({x, c}), frozenset({x, d})
        }
        self.assertTrue(is_com_closed(extension_set))
