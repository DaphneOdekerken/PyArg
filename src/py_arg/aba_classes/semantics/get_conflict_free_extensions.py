from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.algorithms.canonical_constructions.aux_operators as aux


def apply(abaf: ABAF) -> Set[FrozenSet[str]]:
    abaf_extensions = set()
    af = abaf.generate_af()
    for ext in aux.powerset(abaf.assumptions):
        cf = True
        for arg in af.arguments:
            if arg.premise.issubset(ext):
                for asm in ext:
                    if abaf.contraries[asm] == arg.conclusion:
                        cf = False
        if cf:
            abaf_extensions.add(ext)

    return abaf_extensions
