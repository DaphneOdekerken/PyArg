import itertools
from typing import List, Dict, Set

from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.axiom import Axiom
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.aspic_classes.ordinary_premise import OrdinaryPremise
from py_arg.incomplete_aspic_classes.queryable import Queryable
from py_arg.incomplete_aspic_classes.potential_argument import PotentialArgument


class PotentialArgumentationTheory(ArgumentationTheory):
    def __init__(self, argumentation_system: ArgumentationSystem, knowledge_base_axioms: List[Axiom],
                 knowledge_base_ordinary_premises: List[OrdinaryPremise], queryables: List[Queryable]):
        super().__init__(argumentation_system, knowledge_base_axioms, knowledge_base_ordinary_premises)
        self.queryables = queryables
        self._potential_arguments = self.recompute_potential_arguments()

    def recompute_potential_arguments(self) -> Dict[Literal, Set[PotentialArgument]]:
        arguments_per_conclusion = {literal: set() for literal in self.argumentation_system.language.values()}

        for queryable in self.queryables:
            if all(queryable_contrary not in self.knowledge_base_axioms and
                   queryable_contrary not in self.knowledge_base_ordinary_premises
                   for queryable_contrary in queryable.contraries):
                arguments_per_conclusion[queryable].add(PotentialArgument.observation_based(queryable))

        change = True
        while change:
            change = False
            for defeasible_rule in self.argumentation_system.defeasible_rules:
                possible_antecedents = [arguments_per_conclusion[antecedent]
                                        for antecedent in defeasible_rule.antecedents]
                if all(possible_antecedents):
                    for direct_sub_argument_tuple in itertools.product(*possible_antecedents):
                        new_instantiated_argument = \
                            PotentialArgument.defeasible_rule_based(defeasible_rule, set(direct_sub_argument_tuple))
                        if new_instantiated_argument not in arguments_per_conclusion[defeasible_rule.consequent]:
                            arguments_per_conclusion[defeasible_rule.consequent].add(new_instantiated_argument)
                            change = True
            for strict_rule in self.argumentation_system.strict_rules:
                possible_antecedents = [arguments_per_conclusion[antecedent] for antecedent in strict_rule.antecedents]
                if all(possible_antecedents):
                    for direct_sub_argument_tuple in itertools.product(*possible_antecedents):
                        new_instantiated_argument = \
                            PotentialArgument.strict_rule_based(strict_rule, set(direct_sub_argument_tuple))
                        if new_instantiated_argument not in arguments_per_conclusion[strict_rule.consequent]:
                            arguments_per_conclusion[strict_rule.consequent].add(new_instantiated_argument)
                            change = True

        return arguments_per_conclusion

    @property
    def potential_arguments(self) -> Dict[Literal, Set[PotentialArgument]]:
        return self._potential_arguments

    @property
    def all_potential_arguments(self) -> List[PotentialArgument]:
        return [argument for arguments_for_literal in self.potential_arguments.values()
                for argument in arguments_for_literal]

    def get_all_potential_defeats(self, ordering: Ordering) -> List[Defeat]:
        return [Defeat(argument_a, argument_b)
                for argument_a in self.all_potential_arguments
                for argument_b in self.all_potential_arguments
                if self.defeats(argument_a, argument_b, ordering)]
