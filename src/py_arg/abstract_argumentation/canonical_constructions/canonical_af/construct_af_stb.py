from typing import Set

import py_arg.abstract_argumentation.canonical_constructions.canonical_af\
    .canonical_st as canonical_st
from py_arg.abstract_argumentation.canonical_constructions.check_properties \
    import is_tight, is_incomparable, is_non_empty
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat


def apply(extension_set: Set) -> AbstractArgumentationFramework:
    if not is_non_empty(extension_set):
        x = Argument('x')
        return AbstractArgumentationFramework('', arguments=[x],
                                              defeats=[Defeat(x, x)])
    if is_incomparable(extension_set) and is_tight(extension_set):
        return canonical_st.apply(extension_set)
    return AbstractArgumentationFramework('', arguments=[], defeats=[])
