from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.utils.powerset import powerset


def get_conflict_free_extensions(
        aba_framework: AssumptionBasedArgumentationFramework) -> \
        Set[FrozenSet[str]]:
    af = aba_framework.generate_af()

    aba_framework_extensions = set()
    for assumption_set in powerset(aba_framework.assumptions):
        if all(all(aba_framework.contraries[assumption] != argument.conclusion
                   for assumption in assumption_set)
               for argument in af.arguments
               if argument.premise <= assumption_set):
            aba_framework_extensions.add(assumption_set)

    return aba_framework_extensions
