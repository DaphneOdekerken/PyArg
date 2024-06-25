from typing import List

from py_arg.abstract_argumentation.semantics.acceptance_strategy import \
    AcceptanceStrategy
from py_arg.abstract_argumentation.semantics.\
    get_argumentation_framework_extensions import \
    get_argumentation_framework_extensions
from py_arg.aspic.classes.orderings.argument_orderings.last_link_ordering \
    import LastLinkDemocraticOrdering, LastLinkElitistOrdering
from py_arg.aspic.import_export.argumentation_theory_from_lp_file_reader \
    import ArgumentationTheoryFromLPFileReader
from py_arg.aspic.semantics.get_accepted_formulas import get_accepted_formulas
from py_arg_visualisation.functions.ordering_functions.\
    get_ordering_by_specification import get_ordering_by_specification


def get_accepted_formulas_for_file(
        argumentation_theory_file_path: str,
        ordering_specification: str,
        semantics_specification: str,
        acceptance_strategy: str
) -> List[str]:
    # Step 1: read the argumentation theory from the LP file.
    reader = ArgumentationTheoryFromLPFileReader()
    arg_theory = reader.read_from_lp_file(argumentation_theory_file_path)

    # Step 2: convert into abstract AF (based on ordering).
    ordering = get_ordering_by_specification(
        arg_theory, ordering_specification)
    def_rule_preferences = \
        arg_theory.argumentation_system.rule_preferences
    premise_preferences = arg_theory.ordinary_premise_preferences
    if ordering_specification == 'democratic_last_link':
        ordering = \
            LastLinkDemocraticOrdering(def_rule_preferences,
                                       premise_preferences)
    elif ordering_specification == 'elitist_last_link':
        ordering = \
            LastLinkElitistOrdering(def_rule_preferences,
                                    premise_preferences)
    arg_framework = \
        arg_theory.create_abstract_argumentation_framework('af', ordering)

    # Step 3: get the extensions for the chosen semantics.
    frozen_extensions = get_argumentation_framework_extensions(
        arg_framework, semantics_specification)

    # Step 4: get the conclusions of accepted arguments.
    if acceptance_strategy == 'credulous':
        acc_strategy = AcceptanceStrategy.CREDULOUS
    elif acceptance_strategy == 'skeptical':
        acc_strategy = AcceptanceStrategy.WEAKLY_SKEPTICAL
    else:
        raise NotImplementedError('Choose "credulous" or "skeptical" for the '
                                  'acceptance strategy.')
    accepted_formulas = \
        get_accepted_formulas(arg_theory, frozen_extensions,
                              acc_strategy)
    result = sorted([literal.s1 for literal in accepted_formulas])
    return result
