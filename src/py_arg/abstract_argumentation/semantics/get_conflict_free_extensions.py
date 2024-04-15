from typing import Set, TypeVar
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument

T = TypeVar('T', bound=Argument)


def get_conflict_free_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[frozenset[T]]:
    return _recursively_get_conflict_free(
        set(), set(argumentation_framework.arguments),
        argumentation_framework)


def _recursively_get_conflict_free(
        previous_cf: Set[T],
        todo: Set[T],
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[frozenset[T]]:
    if not todo:
        return set()

    new_cf = {frozenset(previous_cf)}
    for argument in todo:
        # If this argument is self-defeating, we will not add it to any
        # conflict-free set.
        if argument in argumentation_framework.\
                get_outgoing_defeat_arguments(argument):
            continue

        new_todo = \
            {other_argument for other_argument in todo
             if other_argument != argument and
             not other_argument < argument and
             other_argument not in
             argumentation_framework.get_incoming_defeat_arguments(
                 argument) and
             other_argument not in
             argumentation_framework.get_outgoing_defeat_arguments(argument)}

        new_cf.add(frozenset(previous_cf.union({argument})))
        new_cf.update(_recursively_get_conflict_free(
            previous_cf.union({argument}), new_todo, argumentation_framework))

    return new_cf
