from typing import Set, TypeVar
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.get_conflict_free_extensions \
    import get_conflict_free_extensions

T = TypeVar('T', bound=Argument)


def get_naive_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[frozenset[T]]:
    conflict_free_extensions = \
        get_conflict_free_extensions(argumentation_framework)

    naive_extensions = {
        extension for extension in conflict_free_extensions
        if not any(other_extension > extension
                   for other_extension in conflict_free_extensions)
    }

    return naive_extensions
