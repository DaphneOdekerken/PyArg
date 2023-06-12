from typing import Set, FrozenSet

from src.py_arg.aba_classes.aba_framework import ABAF
from src import py_arg as is_admissible_af, py_arg as aux


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
