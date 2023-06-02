from typing import Set, Iterable

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.semantics.is_acceptable_with_respect_to import is_acceptable_with_respect_to


def get_acceptable_with_respect_to(argument_set: Iterable[Argument],
                                   argumentation_framework: AbstractArgumentationFramework) -> Set[Argument]:
    """
    Get the set of argument that is acceptable with respect to this set of arguments.

    :param argument_set: The set of arguments for which we want to find the acceptable arguments.
    :param argumentation_framework: Abstract argumentation framework.
    :return: The set of arguments that are acceptable w.r.t. this set of arguments.

    >>> a = Argument('a')
    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [a, b, c, d]
    >>> defeats = [Defeat(b, a), Defeat(c, b), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, defeats)
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
