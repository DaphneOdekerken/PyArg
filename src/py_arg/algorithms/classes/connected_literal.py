from typing import Union

from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


def connect_parents_and_children(
        argumentation_theory: Union[ArgumentationTheory,
                                    IncompleteArgumentationTheory]):
    parents = {literal_str: set() for literal_str in
               argumentation_theory.argumentation_system.language}
    children = {literal_str: set() for literal_str in
                argumentation_theory.argumentation_system.language}
    for rule in argumentation_theory.argumentation_system.rules:
        for antecedent in rule.antecedents:
            parents[antecedent.s1].add(rule)
        children[rule.consequent.s1].add(rule)
    return parents, children
