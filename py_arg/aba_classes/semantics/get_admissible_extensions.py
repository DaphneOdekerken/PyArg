from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.algorithms.semantics.is_admissible as is_admissible_af
import py_arg.algorithms.canonical_constructions.aux_operators as aux


def apply(abaf: ABAF) -> Set[FrozenSet[str]]:
    af = abaf.generate_af()

    abaf_extensions = set()
    for ext in aux.powerset(abaf.assumptions):
        af_ext = set()
        for arg in af.arguments:
            if arg.premise.issubset(ext):
                af_ext.add(arg)
        if is_admissible_af.is_admissible(af_ext, af):
            abaf_extensions.add(ext)

    return abaf_extensions
