from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat


def read_argumentation_framework(arguments_str: str, attacks_str: str):
    """
    Calculate the abstract argumentation framework from the given arguments and
    attacks between them.

    :param arguments_str: The provided arguments.
    :param attacks_str: The provided attacks.
    """
    arg_list = [Argument(arg)
                for arg in arguments_str.replace(',', '').split()]
    defeat_list = []

    for attack in attacks_str.splitlines():
        att_list = attack.replace(' ', '').replace(')', '').replace('(', '').\
            split(',')
        if len(att_list) == 2 and att_list[0] != '' and att_list[1] != '':
            from_argument = Argument(att_list[0])
            to_argument = Argument(att_list[1])
            if from_argument not in arg_list or to_argument not in arg_list:
                raise ValueError('Not a valid defeat, since one of the '
                                 'arguments does not exist.')
            defeat_list.append(Defeat(Argument(att_list[0]),
                                      Argument(att_list[1])))

    arg_framework = AbstractArgumentationFramework('AF', arg_list, defeat_list)
    return arg_framework
