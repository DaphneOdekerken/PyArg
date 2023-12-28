from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.canonical_af\
    .canonical_def as canonical_def
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_conflict_sensitive
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if is_conflict_sensitive(extension_set) and frozenset() in extension_set:
        return canonical_def.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
