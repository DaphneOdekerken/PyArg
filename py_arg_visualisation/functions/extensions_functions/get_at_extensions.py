from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg_visualisation.functions.extensions_functions.get_af_extensions import get_argumentation_framework_extensions
from py_arg_visualisation.functions.ordering_functions.get_ordering_by_specification import get_ordering_by_specification


def get_argumentation_theory_extensions(argumentation_theory: ArgumentationTheory,
                                        semantics_specification: str,
                                        ordering_specification: str):
    """
    Calculate the set of extensions from the given argumentation theory, type of ordering and semantics

    :param argumentation_theory: The argumentation theory.
    :param semantics_specification: The chosen semantics.
    :param ordering_specification: The chosen ordering, combining both last/weakest link and democratic/elitist.
    """

    # Select the required Ordering
    ordering = get_ordering_by_specification(argumentation_theory, ordering_specification)

    # Derive the abstract argumentation framework from the chosen Ordering
    argumentation_framework = argumentation_theory.create_abstract_argumentation_framework('af', ordering)

    # Find the extensions
    return get_argumentation_framework_extensions(argumentation_framework, semantics_specification)
