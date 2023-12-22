from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework import AssumptionBasedArgumentationFramework
import py_arg.abstract_argumentation.semantics.get_stable_extensions as get_stable_extensions_af


def get_stable_extensions(aba_framework: AssumptionBasedArgumentationFramework) -> Set[FrozenSet[str]]:
    af = aba_framework.generate_af()
    af_extensions = get_stable_extensions_af.get_stable_extensions(af)
    aba_framework_extensions = set()
    for af_ext in af_extensions:
        aba_ext = set()
        for arg in af_ext:
            if arg.conclusion in aba_framework.assumptions:
                aba_ext.add(arg.conclusion)
        aba_framework_extensions.add(frozenset(aba_ext))

    return aba_framework_extensions
