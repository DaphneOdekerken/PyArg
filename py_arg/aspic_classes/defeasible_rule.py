from typing import Set, List

from .literal import Literal
from .rule import Rule


class DefeasibleRule(Rule):
    def __init__(self, rule_id: int, antecedents: Set[Literal], consequent: Literal):
        super().__init__(rule_id, antecedents, consequent)

    def __repr__(self):
        return ','.join([str(antecedent) for antecedent in self.antecedents]) + '=>' + str(self.consequent)

    @property
    def id_str(self) -> str:
        return str(self.id)
