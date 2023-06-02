from typing import Set, FrozenSet

import py_arg.algorithms.canonical_constructions.canonical_af.canonical_cf as canonical_cf
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


@staticmethod
def defence_formula(extension_set: Set, arg: Argument) -> Set[FrozenSet]:
    out = set()
    for ext in extension_set:
        if arg in ext:
            out.add(ext.copy().difference({arg}))
    return out  # .difference(ExtensionSet({frozenset()}))


@staticmethod
def disjunctive_defence_formula(extension_set: Set, arg: Argument) -> Set[FrozenSet]:
    cnf = defence_formula(extension_set, arg)
    dnf = set({frozenset()})
    for conjunct in cnf:
        if len(conjunct) == 0:
            return set()
        old_dnf = dnf
        new_dnf = set()
        for disjunct in old_dnf:
            for d in conjunct:
                new_elem = set(disjunct)
                new_elem.add(d)
                new_dnf.add(frozenset(new_elem))
        dnf = new_dnf

    non_minimal = set()
    for d1 in dnf:
        for d2 in dnf:
            if d2.issubset(d1) and not d1.issubset(d2):
                non_minimal.add(d1)

    return dnf.difference(non_minimal)


@staticmethod
def apply(extension_set: Set) -> AbstractArgumentationFramework:
    canon_cf = canonical_cf.apply(extension_set)
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

    return AbstractArgumentationFramework('', arguments=args_def, defeats=atts_def)
