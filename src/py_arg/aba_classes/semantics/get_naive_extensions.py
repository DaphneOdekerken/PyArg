from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg as get_naive_extensions_af


def apply(abaf: ABAF) -> Set[FrozenSet[str]]:
    af = abaf.generate_af()
    af_extensions = get_naive_extensions_af.apply(af)
    abaf_extensions = set()
    for af_ext in af_extensions:
        aba_ext = set()
        for arg in af_ext:
            if arg.conclusion in abaf.assumptions:
                aba_ext.add(arg.conclusion)
        abaf_extensions.add(frozenset(aba_ext))

    return abaf_extensions
