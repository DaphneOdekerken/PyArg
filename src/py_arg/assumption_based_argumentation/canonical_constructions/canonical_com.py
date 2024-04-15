from typing import Set

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.classes.rule import Rule
import py_arg.abstract_argumentation.canonical_constructions.aux_operators as \
    aux
import py_arg.assumption_based_argumentation.canonical_constructions.\
    canonical_adm as canonical_adm


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    extension_set_star = \
        aux.downward_closure(aux.reduce(extension_set)).intersection(
            aux.ucl(aux.reduce(extension_set)))
    assumptions = set(aux.big_a(extension_set))
    abaf_adm_star = canonical_adm.apply(extension_set_star)

    assumptions = assumptions.union(abaf_adm_star.assumptions)
    contraries = {}
    language = set()
    for a in assumptions:
        a_c = a + '_c'
        language.add(a)
        language.add(a_c)
        contraries[a] = a_c

    rules = abaf_adm_star.rules
    for ext_a, ext_b in aux.tuples(aux.reduce(extension_set).difference(
            frozenset())):
        for a in aux.unique_big_c(frozenset(set(ext_a).union(set(ext_b))),
                                  aux.reduce(extension_set)):
            x_a_c = 'χ_' + a + '_c'
            rules.add(Rule('', set(ext_a).union(set(ext_b)), x_a_c))

    return AssumptionBasedArgumentationFramework(assumptions, rules, language,
                                                 contraries)
