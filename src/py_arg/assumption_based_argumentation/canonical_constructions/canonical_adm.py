from typing import Set

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.assumption_based_argumentation.canonical_constructions import \
    canonical_ucl, canonical_cf


def apply(extension_set: Set) -> AssumptionBasedArgumentationFramework:
    abaf_cf = canonical_cf.apply(extension_set)
    abaf_ucl = canonical_ucl.apply(extension_set)
    assumptions = abaf_cf.assumptions.union(abaf_ucl.assumptions)
    rules = abaf_cf.rules.union(abaf_ucl.rules)
    language = abaf_cf.language.union(abaf_ucl.language)
    contraries = abaf_cf.contraries
    contraries.update(abaf_ucl.contraries)

    return AssumptionBasedArgumentationFramework(assumptions, rules, language,
                                                 contraries)
