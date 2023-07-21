
from typing import Set

from py_arg.aba_classes.aba_framework import ABAF
from py_arg.algorithms.canonical_constructions.canonical_abaf import canonical_cf
from py_arg.algorithms.canonical_constructions.canonical_abaf import canonical_ucl


@staticmethod
def apply(extension_set: Set) -> ABAF:
    abaf_cf = canonical_cf.apply(extension_set)
    abaf_ucl = canonical_ucl.apply(extension_set)
    assumptions = abaf_cf.assumptions.union(abaf_ucl.assumptions)
    rules = abaf_cf.rules.union(abaf_ucl.rules)
    language = abaf_cf.language.union(abaf_ucl.language)
    contraries = abaf_cf.contraries
    contraries.update(abaf_ucl.contraries)

    return ABAF(assumptions, rules, language, contraries)
