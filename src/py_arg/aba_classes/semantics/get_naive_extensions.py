from typing import Set, FrozenSet

from py_arg.aba_classes.aba_framework import ABAF
import py_arg.aba_classes.semantics.get_conflict_free_extensions as get_conflict_free_extensions


def get_naive_extensions(aba_framework: ABAF) -> Set[FrozenSet[str]]:
    cf_ext = get_conflict_free_extensions.get_conflict_free_extensions(aba_framework)
    rm = set()
    for ext1 in cf_ext:
        for ext2 in cf_ext:
            if ext1.issubset(ext2) and not ext2.issubset(ext1):
                rm.add(ext1)
    return cf_ext.difference(rm)
