from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.algorithms.semantics.get_grounded_extension as get_grounded_extensions_af


def apply(abaf: ABAF) -> Set[FrozenSet[str]]:
    af = abaf.generate_af()
    af_extension = get_grounded_extensions_af.get_grounded_extension(af)
    abaf_ext = set()
    for arg in af_extension:
        if arg.conclusion in abaf.assumptions:
            abaf_ext.add(arg.conclusion)

    return {frozenset(abaf_ext)}
