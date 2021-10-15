from typing import Set

from ASPIC.abstract_argumentation_classes.defeat import Defeat
from ASPIC.semantics.get_acceptable_with_respect_to import get_acceptable_with_respect_to
from ASPIC.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from ASPIC.abstract_argumentation_classes.argument import Argument
from ASPIC.utils.fixpoint import get_least_fixed_point


def get_grounded_extension(argumentation_framework: AbstractArgumentationFramework) -> Set[Argument]:
    """

    :param argumentation_framework:
    :return:

    >>> a = Argument('a')
    >>> b = Argument('b')
    >>> c = Argument('c')
    >>> d = Argument('d')
    >>> arguments = [a, b, c, d]
    >>> attacks = [Defeat(b, a), Defeat(c, b), Defeat(d, c)]
    >>> af = AbstractArgumentationFramework('af', arguments, attacks)
    >>> ge = get_grounded_extension(af)
    >>> a in ge
    False
    >>> b in ge
    True
    >>> c in ge
    False
    >>> d in ge
    True
    """
    return get_least_fixed_point(lambda x: get_acceptable_with_respect_to(x, argumentation_framework), set())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
