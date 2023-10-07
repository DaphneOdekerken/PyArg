from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.algorithms.semantics.get_grounded_extension as get_grounded_extensions_af


def get_preferred_extensions(aba_framework: ABAF) -> Set[FrozenSet[str]]:
    af = aba_framework.generate_af()
    af_extension = get_grounded_extensions_af.get_grounded_extension(af)
    aba_framework_extensions = set()
    for arg in af_extension:
        if arg.conclusion in aba_framework.assumptions:
            aba_framework_extensions.add(arg.conclusion)

    return {frozenset(aba_framework_extensions)}
