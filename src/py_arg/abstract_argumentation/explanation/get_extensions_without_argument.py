from typing import TypeVar, Set, FrozenSet

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.semantics.\
    get_argumentation_framework_extensions import \
    get_argumentation_framework_extensions

T = TypeVar('T', bound=Argument)


def filter_argumentation_framework_extensions_without_argument(
        all_extensions: Set[FrozenSet[T]],
        argument: T) -> Set[FrozenSet[T]]:
    """
    Select only those extensions not containing the given argument.

    :param all_extensions: All extensions, computed earlier.
    :param argument: The argument that should be absent from each extension
    that is left in the result.
    """
    return {frozen_extension for frozen_extension in all_extensions
            if argument not in frozen_extension}


def get_argumentation_framework_extensions_without_argument(
        argumentation_framework: AbstractArgumentationFramework,
        semantics_specification: str,
        argument: T) -> Set[FrozenSet[T]]:
    """
    Calculate the set of extensions from the given abstract argumentation
    framework and chosen semantics, and select only those extensions
    not containing the given argument.

    :param argumentation_framework: The abstract argumentation framework.
    :param semantics_specification: The chosen semantics.
    :param argument: The argument that is required to be absent from the output
    extensions.
    """
    all_extensions = get_argumentation_framework_extensions(
        argumentation_framework, semantics_specification)
    return filter_argumentation_framework_extensions_without_argument(
        all_extensions, argument)
