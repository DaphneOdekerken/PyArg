from typing import Dict, Set

from py_arg.aba_classes.instantiated_argument import InstantiatedArgument
from py_arg.aba_classes.rule import Rule
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import \
    AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.defeat import Defeat


class ABAF:
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

        # Verify that every item in the body or head of the rule is in the language.
        for rule in rules:
            if any(rule_part not in self.language for rule_part in rule.get_signature()):
                raise ValueError('Some part of the rule ' + str(rule) + ' is not in the language.')

        self.contraries = contraries

        # Verify that each assumption has a contrary.
        if any(assumption not in self.contraries.keys() for assumption in self.assumptions):
            raise ValueError('Some assumption does not have a contrary.')

        # Verify that each contrary element is in the language.
        if any(assumption not in self.assumptions or contrary not in self.language
               for assumption, contrary in self.contraries.items()):
            raise ValueError('Some contrary pair does not consist of an assumption and an atom.')

        # Verify that the framework is flat (assumptions cannot be in the rule head).
        self.is_flat = True
        for rule in rules:
            if rule.head in assumptions:
                self.is_flat = False
                raise ValueError('This ABA framework is not flat. At this point, we only support flat ABA.')

    def __eq__(self, other):
        return self.assumptions == other.assumptions and \
            self.rules == other.rules and \
            self.language == other.language and \
            all(literal.contraries_and_contradictories == other.language[lit_str].contraries_and_contradictories
                for lit_str, literal in self.language)

    def generate_af(self) -> AbstractArgumentationFramework:
        arguments = set()
        defeats = set()

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

            contrary = self.contraries[assumption]
            contrary_premises_set = self.recursively_construct_argument(self.rules, contrary, {contrary})

            for contrary_premise in contrary_premises_set:
                arguments.add(InstantiatedArgument('', set(contrary_premise), contrary))

        for arg1 in arguments:
            for premise in arg1.premise:
                for arg2 in arguments:
                    # if arg1 != arg2 and self.contraries[premise] == arg2.conclusion:
                    if self.contraries[premise] == arg2.conclusion:
                        arg1.add_ingoing_defeat(arg2)
                        arg2.add_outgoing_defeat(arg1)
                        defeats.add(Defeat(arg2, arg1))

        return AbstractArgumentationFramework('', arguments=list(arguments), defeats=list(defeats))

    def generate_af_full(self) -> AbstractArgumentationFramework:
        arguments = set()
        defeats = set()

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

        for assumption in self.assumptions:
            arguments.add(InstantiatedArgument('', {assumption}, assumption))

        for atom in self.language.difference(self.assumptions):

            atom_premises_set = self.recursively_construct_argument(self.rules, atom, {atom})

            for atom_premise in atom_premises_set:
                arguments.add(InstantiatedArgument('', set(atom_premise), atom))

        for arg1 in arguments:
            for premise in arg1.premise:
                for arg2 in arguments:
                    # if arg1 != arg2 and self.contraries[premise] == arg2.conclusion:
                    if self.contraries[premise] == arg2.conclusion:
                        arg1.add_ingoing_defeat(arg2)
                        arg2.add_outgoing_defeat(arg1)
                        defeats.add(Defeat(arg2, arg1))

        return AbstractArgumentationFramework('', arguments=list(arguments), defeats=list(defeats))

    # I am basically reimplementing Prolog?
    # A premise of an argument is a minimal set of assumptions implying an atom
    # Premises of an atom are determined recursively, going through all rules implying the atom
    # Dealing with all the combinations makes the code a bit convoluted, but basically it is only backtracking
    def recursively_construct_argument(self, rules: Set[Rule], target: str, visited: Set[str]):
        premises_set = set()
        relevant_rules = set()
        rest_rules = set()

        for rule in rules:
            if rule.head == target:
                relevant_rules.add(rule)
            else:
                rest_rules.add(rule)

        for rule in relevant_rules:
            rule_premises = set()
            if len(rule.body) == 0:
                rule_premises.add(frozenset())
            asm = set()
            for atom in rule.body:
                if atom in self.assumptions:
                    asm.add(atom)
            rule_premises = {frozenset(asm)}
            for atom in rule.body:
                if atom not in self.assumptions:
                    rule_premises = self.merge(rule_premises,
                                               self.recursively_construct_argument(rest_rules,
                                                                                   atom,
                                                                                   visited.copy().union({atom})))
            premises_set = premises_set.union(rule_premises)

        return premises_set

    # crossproductlike merge
    def merge(self, premise_set_set1: Set[frozenset], premise_set_set2: Set[frozenset]):
        if len(premise_set_set1) == 0:
            return premise_set_set2
        out = set()
        for s1 in premise_set_set1:
            for s2 in premise_set_set2:
                out.add(s1.union(s2))
        return out

    def reduce(self):
        rm = set()
        for rule1 in self.rules:
            for rule2 in self.rules:
                if rule1.head == rule2.head and rule1.body.issubset(rule2.body) and not rule2.body.issubset(rule1.body):
                    rm.add(rule2)
        self.rules = self.rules.difference(rm)
