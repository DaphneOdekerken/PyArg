import unittest

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.explanation.get_attackers_without_defense \
    import get_attackers_without_defense_in_extension, \
    get_reachable_by_odd_path
from py_arg.abstract_argumentation.explanation.get_defending_arguments import \
    get_reachable_by_even_path, get_defending_arguments_in_extension
from py_arg.abstract_argumentation.explanation.get_extensions_with_argument \
    import filter_argumentation_framework_extensions_with_argument
from py_arg.abstract_argumentation.explanation.\
    get_extensions_without_argument import \
    filter_argumentation_framework_extensions_without_argument
from py_arg.abstract_argumentation.explanation.\
    get_reachable_arguments_and_distances import \
    get_reachable_arguments_and_distances
from py_arg.abstract_argumentation.semantics.acceptance_strategy import \
    AcceptanceStrategy
from py_arg.abstract_argumentation.semantics.get_accepted_arguments import \
    get_accepted_arguments
from py_arg.abstract_argumentation.semantics.get_eager_extension import \
    get_eager_extensions
from py_arg.abstract_argumentation.semantics.get_grounded_extension import \
    get_grounded_extensions
from py_arg.abstract_argumentation.semantics.get_ideal_extension import \
    get_ideal_extensions
from py_arg.abstract_argumentation.semantics.get_preferred_extensions import \
    get_preferred_extensions
from py_arg.abstract_argumentation.semantics.get_semistable_extensions import \
    get_semi_stable_extensions
from py_arg.abstract_argumentation.semantics.get_stable_extensions import \
    get_stable_extensions
from py_arg.aspic.classes.argumentation_system import ArgumentationSystem
from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic.classes.defeasible_rule import DefeasibleRule
from py_arg.aspic.classes.literal import Literal
from py_arg.aspic.semantics.get_accepted_formulas import get_accepted_formulas


# These examples are from Borg, AnneMarie, and Floris Bex. "Necessary and
# sufficient explanations for argumentation-based conclusions." European
# Conference on Symbolic and Quantitative Approaches with Uncertainty.
# Springer International Publishing, 2021.

class TestNecessarySufficientExplanations(unittest.TestCase):
    def test_af_1(self):
        # Create the example argumentation framework from Figure 1/Example 1.
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        e = Argument('e')
        f = Argument('f')
        defeats = [Defeat(x, y) for x, y in [(b, a), (c, b), (c, d), (d, c),
                                             (e, b), (e, f), (f, e)]]
        af = AbstractArgumentationFramework('af', [a, b, c, d, e, f], defeats)

        # Extensions for various semantics (Example 2).
        grounded_extensions = get_grounded_extensions(af)
        preferred_extensions = get_preferred_extensions(af)
        self.assertSetEqual(grounded_extensions, {frozenset(set())})
        accepted_grounded = get_accepted_arguments(
            grounded_extensions, AcceptanceStrategy.CREDULOUS)
        self.assertSetEqual(accepted_grounded, set())

        gt_extensions = {
            frozenset({a, c, e}),
            frozenset({a, c, f}),
            frozenset({a, d, e}),
            frozenset({b, d, f})
        }
        self.assertSetEqual(preferred_extensions, gt_extensions)

        # The "SemWith" and "SemWithout" notation, introduced in Notation 1
        # (Example 3).
        gt_extensions_with_a = {
            frozenset({a, c, e}),
            frozenset({a, c, f}),
            frozenset({a, d, e})
        }
        extensions_with_a = \
            filter_argumentation_framework_extensions_with_argument(
                preferred_extensions, a)
        self.assertSetEqual(gt_extensions_with_a, extensions_with_a)
        gt_extensions_with_b = {
            frozenset({b, d, f})
        }
        extensions_with_b = \
            filter_argumentation_framework_extensions_with_argument(
                preferred_extensions, b)
        self.assertSetEqual(gt_extensions_with_b, extensions_with_b)
        gt_extensions_without_d = {
            frozenset({a, c, e}),
            frozenset({a, c, f})
        }
        extensions_without_d = \
            filter_argumentation_framework_extensions_without_argument(
                preferred_extensions, d)
        self.assertSetEqual(gt_extensions_without_d, extensions_without_d)
        gt_extensions_without_e = {
            frozenset({a, c, f}),
            frozenset({b, d, f})
        }
        extensions_without_e = \
            filter_argumentation_framework_extensions_without_argument(
                preferred_extensions, e)
        self.assertSetEqual(gt_extensions_without_e, extensions_without_e)

        # Credulous and skeptical acceptance for various semantics(Example 4).
        no_arguments = set()
        all_arguments = set(af.arguments)

        accepted_preferred_skeptical = get_accepted_arguments(
            preferred_extensions, AcceptanceStrategy.SKEPTICAL)
        self.assertSetEqual(accepted_preferred_skeptical, no_arguments)
        accepted_preferred_credulous = get_accepted_arguments(
            preferred_extensions, AcceptanceStrategy.CREDULOUS)
        self.assertSetEqual(accepted_preferred_credulous, all_arguments)

        semi_stable_extensions = get_semi_stable_extensions(af)
        accepted_semi_stable = get_accepted_arguments(
            semi_stable_extensions, AcceptanceStrategy.CREDULOUS)
        self.assertSetEqual(accepted_semi_stable, all_arguments)

        # Reachability (Example 12).
        reachable_arguments, distance_dictionary = \
            get_reachable_arguments_and_distances(af, a)
        self.assertSetEqual(distance_dictionary[c], {2, 4})

        gt_reachable_from_a = {b, c, d, e, f}
        self.assertSetEqual(reachable_arguments, gt_reachable_from_a)

        # Reachability with odd/even path lengths (Example 13).
        gt_even_reachable_from_a = {c, e}
        even_reachable_from_a = get_reachable_by_even_path(
            reachable_arguments, distance_dictionary)
        self.assertSetEqual(gt_even_reachable_from_a, even_reachable_from_a)
        gt_odd_reachable_from_a = {b, d, f}
        odd_reachable_from_a = get_reachable_by_odd_path(
            reachable_arguments, distance_dictionary)
        self.assertSetEqual(gt_odd_reachable_from_a, odd_reachable_from_a)

        reachable_arguments, distance_dictionary = \
            get_reachable_arguments_and_distances(af, b)
        self.assertSetEqual(distance_dictionary[e], {1, 3})

        gt_attackers_of_a_without_defense = {b, d, f}
        attackers_of_a_without_defense = \
            get_attackers_without_defense_in_extension(
                af, a, frozenset({b, d, f}))
        self.assertSetEqual(
            gt_attackers_of_a_without_defense, attackers_of_a_without_defense)

    def test_af_2(self):
        # Create the example argumentation framework from Figure 2/Example 7.
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        e = Argument('e')
        defeats = [Defeat(x, y) for x, y in [(b, a), (c, b), (d, b), (d, e),
                                             (e, d)]]
        af = AbstractArgumentationFramework('af', [a, b, c, d, e], defeats)

        # Example 7.
        gt_preferred_extensions = {
            frozenset({a, c, d}),
            frozenset({a, c, e})
        }
        preferred_extensions = get_preferred_extensions(af)
        stable_extensions = get_stable_extensions(af)
        semi_stable_extensions = get_semi_stable_extensions(af)
        self.assertSetEqual(gt_preferred_extensions, preferred_extensions)
        self.assertSetEqual(gt_preferred_extensions, stable_extensions)
        self.assertSetEqual(gt_preferred_extensions, semi_stable_extensions)

        gt_grounded_extensions = {frozenset({a, c})}
        grounded_extensions = get_grounded_extensions(af)
        ideal_extensions = get_ideal_extensions(af)
        eager_extensions = get_eager_extensions(af)
        self.assertSetEqual(gt_grounded_extensions, grounded_extensions)
        self.assertSetEqual(gt_grounded_extensions, ideal_extensions)
        self.assertSetEqual(gt_grounded_extensions, eager_extensions)

    def test_af_3(self):
        # Create the example argumentation framework from Figure 3/Example 10.
        a = Argument('a')
        b = Argument('b')
        c = Argument('c')
        d = Argument('d')
        e = Argument('e')
        f = Argument('f')
        defeats = [Defeat(x, y) for x, y in [(a, b), (b, a), (b, c), (d, c),
                                             (d, e), (e, f), (f, d)]]
        af = AbstractArgumentationFramework('af', [a, b, c, d, e, f], defeats)

        # Example 10.
        gt_preferred_extensions = {
            frozenset({a}),
            frozenset({b})
        }
        preferred_extensions = get_preferred_extensions(af)
        self.assertSetEqual(gt_preferred_extensions, preferred_extensions)

        gt_defenders_b = {b}
        defenders_b = get_defending_arguments_in_extension(
            af, b, frozenset({b}))
        self.assertSetEqual(gt_defenders_b, defenders_b)

        # gt_attackers_c_without_defense_in_extension_b = {b, d, e, f}
        # attackers_c_without_defense_in_extension_b = \
        #     get_attackers_without_defense_in_extension(af, c, frozenset({b}))
        # TODO: Check with AnneMarie.
        # self.assertSetEqual(gt_attackers_c_without_defense_in_extension_b,
        #                     attackers_c_without_defense_in_extension_b)

    def test_accepted_formulas(self):
        p = Literal('p')
        q = Literal('q')
        r = Literal('r')
        s = Literal('s')
        t = Literal('t')
        u = Literal('u')
        v = Literal('v')
        neg_p = Literal('-p')
        neg_q = Literal('-q')

        d1 = DefeasibleRule('d1', {s, t}, u)
        n_d1 = Literal.from_defeasible_rule(d1)
        neg_n_d1 = Literal.from_defeasible_rule_negation(d1)

        d2 = DefeasibleRule('d2', {p, neg_q}, neg_n_d1)
        d3 = DefeasibleRule('d3', {r, s}, q)
        d4 = DefeasibleRule('d4', {v}, neg_q)
        d5 = DefeasibleRule('d5', {r, t}, neg_p)
        d6 = DefeasibleRule('d6', {v}, p)

        language = {lit.s1: lit
                    for lit in
                    (p, q, r, s, t, u, v, neg_p, neg_q, n_d1, neg_n_d1)}
        defeasible_rules = [d1, d2, d3, d4, d5, d6]

        contradictions = {
            p.s1: {neg_p},
            neg_p.s1: {p},
            q.s1: {neg_q},
            neg_q.s1: {q},
            n_d1.s1: {neg_n_d1},
            neg_n_d1.s1: {n_d1}
        }

        arg_sys = ArgumentationSystem(language, contradictions, [],
                                      defeasible_rules)

        k_1 = [r, s, t, v]
        arg_theory = ArgumentationTheory(arg_sys, k_1, [])

        arg_framework = arg_theory.create_abstract_argumentation_framework(
            'af')
        extensions = get_preferred_extensions(arg_framework)
        accepted_formulas = get_accepted_formulas(extensions,
                                                  AcceptanceStrategy.CREDULOUS)

        gt_accepted_formulas = [p, neg_p, q, neg_q, r, s, t, u, v]
        self.assertListEqual(sorted(accepted_formulas),
                             sorted(gt_accepted_formulas))
