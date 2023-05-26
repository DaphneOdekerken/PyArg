from typing import Dict, List, Optional, Set

from py_arg.aba_classes.rule import Rule
from py_arg.aba_classes.atom import Atom
from py_arg.aba_classes import instantiated_argument
from py_arg.abstract_argumentation_classes import argument, defeat, abstract_argumentation_framework

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

    def generate_af(self):
        arguments = set()
        for assumption in self.assumptions:
            arguments.add(instantiated_argument.InstantiatedArgument('', {assumption}, assumption))

        for assumption in self.assumptions:
            self.recursively_find_attacker(self, self.rules, {self.contraries[assumption]})

    # I am basically reimplementing Prolog?
    def recursively_find_attacker(self, rules: Set[Rule], goals: Set[Atom]):
        return
