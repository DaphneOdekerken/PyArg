from typing import Iterable, TypeVar

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument

T = TypeVar('T', bound=Argument)


def is_acceptable_with_respect_to(
        argument: T, argument_set: Iterable[T],
        argumentation_framework: AbstractArgumentationFramework) -> bool:
    """
    Verify that the argument is acceptable with respect to the argument set in
    the abstract argumentation framework.

    :param argument: Argument for which we want to know if it is acceptable.
    :param argument_set: Argument set for which we want to know if the argument
        is acceptable w.r.t. this set.
    :param argumentation_framework: Argumentation framework in which the
        arguments occur.
    :return: Is the argument acceptable w.r.t. the argument set?
    """
    return all(any([
        attacker_attacker in argument_set
        for attacker_attacker in argumentation_framework.
        get_incoming_defeat_arguments(attacker)])
        for attacker in argumentation_framework.
        get_incoming_defeat_arguments(argument))
