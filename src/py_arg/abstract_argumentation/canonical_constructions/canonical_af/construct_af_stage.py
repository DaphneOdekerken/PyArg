from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.canonical_af\
    .canonical_st as canonical_st
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_incomparable, is_tight
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework


def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if is_incomparable(extension_set) and is_tight(
            extension_set) and len(extension_set) != 0:
        return canonical_st.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
