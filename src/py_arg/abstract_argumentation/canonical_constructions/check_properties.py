from typing import Set

from py_arg.abstract_argumentation.canonical_constructions import \
    aux_operators as aux


def is_tight(extension_set: Set) -> bool:
    a = aux.big_a(extension_set)
    pairs_ = aux.pairs(extension_set)

    for ext in extension_set:
        for lit in a:
            if lit not in ext:
                temp = set(ext.copy())
                temp.add(lit)
                temp = frozenset(temp)
                if temp not in extension_set:
                    boolean = False
                    for lin_in in ext:
                        test = frozenset({lit, lin_in})
                        if test not in pairs_:
                            boolean = True
                    if not boolean:
                        return False
    return True


def is_conflict_sensitive(extension_set: Set) -> bool:
    pairs_ = aux.pairs(extension_set)

    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.union(ext2) not in extension_set:
            boolean = False
            for lit1 in ext1:
                for lit2 in ext2:
                    temp = frozenset({lit1, lit2})
                    if temp not in pairs_:
                        boolean = True
            if not boolean:
                return False
    return True


def is_downward_closed(extension_set: Set) -> bool:
    return aux.dcl(extension_set).__eq__(extension_set)


def is_incomparable(extension_set: Set) -> bool:
    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.intersection(ext2) == ext1:
            return False
        if ext1.intersection(ext2) == ext2:
            return False
    return True


def is_dcl_tight(extension_set: Set) -> bool:
    return is_tight(aux.dcl(extension_set))


def contains_empty_set(extension_set: Set) -> bool:
    return frozenset({}) in extension_set


def is_non_empty(extension_set: Set) -> bool:
    return len(extension_set) > 0


def is_unary(extension_set: Set) -> bool:
    return len(extension_set) == 1
