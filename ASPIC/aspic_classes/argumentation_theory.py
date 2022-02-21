import itertools
from typing import List, Dict, Optional, Set, Tuple

from ASPIC.abstract_argumentation_classes.defeat import Defeat
from ASPIC.aspic_classes.axiom import Axiom
from ASPIC.aspic_classes.defeasible_rule import DefeasibleRule
from ASPIC.aspic_classes.literal import Literal
from ASPIC.aspic_classes.orderings.ordering import Ordering
from ASPIC.aspic_classes.ordinary_premise import OrdinaryPremise
from ASPIC.aspic_classes.preference import Preference
from ASPIC.aspic_classes.instantiated_argument import InstantiatedArgument
from ASPIC.aspic_classes.argumentation_system import ArgumentationSystem


class ArgumentationTheory:
    """
    An ArgumentationTheory consists of an ArgumentationSystem and a knowledge base.
    Arguments can be inferred on the basis of an ArgumentationTheory.
    """

    def __init__(self, argumentation_system: ArgumentationSystem,
                 knowledge_base_axioms: List[Axiom],
                 knowledge_base_ordinary_premises: List[OrdinaryPremise],
                 ordinary_premise_preferences: Optional[List[Preference]] = None):
        self.argumentation_system = argumentation_system
        self.knowledge_base_axioms = knowledge_base_axioms
        self.knowledge_base_ordinary_premises = knowledge_base_ordinary_premises

        # Rule preferences
        self.ordinary_premise_preference_dict = \
            {str(premise): {str(other_premise): Preference(str(premise), '?', str(other_premise))
                            for other_premise in self.knowledge_base_ordinary_premises}
             for premise in self.knowledge_base_ordinary_premises}
        if ordinary_premise_preferences is not None:
            for ordinary_premise_preference in ordinary_premise_preferences:
                self.add_ordinary_queryable_preference(ordinary_premise_preference)

        self._arguments = self.recompute_arguments()

    @property
    def arguments(self) -> Dict[Literal, Set[InstantiatedArgument]]:
        return self._arguments

    def recompute_arguments(self):
        arguments_per_conclusion = {literal: set() for literal in self.argumentation_system.language.values()}

        for knowledge_item in self.knowledge_base_axioms:
            arguments_per_conclusion[knowledge_item].add(InstantiatedArgument.observation_based(knowledge_item))
        for knowledge_item in self.knowledge_base_ordinary_premises:
            arguments_per_conclusion[knowledge_item].add(InstantiatedArgument.observation_based(knowledge_item))

        change = True
        while change:
            change = False
            for defeasible_rule in self.argumentation_system.defeasible_rules:
                possible_antecedents = [arguments_per_conclusion[antecedent]
                                        for antecedent in defeasible_rule.antecedents]
                if all(possible_antecedents):
                    for direct_sub_argument_tuple in itertools.product(*possible_antecedents):
                        new_instantiated_argument = \
                            InstantiatedArgument.defeasible_rule_based(defeasible_rule, set(direct_sub_argument_tuple))
                        if new_instantiated_argument not in arguments_per_conclusion[defeasible_rule.consequent]:
                            arguments_per_conclusion[defeasible_rule.consequent].add(new_instantiated_argument)
                            change = True
            for strict_rule in self.argumentation_system.strict_rules:
                possible_antecedents = [arguments_per_conclusion[antecedent] for antecedent in strict_rule.antecedents]
                if all(possible_antecedents):
                    for direct_sub_argument_tuple in itertools.product(*possible_antecedents):
                        new_instantiated_argument = \
                            InstantiatedArgument.strict_rule_based(strict_rule, set(direct_sub_argument_tuple))
                        if new_instantiated_argument not in arguments_per_conclusion[strict_rule.consequent]:
                            arguments_per_conclusion[strict_rule.consequent].add(new_instantiated_argument)
                            change = True

        return arguments_per_conclusion

    @property
    def all_arguments(self) -> List[InstantiatedArgument]:
        return [argument for arguments_for_literal in self.arguments.values() for argument in arguments_for_literal]

    @property
    def all_attacks(self) -> List[Tuple[InstantiatedArgument, InstantiatedArgument]]:
        return [(argument_a, argument_b)
                for argument_a in self.all_arguments
                for argument_b in self.all_arguments
                if self.attacks(argument_a, argument_b)]

    def add_ordinary_queryable_preference(self, queryable_preference: Preference):
        a, b = str(queryable_preference.object_a), str(queryable_preference.object_b)
        self.ordinary_premise_preference_dict[a][b] = queryable_preference
        self.ordinary_premise_preference_dict[b][a] = Preference.inversion(queryable_preference)

    @staticmethod
    def rebuts_on_conclusion(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        if argument_b.is_observation_based:
            return False
        if not isinstance(argument_b.top_rule, DefeasibleRule):
            return False
        if argument_a.conclusion not in argument_b.conclusion.contraries:
            return False
        return True

    def rebuts(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        return any([self.rebuts_on_conclusion(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    def rebuts_and_is_not_weaker(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument,
                                 ordering: Ordering) -> bool:
        return any([self.rebuts_on_conclusion(argument_a, sub_argument_b) and
                    not ordering.argument_is_strictly_weaker_than(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    @staticmethod
    def contrary_rebuts_on_conclusion(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        if argument_b.is_observation_based:
            return False
        if not isinstance(argument_b.top_rule, DefeasibleRule):
            return False
        if argument_a.conclusion not in argument_b.conclusion.contraries:
            return False
        if argument_b.conclusion in argument_a.conclusion.contraries:
            return False
        return True

    def contrary_rebuts(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        return any([self.contrary_rebuts_on_conclusion(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    def undercuts_on_top_rule(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        if argument_b.is_observation_based:
            return False
        if not isinstance(argument_b.top_rule, DefeasibleRule):
            return False
        argument_b_top_rule_literal = self.argumentation_system.get_literal(argument_b.top_rule)
        if argument_a.conclusion not in argument_b_top_rule_literal.contraries:
            return False
        return True

    def undercuts(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        return any([self.undercuts_on_top_rule(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    @staticmethod
    def undermines(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        return any([argument_a.conclusion in ordinary_premise_b.contraries
                    for ordinary_premise_b in argument_b.ordinary_premises])

    @staticmethod
    def undermines_and_is_not_weaker(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument,
                                     ordering: Ordering) -> bool:
        return any([argument_a.conclusion in sub_argument_b.conclusion.contraries and
                    not ordering.argument_is_strictly_weaker_than(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments
                    if sub_argument_b.is_observation_based and sub_argument_b.is_plausible])

    @staticmethod
    def contrary_undermines(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        return any([argument_a.conclusion in ordinary_premise_b.contraries and
                    ordinary_premise_b not in argument_a.conclusion.contraries
                    for ordinary_premise_b in argument_b.ordinary_premises])

    def attacks(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        return self.rebuts(argument_a, argument_b) or self.undercuts(argument_a, argument_b) or \
               self.undermines(argument_a, argument_b)

    def defeats(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument, ordering: Ordering) -> bool:
        # Preference-independent attacks
        if self.undercuts(argument_a, argument_b):
            return True
        if self.contrary_rebuts(argument_a, argument_b):
            return True
        if self.contrary_undermines(argument_a, argument_b):
            return True

        # Preference-dependent attacks
        if self.rebuts_and_is_not_weaker(argument_a, argument_b, ordering):
            return True
        if self.undermines_and_is_not_weaker(argument_a, argument_b, ordering):
            return True
        return False

    def get_all_defeats(self, ordering: Ordering) -> List[Defeat]:
        return [Defeat(argument_a, argument_b)
                for argument_a in self.all_arguments
                for argument_b in self.all_arguments
                if self.defeats(argument_a, argument_b, ordering)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
