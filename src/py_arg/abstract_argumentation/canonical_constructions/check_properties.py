from typing import Set

import py_arg.utils.powerset
from py_arg.abstract_argumentation.canonical_constructions import \
    aux_operators as aux


def is_tight(extension_set: Set) -> bool:
    """
    Check if this extension set is tight, by Definition 7 of
    Dunne et al., 2015.
    """
    all_elements = aux.big_a(extension_set)
    element_pairs_in_extensions = aux.pairs(extension_set)

    for extension in extension_set:
        for extra_element in all_elements:
            if extra_element not in extension:
                # We can keep iterating as long as for each extension,
                # adding any new element that is not yet in the extension
                # implies that there is some extension argument that is not
                # a pair together with the new element.
                with_extra_element = \
                    frozenset(set(extension.copy()).union({extra_element}))
                if with_extra_element not in extension_set:
                    if all(frozenset({extra_element, other_extension_element})
                           in element_pairs_in_extensions
                           for other_extension_element in extension):
                        return False
    return True


def is_conflict_sensitive(extension_set: Set) -> bool:
    """
    Check if this extension set is conflict_sensitive, by Definition 8 of
    Dunne et al., 2015. Informally, the property checks whether the absence
    of the union of any pair of extensions in an extension set is justified
    by some conflict in that extension set.
    """
    extension_pairs = aux.pairs(extension_set)

    for extension_1, extension_2 in aux.tuples(extension_set):
        if extension_1.union(extension_2) not in extension_set:
            if all(frozenset({element_1, element_2}) in extension_pairs
                   for element_1 in extension_1
                   for element_2 in extension_2):
                return False
    return True


def is_downward_closed(extension_set: Set) -> bool:
    """
    Check if this extension set is downward-closed, by Definition 6 of
    Dunne et al., 2015.
    """
    return aux.downward_closure(extension_set) == extension_set


def is_incomparable(extension_set: Set) -> bool:
    """
    Check if this extension set is incomparable, by Definition 6 of
    Dunne et al., 2015.
    """
    for ext1, ext2 in aux.tuples(extension_set):
        if ext1.intersection(ext2) == ext1:
            return False
        if ext1.intersection(ext2) == ext2:
            return False
    return True


def is_dcl_tight(extension_set: Set) -> bool:
    return is_tight(aux.downward_closure(extension_set))


def contains_empty_set(extension_set: Set) -> bool:
    return frozenset({}) in extension_set


def is_non_empty(extension_set: Set) -> bool:
    return len(extension_set) > 0


def is_unary(extension_set: Set) -> bool:
    return len(extension_set) == 1


def is_com_closed(extension_set: Set) -> bool:
    """
    Check if this extension set is com-closed, by Definition 10 of
    Dunne et al., 2015. "Com" here stands for completion.
    """
    subsets_of_extension_set = py_arg.utils.powerset.powerset(extension_set)
    extension_set_pairs = aux.pairs(extension_set)

    for subset in subsets_of_extension_set:
        elements_in_subset = aux.big_a(set(subset))
        if not elements_in_subset:
            continue

        all_pairs_are_present_in_extension = \
            all(frozenset({element_1, element_2}) in extension_set_pairs
                for element_1, element_2 in aux.tuples(elements_in_subset))
        completion_set = aux.completion_sets(elements_in_subset, extension_set)
        no_unique_completion_set = len(completion_set) != 1

        if all_pairs_are_present_in_extension and no_unique_completion_set:
            return False

    return True
