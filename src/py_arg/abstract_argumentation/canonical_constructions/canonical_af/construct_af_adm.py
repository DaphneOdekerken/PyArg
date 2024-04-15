from typing import Set

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_def import get_canonical_def_framework
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_conflict_sensitive
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


def construct_argumentation_framework_admissible(extension_set: Set) -> \
        AbstractArgumentationFramework:
    if is_conflict_sensitive(extension_set) and frozenset() in extension_set:
        return get_canonical_def_framework(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
