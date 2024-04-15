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
            rules.add(Rule('', ext,
                           contraries[corresponding_self_attackers[a]]))

    return AssumptionBasedArgumentationFramework(assumptions, rules, language,
                                                 contraries)
