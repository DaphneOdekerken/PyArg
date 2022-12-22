from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.algorithms.explanation.defending import get_defending, get_dir_defending
from py_arg.algorithms.explanation.not_defending import get_not_defending, get_no_dir_defending, get_no_self_defense
from py_arg.algorithms.explanation.suff_nec import get_suff_nec


def get_argumentation_framework_explanations(arg_framework: AbstractArgumentationFramework, semantics, extensions, accepted, function, expl_type, strategy):
    """
    Calculate, for each argument, the explanations, given the function, type and strategy.

    :param arg_framework: The argumentation framework the explanation has to be calculated from.
    :param semantics: The semantics used to determine (non-)acceptance.
    :param extensions: The sets of accepted arguments in arg_framework, based on semantics.
    :param accepted: The arguments that are considered accepted given the extensions and strategy.
    :param function: The explanation function, to determine the content of the explanation.
    :param expl_type: The explanation type, to determine acceptance/non-acceptance explanation.
    :param strategy: The strategy of the explanation, whether credulous or skeptical reasoning.
    :return: A dictionary with for each (non-)accepted argument its explanation, given the parameters.
    """
    explanation = {}
    not_accepted = [arg for arg in arg_framework.arguments if arg not in accepted]
    if expl_type == 'Acc':
        for arg in accepted:
            if function == 'Defending':
                explanation[str(arg)] = get_defending(arg_framework, arg, extensions)
            elif function == 'DirDefending':
                explanation[str(arg)] = get_dir_defending(arg_framework, arg, extensions)
            else:
                explanation[str(arg)] = get_suff_nec(arg_framework, arg, function, expl_type)
        return explanation

    elif expl_type == 'NonAcc':
        for arg in not_accepted:
            if function == 'NoDefAgainst':
                explanation[str(arg)] = get_not_defending(arg_framework, arg, extensions)
            elif function == 'NoDirDefense':
                explanation[str(arg)] = get_no_dir_defending(arg_framework, arg, extensions)
            elif function == 'NoSelfDefense':
                explanation[str(arg)] = get_no_self_defense(arg_framework, arg, extensions)
        return explanation
