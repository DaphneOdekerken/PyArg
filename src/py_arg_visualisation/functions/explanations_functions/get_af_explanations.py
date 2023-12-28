from typing import List, Set

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.explanation.get_defending_arguments \
    import get_defending_arguments_in_extensions, \
    get_directly_defending_arguments
from py_arg.abstract_argumentation.explanation.get_attackers_without_defense \
    import get_attackers_without_defense_in_extensions, get_no_dir_defending, \
    get_no_self_defense
from py_arg.abstract_argumentation.explanation.suff_nec \
    import get_sufficient_or_necessary


def get_argumentation_framework_explanations(
        arg_framework: AbstractArgumentationFramework,
        extensions: List[Set],
        accepted_arguments: Set, explanation_function: str,
        explanation_type: str):
    """
    Calculate, for each argument, the explanations, given the function, type
    and strategy.

    :param arg_framework: The argumentation framework the explanation has to be
     calculated from.
    :param extensions: The sets of accepted arguments in arg_framework, based
    on semantics.
    :param accepted_arguments: The arguments that are considered accepted given
    the extensions and strategy.
    :param explanation_function: The explanation function, to determine the
    content of the explanation.
    :param explanation_type: The explanation type, to determine
    acceptance/non-acceptance explanation.
    :return: A dictionary with for each (non-)accepted argument its
     explanation, given the parameters.
    """
    explanation = {}
    if explanation_type == 'Acceptance':
        for arg in accepted_arguments:
            if explanation_function == 'Defending':
                explanation[str(arg)] = get_defending_arguments_in_extensions(
                    arg_framework, arg, extensions)
            elif explanation_function == 'DirDefending':
                explanation[str(arg)] = get_directly_defending_arguments(
                    arg_framework, arg, extensions)
            else:
                explanation[str(arg)] = get_sufficient_or_necessary(
                    arg_framework, arg, explanation_function,
                    explanation_type)
        return explanation

    elif explanation_type == 'NonAcceptance':
        not_accepted_arguments = [arg for arg in arg_framework.arguments
                                  if arg not in accepted_arguments]
        for arg in not_accepted_arguments:
            if explanation_function == 'NoDefAgainst':
                explanation[str(arg)] = \
                    get_attackers_without_defense_in_extensions(
                        arg_framework, arg, extensions)
            elif explanation_function == 'NoDirDefense':
                explanation[str(arg)] = get_no_dir_defending(
                    arg_framework, arg, extensions)
            elif explanation_function == 'NoSelfDefense':
                explanation[str(arg)] = get_no_self_defense(
                    arg_framework, arg, extensions)
        return explanation
