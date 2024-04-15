from typing import Dict, Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.instantiated_argument \
    import InstantiatedArgument
from py_arg.assumption_based_argumentation.classes.rule import Rule
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.defeat import Defeat


class AssumptionBasedArgumentationFramework:
    def __init__(self,
                 assumptions: Set[str],
                 rules: Set[Rule],
                 language: Set[str],
                 contraries: Dict[str, str]):
        self.assumptions = assumptions
        self.rules = rules

        # Verify that every assumption is in the language.
        if any(assumption not in language for assumption in self.assumptions):
            raise ValueError('Some assumption is not in the language.')

        self.language = language

        # Verify that every item in the body or head of the rule is in the
        # language.
        for rule in rules:
            if any(rule_part not in self.language
                   for rule_part in rule.get_signature()):
                raise ValueError('Some part of the rule ' + str(rule) +
                                 ' is not in the language.')

        self.contraries = contraries

        # Verify that each assumption has a contrary.
        if any(assumption not in self.contraries.keys()
               for assumption in self.assumptions):
            raise ValueError('Some assumption does not have a contrary.')

        # Verify that each contrary element is in the language.
        if any(assumption not in self.assumptions or
               contrary not in self.language
               for assumption, contrary in self.contraries.items()):
            raise ValueError('Some contrary pair does not consist of an '
                             'assumption and an atom.')

        # Verify that the framework is flat (assumptions cannot be in the
        # rule head).
        self.is_flat = True
        for rule in rules:
            if rule.head in assumptions:
                self.is_flat = False
                raise ValueError('This ABA framework is not flat. At this '
                                 'point, we only support flat ABA.')

    def __eq__(self, other):
        return self.assumptions == other.assumptions and \
            self.rules == other.rules and \
            self.language == other.language and \
            all(literal.contraries_and_contradictories == other.language[
                lit_str].contraries_and_contradictories
                for lit_str, literal in self.language)

    def generate_af(self) -> AbstractArgumentationFramework:
        arguments = set()
        defeats = set()

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

            contrary = self.contraries[assumption]
            contrary_premises_set = self.recursively_construct_argument(
                self.rules, contrary, {contrary})

            for contrary_premise in contrary_premises_set:
                arguments.add(InstantiatedArgument('', set(contrary_premise),
                                                   contrary))

        for arg1 in arguments:
            for premise in arg1.premise:
                for arg2 in arguments:
                    if self.contraries[premise] == arg2.conclusion:
                        defeats.add(Defeat(arg2, arg1))

        return AbstractArgumentationFramework('', arguments=list(arguments),
                                              defeats=list(defeats))

    def generate_af_full(self) -> AbstractArgumentationFramework:
        arguments = set()
        defeats = set()

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

        for atom in self.language.difference(self.assumptions):

            atom_premises_set = self.recursively_construct_argument(
                self.rules, atom, {atom})

            for atom_premise in atom_premises_set:
                arguments.add(InstantiatedArgument(
                    '', set(atom_premise), atom))

        for arg1 in arguments:
            for premise in arg1.premise:
                for arg2 in arguments:
                    if self.contraries[premise] == arg2.conclusion:
                        defeats.add(Defeat(arg2, arg1))

        return AbstractArgumentationFramework('', arguments=list(arguments),
                                              defeats=list(defeats))

    def recursively_construct_argument(
            self, rules: Set[Rule], target: str, visited: Set[str]) -> \
            Set[FrozenSet]:
        """
        A premise of an argument is a minimal set of assumptions implying an
        atom. Premises of an atom are determined recursively, going through
        all rules implying the atom.
        """
        # First split the rules into relevant rules (having the target as
        # their head) and other rules.
        relevant_rules = set()
        rest_rules = set()
        for rule in rules:
            if rule.head == target:
                relevant_rules.add(rule)
            else:
                rest_rules.add(rule)

        premises_set = set()
        for rule in relevant_rules:
            assumptions_in_rule_body = {atom for atom in rule.body
                                        if atom in self.assumptions}
            rule_premises = {frozenset(assumptions_in_rule_body)}
            for atom in rule.body:
                if atom not in self.assumptions:
                    atom_rule_premises = self.recursively_construct_argument(
                                rest_rules, atom, visited.copy().union({atom}))
                    rule_premises = self.merge_premise_sets(rule_premises,
                                                            atom_rule_premises)
            premises_set = premises_set.union(rule_premises)

        return premises_set

    @staticmethod
    def merge_premise_sets(premise_set_set1: Set[frozenset],
                           premise_set_set2: Set[frozenset]):
        """
        Merge premise sets.
        """
        if not premise_set_set1:
            return premise_set_set2
        return {set_1.union(set_2)
                for set_1 in premise_set_set1
                for set_2 in premise_set_set2}

    def reduce(self):
        reduction = set()
        for rule in self.rules:
            if not any(other_rule.body < rule.body
                       for other_rule in self.rules
                       if other_rule.head == rule.head):
                reduction.add(rule)
        self.rules = reduction
