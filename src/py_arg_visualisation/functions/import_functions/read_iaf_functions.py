from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.incomplete_argumentation_frameworks.classes.incomplete_argumentation_framework import \
    IncompleteArgumentationFramework


def read_incomplete_argumentation_framework(
        certain_arguments_str: str, certain_attacks_str: str,
        uncertain_arguments_str: str, uncertain_attacks_str: str):
    """
    Calculate the incomplete argumentation framework from the given
    (certain and uncertain) arguments and attacks between them.

    :param certain_arguments_str: The provided certain arguments.
    :param certain_attacks_str: The provided certain attacks.
    :param uncertain_arguments_str: The provided uncertain arguments.
    :param uncertain_attacks_str: The provided uncertain attacks.
    """
    certain_arg_list = [Argument(arg) for arg in
                        certain_arguments_str.replace(',', '').split()]
    uncertain_arg_list = [Argument(arg) for arg in
                          uncertain_arguments_str.replace(',', '').split()]
    arg_list = certain_arg_list + uncertain_arg_list

    certain_defeat_list = []
    uncertain_defeat_list = []

    for attack in certain_attacks_str.splitlines():
        att_list = attack.replace(' ', '').replace(')', '').replace('(', '').\
            split(',')
        if len(att_list) == 2 and att_list[0] != '' and att_list[1] != '':
            from_argument = Argument(att_list[0])
            to_argument = Argument(att_list[1])
            if from_argument not in arg_list or to_argument not in arg_list:
                raise ValueError('Not a valid attack, since one of the '
                                 'arguments does not exist.')
            certain_defeat_list.append(Defeat(Argument(att_list[0]),
                                              Argument(att_list[1])))
    for attack in uncertain_attacks_str.splitlines():
        att_list = attack.replace(' ', '').replace(')', '').replace('(', '').\
            split(',')
        if len(att_list) == 2 and att_list[0] != '' and att_list[1] != '':
            from_argument = Argument(att_list[0])
            to_argument = Argument(att_list[1])
            if from_argument not in arg_list or to_argument not in arg_list:
                raise ValueError('Not a valid attack, since one of the '
                                 'arguments does not exist.')
            uncertain_defeat_list.append(Defeat(Argument(att_list[0]),
                                                Argument(att_list[1])))

    arg_framework = IncompleteArgumentationFramework(
        'AF', certain_arg_list, uncertain_arg_list,
        certain_defeat_list, uncertain_defeat_list)
    return arg_framework
