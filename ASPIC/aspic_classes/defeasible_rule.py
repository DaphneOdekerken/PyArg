from typing import Set, List

from .literal import Literal
from .rule import Rule


class DefeasibleRule(Rule):
    def __init__(self, rule_id: int, antecedents: Set[Literal], consequent: Literal, rule_description: str):
        super().__init__(rule_id, antecedents, consequent, rule_description)
        self._stronger_rules = []
        self._equally_strong_rules = []
        self._weaker_rules = []

    def __repr__(self):
        return ','.join([str(antecedent) for antecedent in self.antecedents]) + '=>' + str(self.consequent)

    @property
    def id_str(self) -> str:
        return 'd' + str(self.id)

    def add_stronger_rule(self, other_rule: 'DefeasibleRule'):
        self._stronger_rules.append(other_rule)

    def add_equally_strong_rule(self, other_rule: 'DefeasibleRule'):
        self._equally_strong_rules.append(other_rule)

    def add_weaker_rule(self, other_rule: 'DefeasibleRule'):
        self._weaker_rules.append(other_rule)

    @property
    def get_stronger_rules(self) -> List['DefeasibleRule']:
        return self._stronger_rules

    @property
    def get_equally_strong_rules(self) -> List['DefeasibleRule']:
        return self._equally_strong_rules

    @property
    def get_weaker_rules(self) -> List['DefeasibleRule']:
        return self._weaker_rules

    @property
    def get_stronger_or_equal_rules(self) -> List['DefeasibleRule']:
        return self.get_stronger_rules + self.get_equally_strong_rules

    @property
    def get_weaker_or_equal_rules(self) -> List['DefeasibleRule']:
        return self.get_weaker_or_equal_rules + self.get_equally_strong_rules
