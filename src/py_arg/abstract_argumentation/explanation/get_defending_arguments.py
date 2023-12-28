from typing import TypeVar, FrozenSet, Set, List, Dict

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.explanation.\
    get_reachable_arguments_and_distances import \
    get_reachable_arguments_and_distances

T = TypeVar('T', bound=Argument)


def _is_reachable_by_even_path(distance_set: set[int]) -> bool:
    """
    Check if there is some even path in the distance_set.
    """
    return any(not distance % 2 for distance in distance_set)


def get_reachable_by_even_path(
        reachable_arguments: Set[T],
        distance_dictionary: Dict[T, Set[int]]
) -> Set[T]:
    return {
        other_argument for other_argument in reachable_arguments
        if _is_reachable_by_even_path(distance_dictionary[other_argument])
    }


def get_defending_arguments(
        argumentation_framework: AbstractArgumentationFramework,
        argument: T) -> Set[T]:
    """
    Obtain the set of arguments that (in)directly defend the argument.

    :param argumentation_framework: The argumentation framework containing
    the argument.
    :param argument: The argument for which we need an explanation.
    :return: The set of arguments that defends the argument.
    """
    reachable_arguments, distance_dict = get_reachable_arguments_and_distances(
        argumentation_framework, argument)
    return get_reachable_by_even_path(reachable_arguments, distance_dict)


def get_defending_arguments_in_extension(
        argumentation_framework: AbstractArgumentationFramework,
        argument: T,
        extension: FrozenSet[T]) -> \
        Set[T]:
    """
    Obtain for the extension those arguments that (in)directly defend the
    argument.

    In papers: Defending.

    :param argumentation_framework: the argumentation framework the explanation
        should be about.
    :param argument: the argument that is accepted.
    :param extension: the extensions for which we need the explanation.
    :return: a set of arguments, containing the arguments from the
        extension that (in)directly defend the argument.
    """
    defending = get_defending_arguments(argumentation_framework, argument)

    if argument not in extension:
        raise ValueError('This argument was not in the extension.')

    return defending.intersection(extension)


def get_defending_arguments_in_extensions(
        argumentation_framework: AbstractArgumentationFramework,
        argument: T,
        extensions: Set[FrozenSet[T]]) -> \
        List[Set[T]]:
    """
    Obtain for each extension with the argument the set of arguments that
    (in)directly defend the argument.

    In papers: Defending.

    :param argumentation_framework: the argumentation framework the explanation
        should be about
    :param argument: the argument that is accepted
    :param extensions: the extensions (sets of accepted arguments) of the
        argumentation framework.
    :return: a list of sets of arguments, each representing one or more
        extensions, containing the arguments from the
        extension that (in)directly defend the argument.
    """
    defending = get_defending_arguments(argumentation_framework, argument)
    defending_sets = []

    for extension in extensions:
        if argument in extension:
            defending_and_in_extension = defending.intersection(extension)
            if defending_and_in_extension not in defending_sets:
                defending_sets.append(defending_and_in_extension)

    return defending_sets


def get_directly_defending_arguments(
        argumentation_framework: AbstractArgumentationFramework,
        argument: Argument,
        extensions: Set[FrozenSet[T]]) -> \
        List[Set[T]]:
    """
    Obtain for each extension with the argument the set of arguments that
    directly defend the argument.

    In papers: DirDefending.

    :param argumentation_framework: the argumentation framework the explanation
        should be about
    :param argument: the argument that is accepted
    :param extensions: the extensions (sets of accepted arguments) of the
        argumentation framework.
    :return: a list of sets of arguments, each representing one or more
        extensions, containing the arguments from the
        extension that directly defend the argument.
    """
    reachable_arguments, distance_dict = get_reachable_arguments_and_distances(
        argumentation_framework, argument)

    directly_defending_arguments = {
        other_argument for other_argument in reachable_arguments
        if any(distance == 2 for distance in distance_dict[other_argument])
    }

    directly_defending_sets = []
    for extension in extensions:
        if argument in extension:
            ext_def = directly_defending_arguments.intersection(extension)
            if ext_def not in directly_defending_sets:
                directly_defending_sets.append(ext_def)

    return directly_defending_sets
