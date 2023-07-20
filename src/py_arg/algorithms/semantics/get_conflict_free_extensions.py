from typing import Set
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument


def apply(argumentation_framework: AbstractArgumentationFramework) -> Set[frozenset[Argument]]:
    return recursively_get_cf(set(), set(argumentation_framework.arguments), argumentation_framework)


def recursively_get_cf(in_: Set[Argument], todo: Set[Argument],
                       af: AbstractArgumentationFramework) -> Set[frozenset[Argument]]:
    if len(todo) == 0:
        return set()

    out = {frozenset(in_)}
    for arg in todo:
        if arg in arg.get_outgoing_defeat_arguments:
            continue
        rec_todo = set(todo.copy())
        rec_todo.remove(arg)
        rm = set()
        for a in rec_todo:
            if a < arg or a in arg.get_outgoing_defeat_arguments or a in arg.get_ingoing_defeat_arguments:
                rm.add(a)
        rec_todo.difference_update(rm)
        out.add(frozenset(in_.union({arg})))
        out.update(recursively_get_cf(in_.union({arg}), rec_todo, af))

    return out
