from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument


def get_reach(argumentation_framework: AbstractArgumentationFramework, argument: Argument):
    """
    Obtain the arguments in the framework from which the argument can be reach via the attack relation and the distance
    between those arguments.

    :param argumentation_framework: The argumentation framework used to determine reach and distance.
    :param argument: The argument for which the reach and distance need to be calculated.
    :return: A set of arguments from which the argument can be reached and a dictionary with for each argument in the
        framework the distance (possibly several) to the given argument.
    """
    initial_reach = {argument}
    distance = {}
    for arg in argumentation_framework.arguments:
        distance[str(arg)] = set()
    distance[str(argument)] = {0}
    return recursive_reach(argumentation_framework, initial_reach, argument, argument, 0, [], distance)


def recursive_reach(argumentation_framework, reach, argument, new_argument, dist, visited, distance):
    """
    Obtain the arguments in the framework from which the argument can be reach via the attack relation and the
    distance between those arguments.

    :param argumentation_framework: The argumentation framework used to determine reach and distance.
    :param reach: A set of arguments from which the argument is reachable.
    :param argument: The argument for which the reach and distance need to be calculated.
    :param new_argument: An argument from argumentation_framework from which the argument is reachable.
    :param dist: the depth of the current search step.
    :param visited: a list of defeats that has been used by the algorithm.
    :param distance: the dictionary with the distances.
    :return: A set of arguments from which the argument can be reached and a dictionary with for each argument in the
        framework the distance (possibly several) to the given argument.
    """
    visited_start = visited.copy()
    for pot_argument in argumentation_framework.arguments:
        if pot_argument in argumentation_framework.get_incoming_defeat_arguments(new_argument) \
                and [str(pot_argument), str(new_argument)] not in visited:
            pot_dist = distance[str(pot_argument)]
            pot_dist.add(dist + 1)
            distance[str(pot_argument)] = pot_dist
            reach.add(pot_argument)
            visited.append([str(pot_argument), str(new_argument)])
            recursive_reach(argumentation_framework, reach, argument, pot_argument, dist + 1, visited, distance)
            visited = visited_start

    return reach, distance
