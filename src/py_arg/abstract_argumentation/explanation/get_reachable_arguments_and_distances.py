from typing import TypeVar, Tuple, Set, Dict, List

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat

T = TypeVar('T', bound=Argument)


def get_reachable_arguments_and_distances(
        argumentation_framework: AbstractArgumentationFramework,
        from_argument: T) -> Tuple[Set[T], Dict[T, Set[int]]]:
    """
    Obtain the arguments in the framework from which the argument can be
    reached via the attack relation and the distance between those arguments.

    :param argumentation_framework: The argumentation framework used to
    determine reach and distance.
    :param from_argument: The argument for which the reach and distance need
    to be calculated.
    :return: A set of arguments from which the argument can be reached and a
    dictionary with for each argument in the framework the distances to the
    given argument.
    """
    # Initialise the reachable_arguments with only the argument we start from.
    reachable_arguments = set()

    # Initialize the distance dictionary.
    distance = {}
    for arg in argumentation_framework.arguments:
        distance[arg] = set()
    distance[from_argument] = {0}

    def _recursive_reach(
            from_argument_round: T,
            new_argument: T,
            current_distance: int,
            visited: List[Defeat]):
        """
        Obtain the arguments in the framework from which the argument can be
        reached via the attack relation and the distance between
        those arguments.

        :param from_argument_round: The argument for which the reach and
        distance need to be calculated.
        :param new_argument: An argument from argumentation_framework from
            which the argument is reachable.
        :param current_distance: the depth of the current search step.
        :param visited: a list of defeats that has been used by the algorithm.
        """
        nonlocal argumentation_framework
        nonlocal reachable_arguments
        nonlocal distance

        original_visited = visited.copy()
        for potential_defeat in argumentation_framework.get_incoming_defeats(
                new_argument):
            if potential_defeat not in visited:
                potential_defeat_source = potential_defeat.from_argument

                # Update the distance dictionary.
                potential_distance = distance[potential_defeat_source]
                potential_distance.add(current_distance + 1)
                distance[potential_defeat_source] = potential_distance

                # Update the reachable arguments.
                reachable_arguments.add(potential_defeat_source)

                # Update the visited defeats.
                visited.append(potential_defeat)

                # Recursively update.
                _recursive_reach(from_argument_round, potential_defeat_source,
                                 current_distance + 1, visited)

                # Restore the originally visited arguments.
                visited = original_visited

    _recursive_reach(from_argument, from_argument, 0, [])
    return reachable_arguments, distance
