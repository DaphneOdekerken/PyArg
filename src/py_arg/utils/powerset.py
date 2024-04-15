import itertools
from typing import Set, FrozenSet


def powerset(iterable) -> Set[FrozenSet]:
    """
    Get all subsets of the given set.
    """
    s = list(iterable)
    list_of_tuples = set(itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)))

    return {frozenset(list(element)) for element in list_of_tuples}
