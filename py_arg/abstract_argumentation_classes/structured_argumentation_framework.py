from typing import Optional, List, Tuple

from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory


class StructuredArgumentationFramework:
    # TODO: Check if this is necessary; if so, add docstrings and tests.

    def __init__(self, name: str = '',
                 arguments: Optional[List[Argument]] = None,
                 attacks: Optional[List[Tuple[Argument, Argument]]] = None,
                 argument_preference_relation: Optional[List[Tuple[Argument, Argument]]] = None):
        self.name = name

        if arguments is None:
            self._arguments = {}
        else:
            self._arguments = {argument.name: argument for argument in arguments}

        if attacks is None:
            attacks = []
        self._incoming_attacks = {argument: set() for argument in self._arguments.values()}
        self._outgoing_attacks = {argument: set() for argument in self._arguments.values()}
        self._attack_table = {argument1: {argument2: False
                                          for argument2 in self._arguments.values()}
                              for argument1 in self._arguments.values()}
        for attack_from, attack_to in attacks:
            self._incoming_attacks[attack_to].add(attack_from)
            self._outgoing_attacks[attack_from].add(attack_to)
            self._attack_table[attack_from][attack_to] = True

        if argument_preference_relation is None:
            self._more_preferred_than = {argument: set() for argument in self._arguments.values()}
            self._less_preferred_than = {argument: set() for argument in self._arguments.values()}
            self._equally_preferred = {argument: {argument} for argument in self._arguments.values()}
        for less_preferred, more_preferred in argument_preference_relation:
            self._more_preferred_than[less_preferred].add(more_preferred)
            self._less_preferred_than[more_preferred].add(less_preferred)

    @classmethod
    def from_argumentation_theory(cls, name: str, argumentation_theory: ArgumentationTheory):
        return cls(name, argumentation_theory.all_arguments, argumentation_theory.all_attacks)
