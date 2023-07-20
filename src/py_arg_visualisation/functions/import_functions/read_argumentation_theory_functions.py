from typing import List, Tuple, Set

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.preference_preorder import PreferencePreorder
from py_arg.aspic_classes.strict_rule import StrictRule


def _read_axioms_and_ordinary_premises(axioms_or_ordinary_premises_str) -> List[str]:
    return [literal_str.strip() for literal_str in axioms_or_ordinary_premises_str.split()]


def _read_strict_rules(strict_rules_str) -> List[Tuple[str, Set[str], str]]:
    def read_strict_rule(rule_id, strict_rule_str) -> Tuple[str, Set[str], str]:
        if '->' not in strict_rule_str:
            raise ValueError('Each strict rule should contain -> at least once.')
        before_rule, after_rule = strict_rule_str.split('->', 1)
        antecedents = set(antecedent_str.strip() for antecedent_str in before_rule.split(','))
        if '->' in after_rule:
            raise ValueError('Each strict rule should contain -> only once.')
        consequent = after_rule.strip()
        return rule_id, antecedents, consequent

    return [read_strict_rule(str(rule_id), strict_rule_str)
            for rule_id, strict_rule_str in enumerate(strict_rules_str.splitlines())]


def _read_defeasible_rules(defeasible_rules_str: str) -> List[Tuple[str, Set[str], str]]:
    def read_defeasible_rule(named_defeasible_rule_str: str) -> Tuple[str, Set[str], str]:
        if ':' not in named_defeasible_rule_str:
            raise ValueError('The rule should have a rule name, preceding :.')
        name, defeasible_rule_str = named_defeasible_rule_str.split(':', 1)

        if '=>' not in defeasible_rule_str:
            raise ValueError('Each defeasible rule should contain => at least once.')
        before_rule, after_rule = defeasible_rule_str.split('=>', 1)

        antecedents = set(antecedent_str.strip() for antecedent_str in before_rule.split(','))
        if '=>' in after_rule:
            raise ValueError('Each defeasible rule should contain => only once.')
        consequent = after_rule.strip()

        return name, antecedents, consequent

    return [read_defeasible_rule(named_defeasible_rule_str)
            for named_defeasible_rule_str in defeasible_rules_str.splitlines()]


def _read_preferences(preferences_str: str) -> List[Tuple[str]]:
    def read_preference_rule(preference_str: str) -> Tuple:
        nr_smaller = preference_str.count('<')
        nr_larger = preference_str.count('>')
        if nr_smaller + nr_larger != 1:
            raise ValueError('Please write exactly one premise per line.')
        if '<' in preference_str:
            less, more = preference_str.split('<', 1)
        else:
            more, less = preference_str.split('>', 1)
        return less.strip(), more.strip()
    return [read_preference_rule(preference_str_rule) for preference_str_rule in preferences_str.splitlines()]


def read_argumentation_theory(axioms_str: str, ordinary_premises_str: str,
                              strict_rules_str: str, defeasible_rules_str: str,
                              premise_preferences_str: str, defeasible_rule_preference_str: str):
    """
    Calculate the argumentation theory from the axioms, ordinary premises, strict and defeasible rules, premise and
    rule preference and the given ordering

    :param axioms_str: The provided axioms (premises that cannot be attacked).
    :param ordinary_premises_str: The ordinary premises (premises that can be questioned).
    :param strict_rules_str: The provided strict rules (rules that cannot be attacked).
    :param defeasible_rules_str: The defeasible rules (rules that can be questioned).
    :param premise_preferences_str: The preferences over the ordinary premises.
    :param defeasible_rule_preference_str: The preferences over the defeasible rules.
    """

    # Read axioms, ordinary premises, defeasible rules and strict rules (first in a str format) from the strs
    axioms = _read_axioms_and_ordinary_premises(axioms_str)
    ordinary_premises = _read_axioms_and_ordinary_premises(ordinary_premises_str)
    defeasible_rules = _read_defeasible_rules(defeasible_rules_str)
    strict_rules = _read_strict_rules(strict_rules_str)

    # Derive the language: first obtain "absolute" literal strs from axioms and rules
    def get_absolute(non_absolute_literal_str: str) -> str:
        return non_absolute_literal_str.replace('~', '').replace('-', '')
    absolute_literal_strs = set()
    for literal in axioms + ordinary_premises:
        absolute_literal_strs.add(get_absolute(literal))
    for _, antecedents, consequent in strict_rules:
        for antecedent in antecedents:
            absolute_literal_strs.add(get_absolute(antecedent))
        absolute_literal_strs.add(get_absolute(consequent))
    for _, antecedents, consequent in defeasible_rules:
        for antecedent in antecedents:
            absolute_literal_strs.add(get_absolute(antecedent))
        absolute_literal_strs.add(get_absolute(consequent))

    # Derive the language: add all variations of the absolute literals
    language = {}
    contraries_and_contradictories = {}
    for literal_str in absolute_literal_strs:
        l_pos = Literal(literal_str)
        l_naf = Literal('~' + literal_str)
        l_neg = Literal('-' + literal_str)
        language[l_pos.s1] = l_pos
        language[l_naf.s1] = l_naf
        language[l_neg.s1] = l_neg

        # Derive the contradiction function
        contraries_and_contradictories[l_pos.s1] = {l_neg}
        contraries_and_contradictories[l_naf.s1] = {l_pos}
        contraries_and_contradictories[l_neg.s1] = {l_pos}

    # Read axioms, ordinary premises, defeasible rules and strict rules, now in the proper format
    axioms = [language[axiom_str] for axiom_str in axioms]
    ordinary_premises = [language[ordinary_premise_str] for ordinary_premise_str in ordinary_premises]
    defeasible_rules = [DefeasibleRule(rule_id, {language[antecedent] for antecedent in antecedents},
                                       language[consequent])
                        for rule_id, antecedents, consequent in defeasible_rules]
    strict_rules = [StrictRule(rule_id, {language[antecedent] for antecedent in antecedents}, language[consequent])
                    for rule_id, antecedents, consequent in strict_rules]

    # Read the ordinary premise preferences
    ordinary_premise_preference_strs = _read_preferences(premise_preferences_str)
    ordinary_premise_preferences = PreferencePreorder.create_reflexive_preorder(ordinary_premises)
    for less, more in ordinary_premise_preference_strs:
        less_literal = language[less]
        more_literal = language[more]
        ordinary_premise_preferences.append((less_literal, more_literal))

    # Read the defeasible rule preferences
    defeasible_rule_preference_strs = _read_preferences(defeasible_rule_preference_str)
    defeasible_rule_preferences = PreferencePreorder.create_reflexive_preorder(defeasible_rules)
    defeasible_rule_dict = {rule.id: rule for rule in defeasible_rules}
    for less, more in defeasible_rule_preference_strs:
        less_rule = defeasible_rule_dict[less]
        more_rule = defeasible_rule_dict[more]
        defeasible_rule_preferences.append((less_rule, more_rule))

    argumentation_system = ArgumentationSystem(language, contraries_and_contradictories, strict_rules,
                                               defeasible_rules, defeasible_rule_preferences)
    argumentation_theory = ArgumentationTheory(argumentation_system, axioms, ordinary_premises,
                                               ordinary_premise_preferences)
    return argumentation_theory
