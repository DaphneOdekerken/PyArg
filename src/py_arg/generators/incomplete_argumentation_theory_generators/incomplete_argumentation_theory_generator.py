import random
from typing import Optional, List

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.literal import Literal
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory


class IncompleteArgumentationTheoryGenerator:
    def __init__(self, argumentation_system: ArgumentationSystem,
                 positive_queryable_candidates: Optional[List[Literal]] = None,
                 queryable_literal_ratio: float = 0.4,
                 knowledge_queryable_ratio: float = 0.2,
                 axiom_knowledge_ratio: float = 0.5):
        """
        Initialise the IncompleteArgumentationTheoryGenerator.

        Note: we assume that the contradiction function in the argumentation system only consists of negations.

        :param argumentation_system: The argumentation system based on which this IncompleteArgumentationTheory will be.
        :param positive_queryable_candidates: Literals that are positive and may be queryable.
        :param queryable_literal_ratio: Number of queryables compared to number of literals.
        :param knowledge_queryable_ratio: Number of knowledge base items compared to number of positive queryables.
        :param axiom_knowledge_ratio: Number of axioms compared to number of knowledge base items.
        """
        self.argumentation_system = argumentation_system

        if queryable_literal_ratio < 0 or queryable_literal_ratio > 1:
            raise ValueError('The queryable literal ratio should be between zero and one.')
        self.queryable_literal_ratio = queryable_literal_ratio

        if knowledge_queryable_ratio < 0 or knowledge_queryable_ratio > 1:
            raise ValueError('The knowledge queryable ratio should be between zero and one.')
        self.knowledge_queryable_ratio = knowledge_queryable_ratio

        if axiom_knowledge_ratio < 0 or axiom_knowledge_ratio > 1:
            raise ValueError('The axiom knowledge ratio should be between zero and one.')
        self.axiom_knowledge_ratio = axiom_knowledge_ratio

        # Find the positive literals in the ArgumentationSystem.
        normal_literals = [literal for literal_str, literal in self.argumentation_system.language.items()
                           if 'd' not in literal_str]
        self.positive_literals = [literal for literal in normal_literals if literal.is_positive]

        if positive_queryable_candidates:
            self.positive_queryable_candidates = positive_queryable_candidates
        else:
            self.positive_queryable_candidates = self.positive_literals

        self.nr_of_positive_queryables = int(queryable_literal_ratio * len(self.positive_literals))
        knowledge_base_size = int(self.nr_of_positive_queryables * self.knowledge_queryable_ratio)
        self.axiom_size = int(knowledge_base_size * self.axiom_knowledge_ratio)
        self.ordinary_premise_size = knowledge_base_size - self.axiom_size

    def generate(self) -> IncompleteArgumentationTheory:
        # Sample the queryables from the set of literals.
        positive_queryables = random.sample(self.positive_queryable_candidates, self.nr_of_positive_queryables)
        negative_queryables = [self.argumentation_system.language['-' + str(pos_q)]
                               for pos_q in positive_queryables]
        queryables = positive_queryables + negative_queryables

        # Sample the axioms from the set of queryables, making sure that the axioms are consistent.
        axioms = []
        axiom_candidates = queryables.copy()
        for _ in range(self.axiom_size - 1):
            if not axiom_candidates:
                raise ValueError('Could not construct such a large knowledge base given the contradictories.')
            new_axiom = random.choice(axiom_candidates)
            axioms.append(new_axiom)
            axiom_candidates.remove(new_axiom)
            for new_axiom_contrary in new_axiom.contraries_and_contradictories:
                axiom_candidates.remove(new_axiom_contrary)

        # Finally, sample the ordinary premises.
        ordinary_premise_candidates = [queryable for queryable in queryables if queryable not in axioms]
        ordinary_premises = random.sample(ordinary_premise_candidates, self.ordinary_premise_size)

        return IncompleteArgumentationTheory(
            argumentation_system=self.argumentation_system,
            queryables=queryables,
            knowledge_base_axioms=axioms,
            knowledge_base_ordinary_premises=ordinary_premises)
