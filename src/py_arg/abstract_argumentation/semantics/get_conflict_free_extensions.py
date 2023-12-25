from typing import Set
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument


def get_conflict_free_extensions(
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[frozenset[Argument]]:
    return _recursively_get_conflict_free(
        set(), set(argumentation_framework.arguments),
        argumentation_framework)


def _recursively_get_conflict_free(
        previous_cf: Set[Argument],
        todo: Set[Argument],
        argumentation_framework: AbstractArgumentationFramework) -> \
        Set[frozenset[Argument]]:
    if not todo:
        return set()

    new_cf = {frozenset(previous_cf)}
    for argument in todo:
        # If this argument is self-defeating, we will not add it to any
        # conflict-free set.
        if argument in argument.get_outgoing_defeat_arguments:
            continue

        new_todo = \
            {other_argument for other_argument in todo
             if other_argument != argument and
             not other_argument < argument and
             other_argument not in argument.get_ingoing_defeat_arguments and
             other_argument not in argument.get_outgoing_defeat_arguments}

        new_cf.add(frozenset(previous_cf.union({argument})))
        new_cf.update(_recursively_get_conflict_free(
            previous_cf.union({argument}), new_todo, argumentation_framework))

    return new_cf
