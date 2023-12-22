from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import AssumptionBasedArgumentationFramework
import py_arg.abstract_argumentation.semantics.is_admissible as is_admissible_af
import py_arg.abstract_argumentation.canonical_constructions.aux_operators as aux


def get_admissible_extensions(aba_framework: AssumptionBasedArgumentationFramework) -> Set[FrozenSet[str]]:
    af = aba_framework.generate_af()

    aba_framework_extensions = set()
    for ext in aux.powerset(aba_framework.assumptions):
        af_ext = set()
        for arg in af.arguments:
            if arg.premise.issubset(ext):
                af_ext.add(arg)
        if is_admissible_af.is_admissible(af_ext, af):
            aba_framework_extensions.add(ext)

    return aba_framework_extensions
