from typing import Set

from py_arg.abstract_argumentation.semantics.get_acceptable_with_respect_to \
    import get_acceptable_with_respect_to
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.utils.fixpoint import get_least_fixed_point


def get_grounded_extension(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[Argument]:
    return get_least_fixed_point(
        lambda x: get_acceptable_with_respect_to(x, argumentation_framework),
        set())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
