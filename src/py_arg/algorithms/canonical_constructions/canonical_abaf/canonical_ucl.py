
from typing import Set

from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes.rule import Rule
import py_arg.algorithms.canonical_constructions.aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> ABAF:
    assumptions = set(aux.big_a(extension_set))
    language = assumptions.copy()
    contraries = {}
    rules = set()

    corresponding_self_attackers = {}
    new_assumptions = set()
    for a in assumptions:
        a_c = a + '_c'
        language.add(a_c)
        contraries[a] = a_c

        x_a = 'χ_' + a
        x_a_c = 'χ_' + a + '_c'
        new_assumptions.add(x_a)
        language.add(x_a)
        language.add(x_a_c)
        contraries[x_a] = x_a_c
        rules.add(Rule('', {x_a}, contraries[x_a]))
        rules.add(Rule('', {x_a}, a_c))

        corresponding_self_attackers[a] = x_a
    assumptions.update(new_assumptions)

    for ext in extension_set:
        for a in ext:
            rules.add(Rule('', ext, contraries[corresponding_self_attackers[a]]))

    return ABAF(assumptions, rules, language, contraries)
