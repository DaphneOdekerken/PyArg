
from typing import Set

from py_arg.aba_classes.aba_framework import ABAF
from py_arg.aba_classes.rule import Rule
from py_arg.aba_classes.atom import Atom
import py_arg.algorithms.canonical_constructions.aux_operators as aux


@staticmethod
def apply(extension_set: Set) -> ABAF:
    assumptions = set(aux.big_a(extension_set))
    language = assumptions.copy()
    contraries = {}
    rules = set()

    corresponding_self_attackers = {}

    for a in assumptions:
        a_c = Atom(a.name + '_c')
        language.add(a_c)
        contraries[a] = a_c

        x_a = Atom('x_' + a.name)
        x_a_c = Atom('x_' + a.name + '_c')
        assumptions.add(x_a)
        language.add(x_a)
        language.add(x_a_c)
        contraries[x_a] = x_a_c
        rules.add(Rule('', {x_a}, contraries[x_a]))
        rules.add(Rule('', {x_a}, a))

        corresponding_self_attackers[a] = x_a

    for ext in extension_set:
        for a in ext:
            rules.add(Rule('', ext, contraries[corresponding_self_attackers[a]]))

    return ABAF(assumptions, rules, language, contraries)
