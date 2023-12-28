from typing import Set, FrozenSet

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_cf import get_canonical_cf_framework
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat


def conjunctive_defense_formula(extension_set: Set, argument: Argument) -> \
        Set[FrozenSet]:
    return {
        extension.copy().difference({argument})
        for extension in extension_set
        if argument in extension
    }


def disjunctive_defence_formula(extension_set: Set, arg: Argument) -> \
        Set[FrozenSet]:
    cnf = conjunctive_defense_formula(extension_set, arg)
    dnf = {frozenset()}
    for conjunct in cnf:
        if not conjunct:
            return set()
        old_dnf = dnf
        new_dnf = set()
        for disjunct in old_dnf:
            for d in conjunct:
                new_elem = set(disjunct)
                new_elem.add(d)
                new_dnf.add(frozenset(new_elem))
        dnf = new_dnf

    non_minimal = {d1 for d1 in dnf if any(d2 < d1 for d2 in dnf)}

    return dnf.difference(non_minimal)


def get_canonical_def_framework(extension_set: Set) -> \
        AbstractArgumentationFramework:
    canon_cf = get_canonical_cf_framework(extension_set)
    atts_cf = canon_cf.defeats
    args_cf = canon_cf.arguments

    atts_def = atts_cf.copy()
    args_def = args_cf.copy()

    for arg in args_cf:
        arg_dnf = disjunctive_defence_formula(extension_set, arg)
        for disj in arg_dnf:
            new_arg = Argument(str(arg) + '_' + str(set(disj)))
            args_def.append(new_arg)
            atts_def.append(Defeat(new_arg, new_arg))
            atts_def.append(Defeat(new_arg, arg))
            for c in disj:
                atts_def.append(Defeat(c, new_arg))

    return AbstractArgumentationFramework(
        '', arguments=args_def, defeats=atts_def)
