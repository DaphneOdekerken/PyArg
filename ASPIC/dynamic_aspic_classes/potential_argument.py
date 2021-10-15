import itertools
from typing import Optional, Set

from ASPIC.aspic_classes.defeasible_rule import DefeasibleRule
from ASPIC.aspic_classes.literal import Literal
from ASPIC.aspic_classes.rule import Rule
from ASPIC.aspic_classes.strict_rule import StrictRule
from ASPIC.aspic_classes.instantiated_argument import InstantiatedArgument


class PotentialArgument(InstantiatedArgument):
    def __init__(self, name: str, premises: Set[Literal], conclusion: Literal,
                 direct_sub_arguments: Set[InstantiatedArgument], def_rules: Set[DefeasibleRule],
                 strict_rules: Set[StrictRule], top_rule: Optional[Rule]):
        super().__init__(name, premises, conclusion, direct_sub_arguments, def_rules, strict_rules, top_rule)

    def is_consistent(self) -> bool:
        return all([not a.is_contrary_of(b) for a, b in itertools.combinations(list(self.premises), 2)])
