
from typing import Set

from src.py_arg.aba_classes.aba_framework import ABAF
from src.py_arg.aba_classes.rule import Rule
from src import py_arg as aux, py_arg as canonical_adm


@staticmethod
def apply(extension_set: Set) -> ABAF:
    extension_set_star = aux.dcl(aux.reduce(extension_set)).intersection(aux.ucl(aux.reduce(extension_set)))

    abaf_adm_star = canonical_adm.apply(extension_set_star)
    abaf_adm = canonical_adm.apply(extension_set)

    assumptions = abaf_adm.assumptions.union(abaf_adm_star.assumptions)
    rules = abaf_adm_star.rules
    language = abaf_adm.language.union(abaf_adm_star.language)
    contraries = abaf_adm.contraries
    contraries.update(abaf_adm_star.contraries)

    for ext_a, ext_b in aux.tuples(aux.reduce(extension_set).difference(frozenset())):
        for a in aux.unique_big_c(frozenset(set(ext_a).union(set(ext_b))), aux.reduce(extension_set)):
            x_a_c = 'x_' + a + '_c'
            rules.add(Rule('', set(ext_a).union(set(ext_b)), x_a_c))

    return ABAF(assumptions, rules, language, contraries)

