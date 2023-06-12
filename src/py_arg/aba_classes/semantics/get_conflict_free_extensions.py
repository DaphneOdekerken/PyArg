from typing import Set, FrozenSet

from src.py_arg.aba_classes.aba_framework import ABAF
from src import py_arg as aux


def apply(abaf: ABAF) -> Set[FrozenSet[str]]:
    abaf_extensions = set()
    for ext in aux.powerset(abaf.assumptions):
        cf = True
        for r in abaf.rules:
            if r.body.issubset(ext):
                for asm in ext:
                    if abaf.contraries[asm] == r.head:
                        cf = False
        if cf:
            abaf_extensions.add(ext)

    return abaf_extensions
