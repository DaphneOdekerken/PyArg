import unittest

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.orderings.elitist_ordering import ElitistOrdering
from py_arg.aspic_classes.orderings.last_link_ordering import LastLinkElitistOrdering, LastLinkDemocraticOrdering
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.ordinary_premise import OrdinaryPremise
from py_arg.aspic_classes.preference import Preference
from py_arg.aspic_classes.strict_rule import StrictRule
from py_arg.aspic_classes.orderings.weakest_link_ordering import WeakestLinkElitistOrdering, \
    WeakestLinkDemocraticOrdering
from py_arg.aspic_classes.instantiated_argument import InstantiatedArgument


def get_argumentation_theory(include_d: bool = False, include_e: bool = False) -> ArgumentationTheory:
    literal_str_list = ['a', 'p', 'q', 'r', 's', 't']

    if include_d:
        literal_str_list.append('d')

    literal_str_list += ['-' + literal_str for literal_str in literal_str_list]
    literal_str_list += ['~' + literal_str for literal_str in literal_str_list]

    language = {literal_str: Literal(literal_str, literal_str + ' is present', literal_str + ' is absent')
                for literal_str in literal_str_list}

    contraries = {literal_str: [] for literal_str in language.keys()}
    for literal_str in language.keys():
        if literal_str[0] in ('~', '-'):
            contraries[literal_str].append(language[literal_str[1:]])
        else:
            contraries[literal_str].append(language['-' + literal_str])

    strict_rules = [StrictRule(1, {language['t'], language['q']}, language['-p'], 'r1')]

    d1 = DefeasibleRule(1, {language['~s']}, language['t'], 'd1')
    d2 = DefeasibleRule(2, {language['r']}, language['q'], 'd2')
    d3 = DefeasibleRule(3, {language['a']}, language['p'], 'd3')
    defeasible_rules = [d1, d2, d3]

    if include_d:
        defeasible_rules.append(DefeasibleRule(4, {language['~d']}, language['s'], 'd4'))

    for defeasible_rule in defeasible_rules:
        defeasible_rule_literal = Literal.from_defeasible_rule(defeasible_rule)
        defeasible_rule_literal_negation = Literal.from_defeasible_rule_negation(defeasible_rule)
        language[str(defeasible_rule_literal)] = defeasible_rule_literal
        language[str(defeasible_rule_literal_negation)] = defeasible_rule_literal_negation
        contraries[str(defeasible_rule_literal)] = [defeasible_rule_literal_negation]
        contraries[str(defeasible_rule_literal_negation)] = [defeasible_rule_literal]

    if include_e:
        strict_rules.append(StrictRule(2, {language['r']}, language['-d3'], 'r2'))

    arg_sys = ArgumentationSystem(language, contraries, strict_rules, defeasible_rules)

    axioms = []
    ordinary_premises = [language[literal_str] for literal_str in ['a', 'r', '-r', '~s']]

    if include_d:
        ordinary_premises.append(language['~d'])

    for ordinary_premise in ordinary_premises:
        ordinary_premise.__class__ = OrdinaryPremise

    arg_theory = ArgumentationTheory(arg_sys, axioms, ordinary_premises)
    return arg_theory


class TestModgilPrakkenAIJ(unittest.TestCase):
    def test_contradiction_function(self):
        arg_theory = get_argumentation_theory()
        a = arg_theory.argumentation_system.language['a']
        naf_a = arg_theory.argumentation_system.language['~a']
        neg_a = arg_theory.argumentation_system.language['-a']
        naf_neg_a = arg_theory.argumentation_system.language['~-a']
        self.assertIn(a, neg_a.contraries)
        self.assertIn(a, naf_a.contraries)
        self.assertIn(neg_a, a.contraries)
        self.assertIn(neg_a, naf_neg_a.contraries)
        self.assertNotIn(naf_a, a.contraries)
        self.assertNotIn(naf_neg_a, neg_a.contraries)

    def test_arguments(self):
        arg_theory = get_argumentation_theory()
        language = arg_theory.argumentation_system.language
        args_per_literal = arg_theory.arguments
        all_args = set().union(*args_per_literal.values())
        arg_a_prime = InstantiatedArgument.observation_based(language['a'])
        arg_a = InstantiatedArgument.defeasible_rule_based(
            DefeasibleRule(3, {language['a']}, language['p'], 'd3'), {arg_a_prime})
        arg_b1 = InstantiatedArgument.observation_based(language['~s'])
        arg_b1_prime = InstantiatedArgument.defeasible_rule_based(
            DefeasibleRule(1, {language['~s']}, language['t'], 'd1'), {arg_b1})
        arg_b2 = InstantiatedArgument.observation_based(language['r'])
        arg_b2_prime = InstantiatedArgument.defeasible_rule_based(
            DefeasibleRule(2, {language['r']}, language['q'], 'd2'), {arg_b2})
        arg_b = InstantiatedArgument.strict_rule_based(
            StrictRule(1, {language['t'], language['q']}, language['-p'], 'r1'), {arg_b2_prime, arg_b1_prime})
        arg_c = InstantiatedArgument.observation_based(language['-r'])

        self.assertListEqual(sorted(all_args),
                             sorted([arg_a_prime, arg_a, arg_b1, arg_b1_prime, arg_b2, arg_b2_prime, arg_b, arg_c]))
        self.assertSetEqual(arg_b.premises, {language['~s'], language['r']})
        self.assertEqual(arg_b.conclusion, language['-p'])
        # Note: incorrect in paper!
        self.assertSetEqual(arg_b.sub_arguments, {arg_b1, arg_b2, arg_b1_prime, arg_b2_prime, arg_b})
        self.assertEqual(arg_b.top_rule, StrictRule(1, {language['t'], language['q']}, language['-p'], 'r1'))
        self.assertSetEqual(arg_b.defeasible_rules, {
            DefeasibleRule(1, {language['~s']}, language['t'], 'd1'),
            DefeasibleRule(2, {language['r']}, language['q'], 'd2')
        })
        self.assertSetEqual(arg_b.strict_rules, {StrictRule(1, {language['t'], language['q']}, language['-p'], 'r1')})

        # Test attacks
        self.assertTrue(arg_theory.rebuts(arg_b, arg_a))
        self.assertTrue(arg_theory.undermines(arg_c, arg_b2_prime))
        self.assertTrue(arg_theory.undermines(arg_c, arg_b2))
        self.assertTrue(arg_theory.undermines(arg_b2, arg_c))
        self.assertFalse(arg_theory.attacks(arg_a, arg_b))
        self.assertFalse(arg_theory.attacks(arg_b, arg_c))

        arg_theory = get_argumentation_theory(include_d=True)
        language = arg_theory.argumentation_system.language
        arg_d1 = InstantiatedArgument.observation_based(language['~d'])
        arg_d2 = InstantiatedArgument.defeasible_rule_based(DefeasibleRule(4, {language['~d']}, language['s'], 'd4'),
                                                            {arg_d1})
        self.assertTrue(arg_theory.contrary_undermines(arg_d2, arg_b))
        self.assertTrue(arg_theory.contrary_undermines(arg_d2, arg_b1))
        self.assertTrue(arg_theory.contrary_undermines(arg_d2, arg_b1_prime))

        arg_theory = get_argumentation_theory(include_d=True, include_e=True)
        arg_e = InstantiatedArgument.strict_rule_based(arg_theory.argumentation_system.strict_rules[1], {arg_b2})
        self.assertTrue(arg_theory.undercuts(arg_e, arg_a))

        # Test defeats
        d1 = DefeasibleRule(1, {language['~s']}, language['t'], 'd1')
        d2 = DefeasibleRule(2, {language['r']}, language['q'], 'd2')
        d3 = DefeasibleRule(3, {language['a']}, language['p'], 'd3')

        arg_theory.argumentation_system.add_rule_preference(Preference(d2, '<', d3))
        arg_theory.add_ordinary_premise_preference(Preference(language['-r'], '<', language['r']))
        # arg_theory.add_ordinary_queryable_preference(Preference(language['-a'], '=', language['r']))
        arg_theory.add_ordinary_premise_preference(Preference(language['~s'], '<', language['-r']))

        self.assertSetEqual(arg_a.defeasible_rules, arg_a.last_defeasible_rules, {d3})
        self.assertSetEqual(arg_a.ordinary_premises, {language['a']})
        self.assertSetEqual(arg_a_prime.defeasible_rules, arg_a_prime.last_defeasible_rules, set())
        self.assertSetEqual(arg_a_prime.ordinary_premises, {language['a']})
        self.assertSetEqual(arg_b.defeasible_rules, arg_b.last_defeasible_rules, {d1, d2})
        self.assertSetEqual(arg_b.ordinary_premises, {language['~s'], language['r']})
        self.assertSetEqual(arg_b2.defeasible_rules, arg_b2.last_defeasible_rules, set())
        self.assertSetEqual(arg_b2.ordinary_premises, {language['r']})
        self.assertSetEqual(arg_c.defeasible_rules, arg_c.last_defeasible_rules, set())
        self.assertSetEqual(arg_c.premises, {language['-r']})

        eli = ElitistOrdering(arg_theory.argumentation_system.rule_preference_dict,
                              arg_theory.ordinary_premise_preference_dict)
        self.assertTrue(eli.rule_set_is_strictly_weaker_than(arg_b.last_defeasible_rules, arg_a.last_defeasible_rules))
        ell = LastLinkElitistOrdering(arg_theory.argumentation_system.rule_preference_dict,
                                      arg_theory.ordinary_premise_preference_dict)
        self.assertTrue(ell.argument_is_strictly_weaker_than(arg_b, arg_a))
        self.assertTrue(eli.rule_set_is_strictly_weaker_than(arg_b.defeasible_rules, arg_a.defeasible_rules))
        self.assertFalse(eli.ordinary_premise_set_is_strictly_weaker_than(arg_b.ordinary_premises,
                                                                          arg_a.ordinary_premises))
        ewl = WeakestLinkElitistOrdering(arg_theory.argumentation_system.rule_preference_dict,
                                         arg_theory.ordinary_premise_preference_dict)
        self.assertFalse(ewl.argument_is_strictly_weaker_than(arg_b, arg_a))
        dll = LastLinkDemocraticOrdering(arg_theory.argumentation_system.rule_preference_dict,
                                         arg_theory.ordinary_premise_preference_dict)
        self.assertFalse(dll.argument_is_strictly_weaker_than(arg_b, arg_a))
        dwl = WeakestLinkDemocraticOrdering(arg_theory.argumentation_system.rule_preference_dict,
                                            arg_theory.ordinary_premise_preference_dict)
        self.assertFalse(dwl.argument_is_strictly_weaker_than(arg_b, arg_a))
        self.assertTrue(ell.argument_is_strictly_weaker_than(arg_c, arg_b2))
        self.assertTrue(ewl.argument_is_strictly_weaker_than(arg_c, arg_b2))
        self.assertTrue(dll.argument_is_strictly_weaker_than(arg_c, arg_b2))
        self.assertTrue(dwl.argument_is_strictly_weaker_than(arg_c, arg_b2))

        self.assertFalse(arg_theory.defeats(arg_b, arg_a, ell))
        self.assertFalse(arg_theory.defeats(arg_c, arg_b, ell))
        self.assertFalse(arg_theory.defeats(arg_c, arg_b2_prime, ell))
        self.assertTrue(arg_theory.defeats(arg_b2, arg_c, ell))

        arg_d1 = InstantiatedArgument.observation_based(language['~d'])
        arg_d2 = InstantiatedArgument.defeasible_rule_based(DefeasibleRule(4, {language['~d']}, language['s'], 'd4'),
                                                            {arg_d1})
        arg_e = InstantiatedArgument.strict_rule_based(arg_theory.argumentation_system.strict_rules[1], {arg_b2})

        self.assertTrue(arg_theory.defeats(arg_d2, arg_b1_prime, ell))
        self.assertTrue(arg_theory.defeats(arg_d2, arg_b, ell))
        self.assertTrue(arg_theory.defeats(arg_d2, arg_b1, ell))
        self.assertTrue(arg_theory.defeats(arg_e, arg_a, ell))
