from typing import Dict, List, Optional, Set

from py_arg.aba_classes.rule import Rule
from py_arg.aba_classes.atom import Atom
from py_arg.aba_classes import instantiated_argument
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import *
from py_arg.abstract_argumentation_classes.defeat import *
from py_arg.abstract_argumentation_classes.argument import *


class ABAF:
    def __init__(self,
                 assumptions: Set[Atom],
                 rules: Set[Rule],
                 language: Set[Atom],
                 contraries: Dict[Atom, Atom]):
        self.assumptions = assumptions
        self.rules = rules

        if self.assumptions.difference(language).__len__() > 0:
            raise NotImplementedError

        self.language = language
        # self.language = language.union(assumptions)

        for rule in rules:
            if rule.get_signature().difference(self.language).__len__() > 0:
                raise NotImplementedError
            # self.language = language.union(rule.get_signature())

        self.contraries = contraries

        self.is_flat = True

        for rule in rules:
            if rule.head in assumptions:
                self.is_flat = False
                raise NotImplementedError

    def __eq__(self, other):
        return self.assumptions == other.assumptions and \
            self.rules == other.rules and \
            self.language == other.language and \
            all(literal.contraries_and_contradictories == other.language[lit_str].contraries_and_contradictories
                for lit_str, literal in self.language)

    def generate_af(self) -> AbstractArgumentationFramework:
        arguments = set()
        for assumption in self.assumptions:
            arguments.add(instantiated_argument.InstantiatedArgument('', {assumption}, assumption))

        for assumption in self.assumptions:
            premises_set = self.recursively_construct_argument(self.rules, assumption, {assumption})
            for p in premises_set:
                arguments.add(Argument(str(p)))

        return AbstractArgumentationFramework('', arguments=list(arguments), defeats=[])

    # I am basically reimplementing Prolog?
    # A premise of an argument is a minimal set of assumptions implying an atom
    # Premises of an atom are determined recursively, going through all rules implying the atom
    # Dealing with all the combinations makes the code a bit convoluted, but basically it is only backtracking
    def recursively_construct_argument(self, rules: Set[Rule], target: Atom, visited: Set[Atom]):
        premises_set = set()
        relevant_rules = set()
        rest_rules = set()

        for rule in rules:
            if rule.head == target:
                relevant_rules.add(rule)
            else:
                rest_rules.add(rule)

        for rule in relevant_rules:
            rule_premise = set()
            for atom in rule.body:
                if atom in self.assumptions:
                    rule_premise = self.merge(rule_premise, {frozenset({atom})})
                else:
                    rule_premise = self.merge(rule_premise,
                                              self.recursively_construct_argument(rest_rules,
                                                                                  atom, visited.copy().union({atom})))
            premises_set = premises_set.union(rule_premise)

        return premises_set

    # crossproductlike merge
    def merge(self, premise_set_set1: Set[frozenset], premise_set_set2: Set[frozenset]):
        out = set()
        for s1 in premise_set_set1:
            for s2 in premise_set_set2:
                out.add(s1.union(s2))
        return out
