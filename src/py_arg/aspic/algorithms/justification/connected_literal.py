from typing import Union

from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic.classes.literal import Literal
from py_arg.incomplete_aspic.classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


class ConnectedLiteral(Literal):
    def __init__(self, literal_str: str):
        super().__init__(literal_str)
        self.init_connected_literal()

    def init_connected_literal(self):
        self.children = []
        self.parents = []

    def __eq__(self, other):
        return self.s1 == other.s1

    def __hash__(self):
        return self.s1_hash


def connect_parents_and_children(
        argumentation_theory: Union[
            ArgumentationTheory, IncompleteArgumentationTheory]):
    for literal in argumentation_theory.argumentation_system.language.values():
        literal.__class__ = ConnectedLiteral
        literal.init_connected_literal()
    all_rules = argumentation_theory.argumentation_system.defeasible_rules + \
        argumentation_theory.argumentation_system.strict_rules
    for rule in all_rules:
        for antecedent in rule.antecedents:
            antecedent.parents.append(rule)
        rule.consequent.children.append(rule)
