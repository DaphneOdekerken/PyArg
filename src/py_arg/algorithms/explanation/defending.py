from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.algorithms.explanation.reach_and_dist import get_reach


def get_defending(argumentation_framework: AbstractArgumentationFramework, argument: Argument, extensions):
    """
    Obtain for each extension with the argument te set of arguments that (in)directly defend the argument.

    In papers: Defending.

    :param argumentation_framework: the argumentation framework the explanation should be about
    :param argument: the argument that is accepted
    :param extensions: the extensions (sets of accepted arguments) of the argumentation framework.
    :return: a list of sets of arguments, each representing one or more extensions, containing the arguments from the
        extension that (in)directly defend the argument.
    """
    reach, distance = get_reach(argumentation_framework, argument)

    defending = set()
    defending_sets = []
    for pot_def_arg in reach:
        dist_pot_arg = distance[str(pot_def_arg)]
        for dist in dist_pot_arg:
            if not dist % 2:
                defending.add(pot_def_arg)
                break

    for extension in extensions:
        if argument in extension:
            ext_def = defending.intersection(extension)
            if ext_def not in defending_sets:
                defending_sets.append(ext_def)

    return defending_sets


def get_dir_defending(argumentation_framework: AbstractArgumentationFramework, argument: Argument, extensions):
    """
    Obtain for each extension with the argument te set of arguments that directly defend the argument.

    In papers: DirDefending.

    :param argumentation_framework: the argumentation framework the explanation should be about
    :param argument: the argument that is accepted
    :param extensions: the extensions (sets of accepted arguments) of the argumentation framework.
    :return: a list of sets of arguments, each representing one or more extensions, containing the arguments from the
        extension that directly defend the argument.
    """
    reach, distance = get_reach(argumentation_framework, argument)

    defending = set()
    defending_sets = []
    for pot_def_arg in reach:
        dist_pot_arg = distance[str(pot_def_arg)]
        for dist in dist_pot_arg:
            if dist == 2:
                defending.add(pot_def_arg)
                break

    for extension in extensions:
        if argument in extension:
            ext_def = defending.intersection(extension)
            if ext_def not in defending_sets:
                defending_sets.append(ext_def)

    return defending_sets
