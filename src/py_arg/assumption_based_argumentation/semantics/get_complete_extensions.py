from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import \
    AssumptionBasedArgumentationFramework
import py_arg.abstract_argumentation.semantics.get_complete_extensions as \
    get_complete_extensions_af


def get_complete_extensions(
        aba_framework: AssumptionBasedArgumentationFramework) -> \
        Set[FrozenSet[str]]:
    af = aba_framework.generate_af()
    af_extensions = get_complete_extensions_af.get_complete_extensions(af)
    aba_framework_extensions = set()
    for af_ext in af_extensions:
        aba_extension = {argument.conclusion for argument in af_ext
                         if argument.conclusion in aba_framework.assumptions}
        aba_framework_extensions.add(frozenset(aba_extension))

    return aba_framework_extensions
