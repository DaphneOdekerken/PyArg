import itertools
from typing import List, Optional, Union

from py_arg.aspic.classes.argumentation_system import ArgumentationSystem
from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic.classes.literal import Literal
from py_arg.aspic.classes.orderings.preference_preorder import \
    PreferencePreorder


class IncompleteArgumentationTheory:
    """
    An IncompleteArgumentationTheory consists of an ArgumentationSystem, a
    knowledge base and a set of queryables.
    By adding queryables, or their negations, to the knowledge base, future
    ArgumentationTheories can be obtained.
    """

    def __init__(
            self, argumentation_system: ArgumentationSystem,
            queryables: List[Literal],
            knowledge_base_axioms: List[Literal],
            knowledge_base_ordinary_premises: List[Literal],
            ordinary_premise_preferences: Optional[PreferencePreorder] =
            None):
        self._argumentation_system = argumentation_system
        self._queryables = sorted(queryables)
        self._knowledge_base_axioms = sorted(knowledge_base_axioms)
        self._knowledge_base_ordinary_premises = sorted(
            knowledge_base_ordinary_premises)

        self._is_queryable_dict = {
            lit_str: False
            for lit_str in self.argumentation_system.language.keys()}
        for queryable in self._queryables:
            self._is_queryable_dict[queryable.s1] = True

        # Rule preferences
        if ordinary_premise_preferences:
            self.ordinary_premise_preferences = ordinary_premise_preferences
        else:
            self.ordinary_premise_preferences = \
                PreferencePreorder.create_reflexive_preorder(
                    self._knowledge_base_ordinary_premises)

    @property
    def argumentation_system(self):
        return self._argumentation_system

    @argumentation_system.setter
    def argumentation_system(self, argumentation_system_input):
        self._argumentation_system = argumentation_system_input

    @property
    def queryables(self):
        return self._queryables

    @queryables.setter
    def queryables(self, queryables_input):
        self._queryables = queryables_input

    def is_queryable(self, literal: Union[Literal, str]):
        if isinstance(literal, str):
            return self._is_queryable_dict[literal]
        return self._is_queryable_dict[literal.s1]

    @property
    def positive_queryables(self):
        return [queryable for queryable in self._queryables
                if queryable.is_positive]

    @property
    def knowledge_base(self):
        return self._knowledge_base_axioms + \
            self._knowledge_base_ordinary_premises

    @property
    def knowledge_base_axioms(self):
        return self._knowledge_base_axioms

    @knowledge_base_axioms.setter
    def knowledge_base_axioms(self, knowledge_base_axioms_input):
        self._knowledge_base_axioms = knowledge_base_axioms_input

    def add_to_knowledge_base_axioms(self, new_knowledge_base_axiom: Literal):
        self._knowledge_base_axioms.append(new_knowledge_base_axiom)

    @property
    def knowledge_base_ordinary_premises(self):
        return self._knowledge_base_ordinary_premises

    @knowledge_base_ordinary_premises.setter
    def knowledge_base_ordinary_premises(
            self, knowledge_base_ordinary_premises_input):
        self._knowledge_base_ordinary_premises = \
            knowledge_base_ordinary_premises_input

    def add_to_knowledge_base_ordinary_premises(
            self, new_knowledge_base_ordinary_premise: Literal):
        self._knowledge_base_ordinary_premises.append(
            new_knowledge_base_ordinary_premise)

    def get_all_axiom_completions(self):
        # -1: Negation of this queryable is an axiom in the knowledge base.
        # 0: This queryable remains unknown in that neither this queryable,
        # nor its negation is an axiom.
        # 1: This queryable is an axiom in the knowledge base.
        queryable_value_list = ([(queryable_str, possible_value)
                                 for possible_value in [-1, 0, 1]]
                                for queryable_str in self.positive_queryables)
        queryable_value_combinations = itertools.product(*queryable_value_list)

        def get_knowledge_base(queryable_value_combination_tuples):
            knowledge_base = []
            for queryable, value in queryable_value_combination_tuples:
                if value == -1:
                    knowledge_base.append(
                        self.argumentation_system.language[
                            '-' + str(queryable)])
                elif value == 1:
                    knowledge_base.append(queryable)
            return knowledge_base

        result = (ArgumentationTheory(
            self.argumentation_system,
            get_knowledge_base(queryable_value_combination),
            [], None)
            for queryable_value_combination in queryable_value_combinations)
        return result

    def __eq__(self, other):
        return isinstance(other, IncompleteArgumentationTheory) and \
            self.argumentation_system == other.argumentation_system and \
            self.queryables == other.queryables and \
            self.knowledge_base_axioms == other.knowledge_base_axioms and \
            self.knowledge_base_ordinary_premises == other.\
            knowledge_base_ordinary_premises and \
            self.ordinary_premise_preferences == other.\
            ordinary_premise_preferences


if __name__ == "__main__":
    import doctest
    doctest.testmod()
