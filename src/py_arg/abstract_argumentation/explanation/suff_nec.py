from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.explanation.\
    get_reachable_arguments_and_distances import \
    get_reachable_arguments_and_distances
from py_arg.abstract_argumentation.semantics.get_admissible_sets import \
    get_admissible_sets


def get_sufficient_or_necessary(
        argumentation_framework: AbstractArgumentationFramework,
        argument: Argument,
        explanation_function: str,
        explanation_type: str):
    """
    Obtain the necessary or (minimal) sufficient explanations for the given
    argument.

    :param argumentation_framework: The argumentation framework the explanation
        should be about.
    :param argument: The argument that is accepted.
    :param explanation_function: The explanation function, to determine the
        content of the explanation.
    :param explanation_type: The explanation type, to determine acceptance/
        non-acceptance explanation.
    :return: a list of sets of arguments, each representing a sufficient set of
        arguments for the acceptance of the given argument, or the necessary
        arguments.
    """
    if explanation_type == 'Acceptance':
        if explanation_function == 'Suff':
            return get_sufficient_arguments_for_acceptance(
                argumentation_framework, argument)

        elif explanation_function == 'MinSuff':
            # TODO: Check what happens here, could be done more efficiently.
            sufficient_sets = get_sufficient_arguments_for_acceptance(
                argumentation_framework, argument)
            current_minimal_sufficient_explanations = []
            for sufficient_set in sufficient_sets:
                minsuff_suff = []
                for potential_minimal_sufficient_explanation in \
                        current_minimal_sufficient_explanations:
                    if potential_minimal_sufficient_explanation.issubset(
                            sufficient_set):
                        minsuff_suff.append(
                            potential_minimal_sufficient_explanation)
                    if sufficient_set.issubset(
                            potential_minimal_sufficient_explanation):
                        current_minimal_sufficient_explanations.remove(
                            potential_minimal_sufficient_explanation)
                        current_minimal_sufficient_explanations.append(
                            sufficient_set)
                if minsuff_suff == [] and sufficient_set not in \
                        current_minimal_sufficient_explanations:
                    current_minimal_sufficient_explanations.append(
                        sufficient_set)
            return current_minimal_sufficient_explanations

        elif explanation_function == 'Nec':
            return get_necessary_arguments_for_acceptance(
                argumentation_framework, argument)

    raise NotImplementedError


def get_sufficient_arguments_for_acceptance(
        arg_framework: AbstractArgumentationFramework, argument: Argument):
    """
    Obtain the sets with sufficient arguments for the acceptance of the given
    argument.

    :param arg_framework: The argumentation framework the explanation should
        be about.
    :param argument: The argument that is accepted.
    :return: a list of sets of arguments, each representing a sufficient set of
        arguments for the acceptance of the given argument.
    """
    sufficient_sets = []
    reach, dist = get_reachable_arguments_and_distances(
        arg_framework, argument)
    if dist[argument] == {0}:
        reach.remove(argument)
    admissible_sets = get_admissible_sets(arg_framework)
    adm_arg = [set(adm) for adm in admissible_sets if argument in adm]
    for adm in adm_arg:
        if argument not in reach:
            adm.remove(argument)
        if adm.issubset(reach):
            sufficient_sets.append(adm)

    return sufficient_sets


def get_necessary_arguments_for_acceptance(
        arg_framework: AbstractArgumentationFramework, argument: Argument):
    """
    Obtain the necessary arguments for the acceptance of the given argument.

    :param arg_framework: The argumentation framework the explanation should be
        about.
    :param argument: The argument that is accepted.
    :return: a list of arguments, necessary for the acceptance of the given
        argument.
    """
    reach, dist = get_reachable_arguments_and_distances(
        arg_framework, argument)
    admissible_sets = get_admissible_sets(arg_framework)
    adm_arg = [set(adm) for adm in admissible_sets if argument in adm]
    intersect_adm_arg = set.intersection(*adm_arg)
    if dist[argument] == {0}:
        intersect_adm_arg.remove(argument)
    nec_args = list(intersect_adm_arg)

    return nec_args
