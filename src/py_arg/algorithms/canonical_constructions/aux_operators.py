
from typing import FrozenSet
import itertools
from typing import Set

from py_arg.abstract_argumentation_classes.argument import Argument


@staticmethod
def tuples(iterable):
    return itertools.combinations(iterable, 2)


@staticmethod
def big_a(extension_set: Set) -> frozenset:
    out = set()
    for extension in extension_set:
        out = out.union(extension)
    return frozenset(out)


@staticmethod
def pairs(extension_set: Set) -> Set[FrozenSet]:
    a = big_a(extension_set)
    out = set()
    for e1, e2 in tuples(a):
        for ext in extension_set:
            if e1 in ext and e2 in ext:
                out.add(frozenset({e1, e2}))
    return out


@staticmethod
def powerset(iterable) -> Set[FrozenSet]:
    s = list(iterable)
    list_of_tuples = set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1)))

    out = set()
    for el in list_of_tuples:
        out.add(frozenset(list(el)))
    return out


@staticmethod
def big_p(extension_set: Set) -> Set[FrozenSet]:
    p = pairs(extension_set)
    power = powerset(big_a(extension_set))

    out = set()
    for s in power:
        if len(s) < 2:
            continue
        for e1, e2 in tuples(s):
            if frozenset({e1, e2}) not in p:
                out.add(s)
    return out


@staticmethod
def big_c(extension: frozenset, extension_set: Set) -> Set[FrozenSet]:
    if extension in extension_set:
        return set(frozenset({extension}))

    out = set()
    a = big_a(extension_set)
    bound = len(a)
    temp = set(frozenset({extension}))
    for i in range(bound):
        for ext in temp:
            if ext in extension_set:
                out.add(ext)
        temp = temp.difference(out)
        new_ext = set()
        for ext in temp:
            new_ext = set()
            for lit in a:
                new = set(ext.copy())
                new.add(lit)
                new_ext.add(frozenset(new))
        temp = temp.union(new_ext)
    return out


@staticmethod
def dcl(extension_set: Set) -> Set[FrozenSet]:
    out = set()
    for ext in extension_set:
        for s in powerset(ext):
            out.add(s)
    return out
