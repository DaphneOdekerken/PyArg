from typing import Set, FrozenSet

from py_arg.abstract_argumentation.canonical_constructions.canonical_af.\
    canonical_cf import get_canonical_cf_framework
from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat


def get_defense_formula(extension_set: Set, argument: Argument) -> \
        Set[FrozenSet]:
    """
    This function implements Definition 13 (first part) of Dunne et al., 2015.
    """
    return {
        extension.copy().difference({argument})
        for extension in extension_set
        if argument in extension
    }


def get_cnf_defense_formula(extension_set: Set, arg: Argument) -> \
        Set[FrozenSet]:
    """
    This function implements Definition 13 (second part) of Dunne et al., 2015.
    """
    defense_formula = get_defense_formula(extension_set, arg)
    result = {frozenset()}
    for conjunction_in_disjuction in defense_formula:
        # Check for tautology: if one conjunctive part is always true,
        # then this holds for the whole formula.
        if not conjunction_in_disjuction:
            return set()

        full_cnf_until_now = result
        updated_cnf_formula = set()
        for conjunction_in_earlier_formula in full_cnf_until_now:
            for extra_disjunctive_part in conjunction_in_disjuction:
                # Add this disjunctive part to each earlier element in the
                # formula until now.
                new_elem = set(conjunction_in_earlier_formula)
                new_elem.add(extra_disjunctive_part)
                updated_cnf_formula.add(frozenset(new_elem))
        result = updated_cnf_formula

    # Only keep the minimal conjunctions.
    minimal = {
        conjunction for conjunction in result
        if not any(other_conjunction < conjunction
                   for other_conjunction in result)
    }

    return minimal


def get_canonical_def_framework(extension_set: Set) -> \
        AbstractArgumentationFramework:
    """
    This function implements the canonical defense-argumentation-framework,
    as defined in Dunne et al., 2015 Definition 14.
    """
    canonical_cf = get_canonical_cf_framework(extension_set)

    attacks = canonical_cf.defeats.copy()
    arguments = canonical_cf.arguments.copy()

    for argument in canonical_cf.arguments:
        cnf_defense_formula = get_cnf_defense_formula(extension_set, argument)
        for clause in cnf_defense_formula:
            # Add extra argument.
            extra_argument = Argument(str(argument) + '_' + str(set(clause)))
            arguments.append(extra_argument)
            # This argument is self-attacking, attacked by all (original)
            # arguments in the clause and attacks the argument in canonical_cf.
            attacks.append(Defeat(extra_argument, extra_argument))
            attacks.append(Defeat(extra_argument, argument))
            for clause_element in clause:
                attacks.append(Defeat(clause_element, extra_argument))

    return AbstractArgumentationFramework(
        '', arguments=arguments, defeats=attacks)
