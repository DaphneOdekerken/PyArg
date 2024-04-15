from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
import py_arg.abstract_argumentation.semantics.get_stable_extensions as \
    get_stable_extensions_af


def get_stable_extensions(
        aba_framework: AssumptionBasedArgumentationFramework) -> \
        Set[FrozenSet[str]]:
    af = aba_framework.generate_af()
    af_extensions = get_stable_extensions_af.get_stable_extensions(af)

    aba_framework_extensions = set()
    for af_extension in af_extensions:
        aba_extension = frozenset({
            argument.conclusion for argument in af_extension
            if argument.conclusion in aba_framework.assumptions
        })
        aba_framework_extensions.add(aba_extension)

    return aba_framework_extensions
