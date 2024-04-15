from typing import TypeVar, FrozenSet, Set, Dict

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.explanation.\
    get_reachable_arguments_and_distances import \
    get_reachable_arguments_and_distances

T = TypeVar('T', bound=Argument)


def _is_reachable_by_odd_path(distance_set: set[int]) -> bool:
    """
    Check if there is some even path in the distance_set.
    """
    return any(distance % 2 for distance in distance_set)


def get_reachable_by_odd_path(
        reachable_arguments: Set[T],
        distance_dictionary: Dict[T, Set[int]]
) -> Set[T]:
    return {
        other_argument for other_argument in reachable_arguments
        if _is_reachable_by_odd_path(distance_dictionary[other_argument])
    }


def get_attackers_without_defense_in_extension(
        argumentation_framework: AbstractArgumentationFramework,
        argument: T,
        extension: FrozenSet[T]
) -> Set[T]:
    reachable_arguments, distance_dict = get_reachable_arguments_and_distances(
        argumentation_framework, argument)
    reachable_by_odd_from_a = get_reachable_by_odd_path(
        reachable_arguments, distance_dict)

    result = set()
    for candidate_attacker in reachable_by_odd_from_a:
        reachable_from_attacker, distance_dict_from_attacker = \
            get_reachable_arguments_and_distances(argumentation_framework,
                                                  candidate_attacker)
        reachable_by_odd_from_b = get_reachable_by_odd_path(
            reachable_from_attacker, distance_dict_from_attacker)
        if not extension.intersection(reachable_by_odd_from_b):
            result.add(candidate_attacker)
    return result


def get_attackers_without_defense_in_extensions(
        argumentation_framework: AbstractArgumentationFramework,
        argument: T,
        extensions: Set[FrozenSet[T]]) -> Set[FrozenSet[T]]:
    """
    Obtain for each extension without the argument the set of arguments that
    attack the argument and to which the extension provides no defense.
    In papers: NoDefAgainst.

    :param argumentation_framework: the argumentation framework the explanation
        should be about
    :param argument: the argument that is not accepted
    :param extensions: the extensions (sets of accepted arguments) of the
        argumentation framework.
    :return: a list of sets of arguments, each representing one or more
        extensions, containing the arguments that
        attack the argument and to which the extension provides to defense.
    """
    reachable_arguments, distance = get_reachable_arguments_and_distances(
        argumentation_framework, argument)
    reachable_by_odd_from_a = get_reachable_by_odd_path(
        reachable_arguments, distance)

    result = set()
    for extension in extensions:
        not_defending_for_extension = set()
        for candidate_attacker in reachable_by_odd_from_a:
            reachable_from_attacker, distance_dict_from_attacker = \
                get_reachable_arguments_and_distances(
                    argumentation_framework, candidate_attacker)
            reachable_by_odd_from_b = get_reachable_by_odd_path(
                reachable_from_attacker, distance_dict_from_attacker)
            if not extension.intersection(reachable_by_odd_from_b):
                not_defending_for_extension.add(candidate_attacker)
        not_defending_for_extension = frozenset(not_defending_for_extension)
        result.add(not_defending_for_extension)
    return result


def get_no_dir_defending(
        argumentation_framework: AbstractArgumentationFramework,
        argument: Argument,
        extensions):
    """
    Obtain for each extension without the argument the set of arguments that
    directly attack the argument and to which
    the extension provides no direct defense.
    In papers: NoDirDefense.

    :param argumentation_framework: the argumentation framework the explanation
    should be about
    :param argument: the argument that is not accepted
    :param extensions: the extensions (sets of accepted arguments) of the
    argumentation framework.
    :return: a list of sets of arguments, each representing one or more
    extensions, containing the arguments that
        directly attack the argument and to which the extension provides to
        direct defense.
    """
    not_dir_def_sets = []
    for extension in extensions:
        not_def_ext = set()
        if argument not in extension:
            for attacker in argumentation_framework. \
                    get_incoming_defeat_arguments(argument):
                if not [dirdf
                        for dirdf in
                        argumentation_framework.get_incoming_defeat_arguments(
                            attacker)
                        if dirdf in extension]:
                    not_def_ext.add(attacker)
            if not_def_ext not in not_dir_def_sets:
                not_dir_def_sets.append(not_def_ext)

    return not_dir_def_sets


def get_no_self_defense(
        argumentation_framework: AbstractArgumentationFramework,
        argument: Argument, extensions):
    """
    Obtain for each set obtained with get_not_defending the arguments that are
    not attacked by the argument.
    In papers: NoSelfDefense.

    :param argumentation_framework: the argumentation framework the explanation
        should be about
    :param argument: the argument that is not accepted
    :param extensions: the extensions (sets of accepted arguments) of the
        argumentation framework.
    :return: a list of sets of arguments, each representing one or more
        extensions, containing the arguments that attack
        the argument, to which the extension provides to defense and which the
        argument itself does not (in)directly
        attack either.
    """
    not_defending = get_attackers_without_defense_in_extensions(
        argumentation_framework, argument, extensions)

    not_dir_defending_sets = []
    for not_def_ext in not_defending:
        not_ddef_ext = set()
        for attacker in not_def_ext:
            reachable_attacker, distance_attacker = \
                get_reachable_arguments_and_distances(
                    argumentation_framework, attacker)
            defenders = set()
            for pot_defender in reachable_attacker:
                dist_pot_def = distance_attacker[pot_defender]
                for dist in dist_pot_def:
                    if dist % 2:
                        defenders.add(pot_defender)
            if argument not in defenders:
                not_ddef_ext.add(attacker)
        if not_ddef_ext not in not_dir_defending_sets:
            not_dir_defending_sets.append(not_ddef_ext)

    return not_dir_defending_sets
