
from typing import Set

from src.py_arg.aba_classes.aba_framework import ABAF
from src.py_arg.aba_classes.rule import Rule
from src import py_arg as aux


@staticmethod
def apply(extension_set: Set) -> ABAF:
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

    return ABAF(assumptions, rules, language, contraries)
