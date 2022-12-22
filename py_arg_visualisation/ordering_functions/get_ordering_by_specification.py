from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.orderings.argument_orderings.last_link_ordering import LastLinkDemocraticOrdering, \
    LastLinkElitistOrdering
from py_arg.aspic_classes.orderings.argument_orderings.weakest_link_ordering import WeakestLinkDemocraticOrdering, \
    WeakestLinkElitistOrdering


def get_ordering_by_specification(argumentation_theory: ArgumentationTheory, ordering_specification: str):
    def_rule_preferences = argumentation_theory.argumentation_system.rule_preferences
    premise_preferences = argumentation_theory.ordinary_premise_preferences
    if ordering_specification == 'demlastl':
        ordering = LastLinkDemocraticOrdering(def_rule_preferences, premise_preferences)
    elif ordering_specification == 'elilastl':
        ordering = LastLinkElitistOrdering(def_rule_preferences, premise_preferences)
    elif ordering_specification == 'demweakl':
        ordering = WeakestLinkDemocraticOrdering(def_rule_preferences, premise_preferences)
    elif ordering_specification == 'eliweakl':
        ordering = WeakestLinkElitistOrdering(def_rule_preferences, premise_preferences)
    else:
        ordering = None
    return ordering