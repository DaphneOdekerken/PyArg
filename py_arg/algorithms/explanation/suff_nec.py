from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.algorithms.semantics import get_admissible_sets
from py_arg.algorithms.explanation.reach_and_dist import get_reach


def get_suff_nec(argumentation_framework: AbstractArgumentationFramework, argument: Argument, function, expl_type):
    """
    Obtain the necessary or (minimal) sufficient explanations for the given argument.

    :param argumentation_framework: The argumentation framework the explanation should be about.
    :param argument: The argument that is accepted.
    :param function: The explanation function, to determine the content of the explanation.
    :param expl_type: The explanation type, to determine acceptance/non-acceptance explanation.
    :return: a list of sets of arguments, each representing a sufficient set of arguments for the acceptance of the
    given argument, or the necessary arguments.
    """
    if expl_type == 'Acc':
        if function == 'Suff':
            nec_suff_expl = get_suff_acc(argumentation_framework, argument)

        elif function == 'MinSuff':
            suff_sets = get_suff_acc(argumentation_framework, argument)
            nec_suff_expl = []
            for suff in suff_sets:
                minsuff_suff = []
                for minsuff in nec_suff_expl:
                    if minsuff.issubset(suff):
                        minsuff_suff.append(minsuff)
                    if suff.issubset(minsuff):
                        nec_suff_expl.remove(minsuff)
                        nec_suff_expl.append(suff)
                if minsuff_suff == [] and suff not in nec_suff_expl:
                    nec_suff_expl.append(suff)

        elif function == 'Nec':
            nec_suff_expl = get_nec_acc(argumentation_framework, argument)

    return nec_suff_expl


def get_suff_acc(arg_framework: AbstractArgumentationFramework, argument: Argument):
    """
    Obtain the sets with sufficient arguments for the acceptance of the given argument.

    :param arg_framework: The argumentation framework the explanation should be about.
    :param argument: The argument that is accepted.
    :return: a list of sets of arguments, each representing a sufficient set of arguments for the acceptance of the
    given argument.
    """
    suff_sets = []
    reach, dist = get_reach(arg_framework, argument)
    if dist[str(argument)] == {0}:
        reach.remove(argument)
    admissible_sets = get_admissible_sets(arg_framework)
    adm_arg = [set(adm) for adm in admissible_sets if argument in adm]
    for adm in adm_arg:
        if argument not in reach:
            adm.remove(argument)
        if adm.issubset(reach):
            suff_sets.append(adm)

    return suff_sets


def get_nec_acc(arg_framework: AbstractArgumentationFramework, argument: Argument):
    """
    Obtain the necessary arguments for the acceptance of the given argument.

    :param arg_framework: The argumentation framework the explanation should be about.
    :param argument: The argument that is accepted.
    :return: a list of arguments, necessary for the acceptance of the given argument.
    """
    reach, dist = get_reach(arg_framework, argument)
    admissible_sets = get_admissible_sets(arg_framework)
    adm_arg = [set(adm) for adm in admissible_sets if argument in adm]
    intersect_adm_arg = set.intersection(*adm_arg)
    if dist[str(argument)] == {0}:
        intersect_adm_arg.remove(argument)
    nec_args = list(intersect_adm_arg)

    return nec_args