from typing import Set

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.classes.rule import Rule
import py_arg.abstract_argumentation.canonical_constructions.aux_operators as \
    aux


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    assumptions = set(aux.big_a(extension_set))
    language = assumptions.copy()
    contraries = {}
    for a in assumptions:
        a_c = a + '_c'
        language.add(a_c)
        contraries[a] = a_c

    rules = set()
    for ext in extension_set:
        for a in assumptions.difference(ext):
            rules.add(Rule('', ext, contraries[a]))

    return AssumptionBasedArgumentationFramework(assumptions, rules, language,
                                                 contraries)
