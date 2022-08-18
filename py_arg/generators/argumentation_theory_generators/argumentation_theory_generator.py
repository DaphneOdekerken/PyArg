import random

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.axiom import Axiom
from py_arg.aspic_classes.ordinary_premise import OrdinaryPremise


class ArgumentationTheoryGenerator:
    def __init__(self, argumentation_system: ArgumentationSystem, knowledge_literal_ratio: float,
                 axiom_knowledge_ratio: float):
        self.argumentation_system = argumentation_system

        if knowledge_literal_ratio > 0.5:
            raise ValueError('At most half of the literals can be in the knowledge base.')
        if knowledge_literal_ratio < 0:
            raise ValueError('The knowledge literal ratio should be at least one.')
        self.knowledge_literal_ratio = knowledge_literal_ratio

        if axiom_knowledge_ratio < 0 or axiom_knowledge_ratio > 1:
            raise ValueError('The axiom knowledge ratio should be between zero and one.')
        self.axiom_knowledge_ratio = axiom_knowledge_ratio

    def generate(self) -> ArgumentationTheory:
        nr_of_literals = len(self.argumentation_system.language)
        knowledge_base_size = int(self.knowledge_literal_ratio * nr_of_literals)

        knowledge_base_candidates = list(self.argumentation_system.language.values())
        knowledge_base = []
        for _ in range(knowledge_base_size):
            if not knowledge_base_candidates:
                raise ValueError('Could not construct such a large knowledge base given the contradictories.')
            new_knowledge = random.choice(knowledge_base_candidates)
            knowledge_base.append(new_knowledge)
            knowledge_base_candidates.remove(new_knowledge)
            for new_knowledge_contrary in new_knowledge.contraries:
                knowledge_base_candidates.remove(new_knowledge_contrary)

        axiom_size = int(knowledge_base_size * self.axiom_knowledge_ratio)
        axiom_indices = random.sample(range(knowledge_base_size), axiom_size)
        axioms = [knowledge_base[i] for i in axiom_indices]
        for axiom in axioms:
            axiom.__class__ = Axiom

        ordinary_premises = [knowledge_base[i] for i in range(knowledge_base_size)
                             if i not in axiom_indices]
        for ordinary_premise in ordinary_premises:
            ordinary_premise.__class__ = OrdinaryPremise

        return ArgumentationTheory(argumentation_system=self.argumentation_system,
                                   knowledge_base_axioms=axioms,
                                   knowledge_base_ordinary_premises=ordinary_premises)
