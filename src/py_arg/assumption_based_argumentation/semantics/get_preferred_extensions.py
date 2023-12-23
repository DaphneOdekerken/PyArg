from typing import Set, FrozenSet

from py_arg.assumption_based_argumentation.classes.aba_framework \
    import AssumptionBasedArgumentationFramework
import py_arg.abstract_argumentation.semantics.get_preferred_extensions as \
    get_preferred_extensions_af


def get_preferred_extensions(
        aba_framework: AssumptionBasedArgumentationFramework) -> \
        Set[FrozenSet[str]]:
    af = aba_framework.generate_af()
    af_extensions = get_preferred_extensions_af.get_preferred_extensions(af)
    abaf_extensions = set()
    for af_ext in af_extensions:
        aba_ext = set()
        for arg in af_ext:
            if arg.conclusion in aba_framework.assumptions:
                aba_ext.add(arg.conclusion)
        abaf_extensions.add(frozenset(aba_ext))

    return abaf_extensions
