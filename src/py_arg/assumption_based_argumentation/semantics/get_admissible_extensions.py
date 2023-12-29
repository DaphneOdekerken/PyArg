from typing import Set, FrozenSet

from py_arg.abstract_argumentation.semantics.is_admissible import is_admissible
from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
from py_arg.utils.powerset import powerset


def get_admissible_extensions(
        aba_framework: AssumptionBasedArgumentationFramework) -> \
        Set[FrozenSet[str]]:
    af = aba_framework.generate_af()

    aba_framework_extensions = set()
    for assumption_subset in powerset(aba_framework.assumptions):
        potential_extension = {argument for argument in af.arguments
                               if argument.premise <= assumption_subset}
        if is_admissible(potential_extension, af):
            aba_framework_extensions.add(assumption_subset)

    return aba_framework_extensions
