from typing import Set, FrozenSet

from py_arg.abstract_argumentation.semantics.acceptance_strategy import \
    AcceptanceStrategy
from py_arg.abstract_argumentation.semantics.get_accepted_arguments import \
    get_accepted_arguments
from py_arg.aspic.classes.instantiated_argument import InstantiatedArgument
from py_arg.aspic.classes.literal import Literal


def get_non_accepted_formulas(
        extensions: Set[FrozenSet[InstantiatedArgument]],
        acceptance_strategy: AcceptanceStrategy) -> \
        Set[Literal]:
    """
    Calculate the set of accepted formulas from a set of extensions
    (sets of arguments) and evaluation strategy

    :param extensions: The extensions (sets of collectively accepted arguments)
    :param acceptance_strategy: The acceptance strategy (e.g., skeptical or
    credulous).
    """
    if acceptance_strategy == AcceptanceStrategy.SKEPTICAL:
        accepted_arguments = \
            get_accepted_arguments(extensions, acceptance_strategy)
        return set(arg.conclusion for arg in accepted_arguments
                   if not arg.conclusion.defeasible_rule_based)
    if acceptance_strategy == AcceptanceStrategy.CREDULOUS:
        accepted_arguments = \
            get_accepted_arguments(extensions, acceptance_strategy)
        return set(arg.conclusion for arg in accepted_arguments
                   if not arg.conclusion.defeasible_rule_based)
    elif acceptance_strategy == AcceptanceStrategy.WEAKLY_SKEPTICAL:
        extension_formulas = [{arg.conclusion for arg in extension}
                              for extension in extensions]
        return set.intersection(*extension_formulas)
