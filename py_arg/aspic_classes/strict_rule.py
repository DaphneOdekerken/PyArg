from typing import Set

from .literal import Literal
from .rule import Rule


class StrictRule(Rule):
    def __init__(self, rule_id: int, antecedents: Set[Literal], consequent: Literal, rule_description: str):
        super().__init__(rule_id, antecedents, consequent, rule_description)

    def __repr__(self):
        return ','.join([str(antecedent) for antecedent in self.antecedents]) + '->' + str(self.consequent)

    def __str__(self):
        return self.__repr__()
