from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import AssumptionBasedArgumentationFramework
import py_arg.abstract_argumentation.canonical_constructions.aux_operators as aux


def get_conflict_free_extensions(aba_framework: AssumptionBasedArgumentationFramework) -> Set[FrozenSet[str]]:
    aba_framework_extensions = set()
    af = aba_framework.generate_af()
    for ext in aux.powerset(aba_framework.assumptions):
        cf = True
        for arg in af.arguments:
            if arg.premise.issubset(ext):
                for asm in ext:
                    if aba_framework.contraries[asm] == arg.conclusion:
                        cf = False
        if cf:
            aba_framework_extensions.add(ext)

    return aba_framework_extensions
