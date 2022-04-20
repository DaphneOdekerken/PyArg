import itertools
from typing import List, Dict, Optional, Set, Tuple

from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.aspic_classes.axiom import Axiom
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.aspic_classes.ordinary_premise import OrdinaryPremise
from py_arg.aspic_classes.preference import Preference
from py_arg.aspic_classes.instantiated_argument import InstantiatedArgument
from py_arg.aspic_classes.argumentation_system import ArgumentationSystem


class ArgumentationTheory:
    """
    An ArgumentationTheory consists of an ArgumentationSystem and a knowledge base.
    Arguments can be inferred on the basis of an ArgumentationTheory.
    """

    def __init__(self, argumentation_system: ArgumentationSystem,
                 knowledge_base_axioms: List[Axiom],
                 knowledge_base_ordinary_premises: List[OrdinaryPremise],
                 ordinary_premise_preferences: Optional[List[Preference]] = None):
        self._argumentation_system = argumentation_system
        self._knowledge_base_axioms = knowledge_base_axioms
        self._knowledge_base_ordinary_premises = knowledge_base_ordinary_premises

        # Rule preferences
        self.ordinary_premise_preference_dict = \
            {str(premise): {str(other_premise): Preference(str(premise), '?', str(other_premise))
                            for other_premise in self._knowledge_base_ordinary_premises}
             for premise in self._knowledge_base_ordinary_premises}
        if ordinary_premise_preferences is not None:
            for ordinary_premise_preference in ordinary_premise_preferences:
                self.add_ordinary_premise_preference(ordinary_premise_preference)

        self._recompute_arguments()

    @property
    def argumentation_system(self):
        return self._argumentation_system

    @argumentation_system.setter
    def argumentation_system(self, argumentation_system_input):
        self._argumentation_system = argumentation_system_input
        self._recompute_arguments()

    @property
    def knowledge_base_axioms(self):
        return self._knowledge_base_axioms

    @knowledge_base_axioms.setter
    def knowledge_base_axioms(self, knowledge_base_axioms_input):
        self._knowledge_base_axioms = knowledge_base_axioms_input
        self._recompute_arguments()

    def add_to_knowledge_base_axioms(self, new_knowledge_base_axiom: Axiom):
        self._knowledge_base_axioms.append(new_knowledge_base_axiom)
        self._recompute_arguments()

    @property
    def knowledge_base_ordinary_premises(self):
        return self._knowledge_base_ordinary_premises

    @knowledge_base_ordinary_premises.setter
    def knowledge_base_ordinary_premises(self, knowledge_base_ordinary_premises_input):
        self._knowledge_base_ordinary_premises = knowledge_base_ordinary_premises_input
        self._recompute_arguments()

    def add_to_knowledge_base_ordinary_premises(self, new_knowledge_base_ordinary_premise: OrdinaryPremise):
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
            arguments_per_conclusion[knowledge_item].add(InstantiatedArgument.observation_based(knowledge_item))
        for knowledge_item in self._knowledge_base_ordinary_premises:
            arguments_per_conclusion[knowledge_item].add(InstantiatedArgument.observation_based(knowledge_item))

        change = True
        while change:
            change = False
            for defeasible_rule in self._argumentation_system.defeasible_rules:
                possible_antecedents = [arguments_per_conclusion[antecedent]
                                        for antecedent in defeasible_rule.antecedents]
                if all(possible_antecedents):
                    for direct_sub_argument_tuple in itertools.product(*possible_antecedents):
                        new_instantiated_argument = \
                            InstantiatedArgument.defeasible_rule_based(defeasible_rule, set(direct_sub_argument_tuple))
                        if new_instantiated_argument not in arguments_per_conclusion[defeasible_rule.consequent]:
                            arguments_per_conclusion[defeasible_rule.consequent].add(new_instantiated_argument)
                            change = True
            for strict_rule in self._argumentation_system.strict_rules:
                possible_antecedents = [arguments_per_conclusion[antecedent] for antecedent in strict_rule.antecedents]
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

    def add_ordinary_premise_preference(self, premise_preference: Preference):
        """
        Add a preference relation to the argumentation theory.

        :param premise_preference: The new preference relation between ordinary premises that should be added.
        """
        a, b = str(premise_preference.object_a), str(premise_preference.object_b)
        self.ordinary_premise_preference_dict[a][b] = premise_preference
        self.ordinary_premise_preference_dict[b][a] = Preference.inversion(premise_preference)

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
        if argument_a.conclusion not in argument_b.conclusion.contraries:
            return False
        return True

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
        if argument_a.conclusion not in argument_b.conclusion.contraries:
            return False
        if argument_b.conclusion in argument_a.conclusion.contraries:
            return False
        return True

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
        if argument_a.conclusion not in argument_b_top_rule_literal.contraries:
            return False
        return True

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
        return any([argument_a.conclusion in ordinary_premise_b.contraries
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
        return any([argument_a.conclusion in sub_argument_b.conclusion.contraries and
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
        return any([argument_a.conclusion in ordinary_premise_b.contraries and
                    ordinary_premise_b not in argument_a.conclusion.contraries
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

        if ordering == None:
            return [Defeat(argument_a,argument_b)
                    for argument_a in self.all_arguments
                    for argument_b in self.all_arguments
                    if self.attacks(argument_a,argument_b)]

        return [Defeat(argument_a, argument_b)
                for argument_a in self.all_arguments
                for argument_b in self.all_arguments
                if self.defeats(argument_a, argument_b, ordering)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
