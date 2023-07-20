from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.algorithms.semantics.get_complete_extensions as get_complete_extensions_af


def apply(abaf: ABAF) -> Set[FrozenSet[str]]:
    af = abaf.generate_af()
    af_extensions = get_complete_extensions_af.get_complete_extensions(af)
    abaf_extensions = set()
    for af_ext in af_extensions:
        aba_ext = set()
        for arg in af_ext:
            if arg.conclusion in abaf.assumptions:
                aba_ext.add(arg.conclusion)
        abaf_extensions.add(frozenset(aba_ext))

    return abaf_extensions
