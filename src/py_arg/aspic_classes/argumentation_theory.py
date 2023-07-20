import itertools
from typing import List, Dict, Optional, Set, Tuple

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.argument_orderings.last_link_ordering import LastLinkElitistOrdering
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.aspic_classes.instantiated_argument import InstantiatedArgument
from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.orderings.preference_preorder import PreferencePreorder
from py_arg.aspic_classes.structured_argumentation_framework import StructuredArgumentationFramework


class ArgumentationTheory:
    """
    An ArgumentationTheory consists of an ArgumentationSystem and a knowledge base.
    Arguments can be inferred on the basis of an ArgumentationTheory.
    """

    def __init__(self, argumentation_system: ArgumentationSystem,
                 knowledge_base_axioms: List[Literal],
                 knowledge_base_ordinary_premises: List[Literal],
                 ordinary_premise_preferences: Optional[PreferencePreorder] = None):
        self._argumentation_system = argumentation_system
        self._knowledge_base_axioms = knowledge_base_axioms
        self._knowledge_base_ordinary_premises = knowledge_base_ordinary_premises

        # Rule preferences
        if ordinary_premise_preferences:
            self.ordinary_premise_preferences = ordinary_premise_preferences
        else:
            self.ordinary_premise_preferences = \
                PreferencePreorder.create_reflexive_preorder(self._knowledge_base_ordinary_premises)

        self._recompute_arguments()

    @property
    def argumentation_system(self):
        return self._argumentation_system

    @argumentation_system.setter
    def argumentation_system(self, argumentation_system_input):
        self._argumentation_system = argumentation_system_input
        self._recompute_arguments()

    @property
    def knowledge_base(self):
        return self._knowledge_base_axioms + self._knowledge_base_ordinary_premises

    @property
    def knowledge_base_axioms(self):
        return self._knowledge_base_axioms

    @knowledge_base_axioms.setter
    def knowledge_base_axioms(self, knowledge_base_axioms_input):
        self._knowledge_base_axioms = knowledge_base_axioms_input
        self._recompute_arguments()

    def add_to_knowledge_base_axioms(self, new_knowledge_base_axiom: Literal):
        self._knowledge_base_axioms.append(new_knowledge_base_axiom)
        self._recompute_arguments()

    @property
    def knowledge_base_ordinary_premises(self):
        return self._knowledge_base_ordinary_premises

    @knowledge_base_ordinary_premises.setter
    def knowledge_base_ordinary_premises(self, knowledge_base_ordinary_premises_input):
        self._knowledge_base_ordinary_premises = knowledge_base_ordinary_premises_input
        self._recompute_arguments()

    def add_to_knowledge_base_ordinary_premises(self, new_knowledge_base_ordinary_premise: Literal):
        self._knowledge_base_ordinary_premises.append(new_knowledge_base_ordinary_premise)
        self._recompute_arguments()

    @property
    def arguments(self) -> Dict[Literal, Set[InstantiatedArgument]]:
        """
        Get a dictionary of all arguments in this argumentation theory, indexed by their conclusion literal.

        :return: A dictionary of all arguments, indexed by their conclusion literal.
        """
        return self._arguments

    def _recompute_arguments(self):
        """
        Recompute the set of arguments inferred from this argumentation theory.

        This step is necessary after every change in the argumentation system or knowledge base (note that this is done
        automatically by the corresponding setters).
        """
        arguments_per_conclusion = {literal: set() for literal in self._argumentation_system.language.values()}

        for knowledge_item in self._knowledge_base_axioms:
            arguments_per_conclusion[knowledge_item].add(InstantiatedArgument.axiom_based(knowledge_item))
        for knowledge_item in self._knowledge_base_ordinary_premises:
            arguments_per_conclusion[knowledge_item].add(InstantiatedArgument.ordinary_premise_based(knowledge_item))

        change = True
        while change:
            change = False
            for defeasible_rule in self._argumentation_system.defeasible_rules:
                possible_antecedents = [[argument_for_antecedent
                                         for argument_for_antecedent in arguments_per_conclusion[antecedent]
                                         if defeasible_rule.consequent not in argument_for_antecedent.sub_conclusions]
                                        for antecedent in defeasible_rule.antecedents]
                if all(possible_antecedents):
                    for direct_sub_argument_tuple in itertools.product(*possible_antecedents):
                        new_instantiated_argument = \
                            InstantiatedArgument.defeasible_rule_based(defeasible_rule, set(direct_sub_argument_tuple))
                        if new_instantiated_argument not in arguments_per_conclusion[defeasible_rule.consequent]:
                            arguments_per_conclusion[defeasible_rule.consequent].add(new_instantiated_argument)
                            change = True
            for strict_rule in self._argumentation_system.strict_rules:
                possible_antecedents = [[argument_for_antecedent
                                         for argument_for_antecedent in arguments_per_conclusion[antecedent]
                                         if strict_rule.consequent not in argument_for_antecedent.sub_conclusions]
                                        for antecedent in strict_rule.antecedents]
                if all(possible_antecedents):
                    for direct_sub_argument_tuple in itertools.product(*possible_antecedents):
                        new_instantiated_argument = \
                            InstantiatedArgument.strict_rule_based(strict_rule, set(direct_sub_argument_tuple))
                        if new_instantiated_argument not in arguments_per_conclusion[strict_rule.consequent]:
                            arguments_per_conclusion[strict_rule.consequent].add(new_instantiated_argument)
                            change = True

        self._arguments = arguments_per_conclusion

    @property
    def all_arguments(self) -> List[InstantiatedArgument]:
        """
        Get a list of all arguments inferred from this argumentation theory.
        """
        return [argument for arguments_for_literal in self.arguments.values() for argument in arguments_for_literal]

    @property
    def all_attacks(self) -> List[Tuple[InstantiatedArgument, InstantiatedArgument]]:
        """
        Get a list of all attacks (note: not defeats!)
        """
        return [(argument_a, argument_b)
                for argument_a in self.all_arguments
                for argument_b in self.all_arguments
                if self.attacks(argument_a, argument_b)]

    @staticmethod
    def rebuts_on_conclusion(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a rebuts argument_b on its conclusion.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a rebuts argument_b on its conclusion.
        """
        if argument_b.is_observation_based:
            return False
        if not isinstance(argument_b.top_rule, DefeasibleRule):
            return False
        return argument_a.conclusion.is_contrary_or_contradictory_of(argument_b.conclusion)

    def rebuts(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a rebuts argument_b.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a rebuts argument_b.
        """
        return any([self.rebuts_on_conclusion(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    def rebuts_and_is_not_weaker(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument,
                                 ordering: Ordering) -> bool:
        """
        Check if argument_a rebuts argument_b and is not weaker according to the given ordering.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :param ordering: The ordering used to identify argument strength.
        :return: Boolean indicating whether argument_a rebuts argument_b and is stronger.
        """
        return any([self.rebuts_on_conclusion(argument_a, sub_argument_b) and
                    not ordering.argument_is_strictly_weaker_than(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    @staticmethod
    def contrary_rebuts_on_conclusion(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a contrary-rebuts argument_b on its conclusion.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a contrary-rebuts argument_b on its conclusion.
        """
        if argument_b.is_observation_based:
            return False
        if not isinstance(argument_b.top_rule, DefeasibleRule):
            return False
        return argument_a.conclusion.is_contrary_of(argument_b.conclusion)

    def contrary_rebuts(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a contrary-rebuts argument_b.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a contrary-rebuts argument_b.
        """
        return any([self.contrary_rebuts_on_conclusion(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    def undercuts_on_top_rule(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a undercuts argument_b on its top rule.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a undercuts argument_b on its top rule.
        """
        if argument_b.is_observation_based:
            return False
        if not isinstance(argument_b.top_rule, DefeasibleRule):
            return False
        argument_b_top_rule_literal = self._argumentation_system.get_literal(argument_b.top_rule)
        return argument_a.conclusion.is_contrary_or_contradictory_of(argument_b_top_rule_literal)

    def undercuts(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a undercuts argument_b.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a undercuts argument_b.
        """
        return any([self.undercuts_on_top_rule(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments])

    @staticmethod
    def undermines(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a undermines argument_b.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a undermines argument_b.
        """
        return any([argument_a.conclusion.is_contrary_or_contradictory_of(ordinary_premise_b)
                    for ordinary_premise_b in argument_b.ordinary_premises])

    @staticmethod
    def undermines_and_is_not_weaker(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument,
                                     ordering: Ordering) -> bool:
        """
        Check if argument_a undermines argument_b and is not weaker according to the specifies ordering.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :param ordering: The ordering used to decide if argument_a is weaker than argument_b.
        :return: Boolean indicating whether argument_a undermines argument_b and is not weaker.
        """
        return any([argument_a.conclusion.is_contrary_or_contradictory_of(sub_argument_b.conclusion) and
                    not ordering.argument_is_strictly_weaker_than(argument_a, sub_argument_b)
                    for sub_argument_b in argument_b.sub_arguments
                    if sub_argument_b.is_observation_based and sub_argument_b.is_plausible])

    @staticmethod
    def contrary_undermines(argument_a: InstantiatedArgument, argument_b: InstantiatedArgument) -> bool:
        """
        Check if argument_a contrary-undermines argument_b.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a contrary-undermines argument_b.
        """
        return any([argument_a.conclusion.is_contrary_of(ordinary_premise_b)
                    for ordinary_premise_b in argument_b.ordinary_premises])

    def attacks(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument):
        """
        Check if argument_a attacks argument_b.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :return: Boolean indicating whether argument_a attacks argument_b.
        """
        return self.rebuts(argument_a, argument_b) or self.undercuts(argument_a, argument_b) or \
            self.undermines(argument_a, argument_b)

    def defeats(self, argument_a: InstantiatedArgument, argument_b: InstantiatedArgument, ordering: Ordering) -> bool:
        """
        Check if argument_a defeats argument_b, given the specified ordering.

        :param argument_a: The supposedly attacking argument.
        :param argument_b: The supposedly attacked argument.
        :param ordering: The ordering used to decide if argument_a is weaker than argument_b.
        :return: Boolean indicating whether argument_a defeats argument_b.
        """
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

    def recompute_all_defeats(self, ordering: Ordering) -> List[Defeat]:
        """
        Recompute all defeats between all arguments, given the specified ordering.

        :param ordering: The ordering used to decide if the attacking argument is weaker than the attacking argument.
        :return: List of all defeats.
        """
        if ordering is None:
            return [Defeat(argument_a, argument_b)
                    for argument_a in self.all_arguments
                    for argument_b in self.all_arguments
                    if self.attacks(argument_a, argument_b)]

        return [Defeat(argument_a, argument_b)
                for argument_a in self.all_arguments
                for argument_b in self.all_arguments
                if self.defeats(argument_a, argument_b, ordering)]

    def create_abstract_argumentation_framework(self, name: str, ordering: Optional[Ordering] = None):
        """
        Create an abstract argumentation framework based on this argumentation theory. Note: if no ordering is given,
        last link elitist ordering is chosen as default ordering.

        :param name: The name of the argumentation framework.
        :param ordering: Ordering that influences which attacks are defeats. Note: default is last link elitist.
        :return: Abstract argumentation framework based on this argumentation theory.

        """
        if ordering is None:
            ordering = LastLinkElitistOrdering(self.argumentation_system.rule_preferences,
                                               self.ordinary_premise_preferences)
        return AbstractArgumentationFramework(name, self.all_arguments, self.recompute_all_defeats(ordering))

    def create_structured_argumentation_framework(self, name: str, ordering: Optional[Ordering] = None):
        """
        Create a structured argumentation framework based on this argumentation theory. Note: if no ordering is given,
        last link elitist ordering is chosen as default ordering.

        :param name: The name of the argumentation framework.
        :param ordering: Ordering that influences the argument preferences. Note: default is last link elitist.
        :return: Structured argumentation framework based on this argumentation theory.

        """
        if ordering is None:
            ordering = LastLinkElitistOrdering(self.argumentation_system.rule_preferences,
                                               self.ordinary_premise_preferences)
        return StructuredArgumentationFramework(name, self.all_arguments, self.all_attacks,
                                                [(arg_a, arg_b)
                                                 for arg_a in self.all_arguments for arg_b in self.all_arguments
                                                 if ordering.argument_is_weaker_or_equal_than(arg_a, arg_b)])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
