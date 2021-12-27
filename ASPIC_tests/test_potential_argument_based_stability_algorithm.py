import unittest

from ASPIC.aspic_classes.argumentation_system import ArgumentationSystem
from ASPIC.aspic_classes.defeasible_rule import DefeasibleRule
from ASPIC.aspic_classes.last_link_ordering import LastLinkElitistOrdering
from ASPIC.aspic_classes.literal import Literal
from ASPIC.aspic_classes.preference import Preference
from ASPIC.dynamic_aspic_classes.potential_argumentation_theory import PotentialArgumentationTheory
from ASPIC.dynamic_aspic_classes.queryable import Queryable
from ASPIC.labels.enum_stability_label import EnumStabilityLabel
from ASPIC.labels.potential_argument_label import PotentialArgumentLabel
from ASPIC.stability.potential_argument_based_stability_algorithm import \
    potential_argument_based_stability_algorithm_from_potential_argumentation_theory, \
    from_potential_argument_labels_to_literal_labels


def get_test_argumentation_system() -> ArgumentationSystem:
    # Get all literals
    queryable_literal_strs = ['complaint', 'bought', 'paid', 'received', 'trusted']
    non_queryable_literal_strs = ['fraud', 'reject', 'accept']
    pos_queryables = {literal_str: Queryable(literal_str) for literal_str in queryable_literal_strs}
    neg_queryables = {'~' + literal_str: Queryable('~' + literal_str) for literal_str in queryable_literal_strs}
    pos_literals = {literal_str: Literal(literal_str) for literal_str in non_queryable_literal_strs}
    neg_literals = {'~' + literal_str: Literal('~' + literal_str) for literal_str in non_queryable_literal_strs}
    all_literals = dict(pos_queryables, **neg_queryables, **pos_literals, **neg_literals)

    # Add contraries
    contraries = dict()
    for literal_str in pos_queryables.keys():
        contraries[literal_str] = {neg_queryables['~' + literal_str]}
        contraries['~' + literal_str] = {pos_queryables[literal_str]}
    for literal_str in pos_literals.keys():
        contraries[literal_str] = {neg_literals['~' + literal_str]}
        contraries['~' + literal_str] = {pos_literals[literal_str]}
    contraries['accept'].add(all_literals['reject'])
    contraries['reject'].add(all_literals['accept'])

    # Add strict rules (there are none)
    strict_rules = []

    # Add defeasible rules
    d1 = DefeasibleRule(1, {all_literals['bought'], all_literals['paid'], all_literals['~received']},
                        all_literals['fraud'], 'd1')
    d2 = DefeasibleRule(2, {all_literals['complaint']}, all_literals['reject'], 'd2')
    d3 = DefeasibleRule(3, {all_literals['complaint'], all_literals['fraud']}, all_literals['accept'], 'd3')
    defeasible_rules = [d1, d2, d3]

    # Add literals corresponding to defeasible rules
    for defeasible_rule in defeasible_rules:
        defeasible_rule_literal = Literal.from_defeasible_rule(defeasible_rule)
        defeasible_rule_literal_negation = Literal.from_defeasible_rule_negation(defeasible_rule)
        all_literals[str(defeasible_rule_literal)] = defeasible_rule_literal
        all_literals[str(defeasible_rule_literal_negation)] = defeasible_rule_literal_negation
        contraries[str(defeasible_rule_literal)] = [defeasible_rule_literal_negation]
        contraries[str(defeasible_rule_literal_negation)] = [defeasible_rule_literal]

    # Add additional undercutter (defeasible rule)
    d4 = DefeasibleRule(4, {all_literals['trusted']}, all_literals['-d1'], 'd4')
    defeasible_rules.append(d4)
    defeasible_rule_literal = Literal.from_defeasible_rule(d4)
    defeasible_rule_literal_negation = Literal.from_defeasible_rule_negation(d4)
    all_literals[str(defeasible_rule_literal)] = defeasible_rule_literal
    all_literals[str(defeasible_rule_literal_negation)] = defeasible_rule_literal_negation
    contraries[str(defeasible_rule_literal)] = [defeasible_rule_literal_negation]
    contraries[str(defeasible_rule_literal_negation)] = [defeasible_rule_literal]

    # Rule preference
    defeasible_rule_preferences = [Preference(d2, '<', d3)]

    # Connect "parents and children"
    for rule in strict_rules + defeasible_rules:
        rule.consequent.children.append(rule)
        for child in rule.antecedents:
            child.parents.append(rule)

    arg_sys = ArgumentationSystem(all_literals, contraries, strict_rules, defeasible_rules,
                                  defeasible_rule_preferences)
    return arg_sys


class TestPotentialArgumentBasedStabilityAlgorithm(unittest.TestCase):
    def test1(self):
        arg_sys = get_test_argumentation_system()
        lan = arg_sys.language
        knowledge_base_axioms = [lan[lit] for lit in ['bought', 'paid', '~received']]
        knowledge_base_normal_premises = []
        queryables = [literal for literal in lan.values() if isinstance(literal, Queryable)]

        ordering = LastLinkElitistOrdering(arg_sys.rule_preference_dict, {})
        potential_argumentation_theory = \
            PotentialArgumentationTheory(arg_sys, knowledge_base_axioms, knowledge_base_normal_premises, queryables)
        potential_argument_labels = potential_argument_based_stability_algorithm_from_potential_argumentation_theory(
            potential_argumentation_theory, ordering)

        for potential_argument, potential_argument_label in potential_argument_labels.items():
            if str(potential_argument.conclusion) == 'complaint':
                self.assertEqual(potential_argument_label, PotentialArgumentLabel(False, False, True, False, False))
            elif str(potential_argument.conclusion) in ['bought', 'paid', '~received']:
                self.assertEqual(potential_argument_label, PotentialArgumentLabel(True, True, True, False, False))
            elif str(potential_argument.conclusion) in ['~bought', '~paid', 'received']:
                self.assertEqual(potential_argument_label, PotentialArgumentLabel(False, False, False, True, True))
            elif str(potential_argument.conclusion) == 'fraud':
                self.assertEqual(potential_argument_label, PotentialArgumentLabel(True, False, True, False, True))
            elif str(potential_argument.conclusion) == 'accept':
                self.assertEqual(potential_argument_label, PotentialArgumentLabel(False, False, True, False, False))
            elif str(potential_argument.conclusion) == 'reject':
                self.assertEqual(potential_argument_label, PotentialArgumentLabel(False, False, True, False, False))

        labels = from_potential_argument_labels_to_literal_labels(potential_argument_labels, arg_sys.language)

        self.assertEqual(labels[lan['bought']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['~bought']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['complaint']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['~complaint']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['fraud']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['accept']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['reject']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['trusted']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['~accept']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['~reject']], EnumStabilityLabel.UNSATISFIABLE)

        knowledge_base_axioms = [lan[lit] for lit in ['bought', 'paid', '~received', 'trusted']]
        potential_argumentation_theory = \
            PotentialArgumentationTheory(arg_sys, knowledge_base_axioms, knowledge_base_normal_premises, queryables)
        potential_argument_labels = potential_argument_based_stability_algorithm_from_potential_argumentation_theory(
            potential_argumentation_theory, ordering)
        labels = from_potential_argument_labels_to_literal_labels(potential_argument_labels, arg_sys.language)

        self.assertEqual(labels[lan['-d1']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['~trusted']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['complaint']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['~complaint']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['fraud']], EnumStabilityLabel.OUT)
        self.assertEqual(labels[lan['accept']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['reject']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['trusted']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['~accept']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['~reject']], EnumStabilityLabel.UNSATISFIABLE)

        knowledge_base_axioms = [lan[lit] for lit in ['bought', 'paid', '~received', 'trusted', 'complaint']]
        potential_argumentation_theory = \
            PotentialArgumentationTheory(arg_sys, knowledge_base_axioms, knowledge_base_normal_premises, queryables)
        potential_argument_labels = potential_argument_based_stability_algorithm_from_potential_argumentation_theory(
            potential_argumentation_theory, ordering)
        labels = from_potential_argument_labels_to_literal_labels(potential_argument_labels, arg_sys.language)

        self.assertEqual(labels[lan['-d1']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['~trusted']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['complaint']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['~complaint']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['fraud']], EnumStabilityLabel.OUT)
        self.assertEqual(labels[lan['accept']], EnumStabilityLabel.OUT)
        self.assertEqual(labels[lan['reject']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['trusted']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['~accept']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['~reject']], EnumStabilityLabel.UNSATISFIABLE)

        knowledge_base_axioms = [lan[lit] for lit in ['complaint']]
        potential_argumentation_theory = \
            PotentialArgumentationTheory(arg_sys, knowledge_base_axioms, knowledge_base_normal_premises, queryables)
        potential_argument_labels = potential_argument_based_stability_algorithm_from_potential_argumentation_theory(
            potential_argumentation_theory, ordering)
        labels = from_potential_argument_labels_to_literal_labels(potential_argument_labels, arg_sys.language)

        self.assertEqual(labels[lan['-d1']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['complaint']], EnumStabilityLabel.DEFENDED)
        self.assertEqual(labels[lan['~complaint']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['fraud']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['accept']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['reject']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['trusted']], EnumStabilityLabel.UNSTABLE)
        self.assertEqual(labels[lan['~accept']], EnumStabilityLabel.UNSATISFIABLE)
        self.assertEqual(labels[lan['~reject']], EnumStabilityLabel.UNSATISFIABLE)
