from typing import Set

from ASPIC.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from ASPIC.abstract_argumentation_classes.argument import Argument
from ASPIC.abstract_argumentation_classes.defeat import Defeat


def is_acceptable_with_respect_to(argument: Argument, argument_set: Set[Argument],
                                  argumentation_framework: AbstractArgumentationFramework) -> bool:
    return all(any([attacker_attacker in argument_set
                    for attacker_attacker in argumentation_framework.get_incoming_defeat_arguments(attacker)])
               for attacker in argumentation_framework.get_incoming_defeat_arguments(argument))


def get_acceptable_with_respect_to(argument_set: Set[Argument],
                                   argumentation_framework: AbstractArgumentationFramework) -> Set[Argument]:
    """

    :param argument_set:
    :param argumentation_framework:
    :return:

    >>> a = Argument('a')
    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [a, b, c, d]
    >>> attacks = [Defeat(b, a), Defeat(c, b), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, attacks)
    >>> acc_set = get_acceptable_with_respect_to(set(), af)
    >>> d in acc_set
    True
    >>> a in acc_set or b in acc_set or c in acc_set
    False
    >>> acc_set = get_acceptable_with_respect_to({d}, af)
    >>> d in acc_set
    True
    >>> b in acc_set
    True
    """
    return {argument for argument in argumentation_framework.arguments
            if is_acceptable_with_respect_to(argument, argument_set, argumentation_framework)}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
