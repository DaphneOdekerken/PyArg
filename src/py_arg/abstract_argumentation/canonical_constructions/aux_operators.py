from typing import FrozenSet
import itertools
from typing import Set

from py_arg.utils.powerset import powerset


def tuples(iterable):
    """
    Get all two-length combinations of some set/list/...
    """
    return itertools.combinations(iterable, 2)


def big_a(extension_set: Set) -> FrozenSet:
    """
    This is the set of all unique elements occurring in the extension_set.
    """
    return frozenset({element for extension in extension_set
                      for element in extension})


def pairs(extension_set: Set) -> Set[FrozenSet]:
    """
    Get all pairs of elements occurring together in some extension,
    by Definition 5 of Dunne et al., 2015.
    """
    all_possible_elements = big_a(extension_set)
    return {frozenset({e1, e2})
            for e1, e2 in tuples(all_possible_elements)
            for extension in extension_set
            if e1 in extension and e2 in extension}


def big_p(extension_set: Set) -> Set[FrozenSet]:
    out = powerset(big_a(extension_set))
    out.difference(downward_closure(extension_set))
    return out


def completion_sets(
        extension: frozenset, extension_set: Set) -> Set[FrozenSet]:
    """
    Compute the completion sets of a given extension set, by Definition 9 of
    Dunne et al., 2015. This is the set of subset-minimal sets in the
    extension set such that the extension is a subset.
    """
    all_extensions_containing_set = {
        extension_in_set for extension_in_set in extension_set
        if extension.issubset(extension_in_set)
    }
    all_smallest_extensions_containing_set = {
        extension_in_set for extension_in_set in all_extensions_containing_set
        if not any(other_extension < extension_in_set
                   for other_extension in all_extensions_containing_set)
    }
    return all_smallest_extensions_containing_set


def unique_big_c(extension: frozenset, extension_set: Set) -> FrozenSet:
    c = completion_sets(extension, extension_set)
    if len(c) == 1:
        return c.pop()
    else:
        return frozenset()


def downward_closure(extension_set: Set) -> Set[FrozenSet]:
    """
    Compute the downward-closure (dcl) as defined in Dunne et al. 2015,
    Definition 6.
    """
    return {extension_subset
            for extension in extension_set
            for extension_subset in powerset(extension)}


def ucl(extension_set: Set) -> Set[FrozenSet]:
    out = extension_set.copy()
    out.add(frozenset())
    new = set()
    for a, b in tuples(extension_set):
        new.add(frozenset(set(a).union(set(b))))
    return out.union(new)


def reduce(extension_set: Set) -> Set[FrozenSet]:
    all_arguments = big_a(extension_set)
    for extension in extension_set:
        all_arguments = all_arguments.intersection(extension)

    return {extension.difference(all_arguments)
            for extension in extension_set}
