from typing import Optional, Set

from ASPIC.abstract_argumentation_classes.argument import Argument
from ASPIC.aspic_classes.axiom import Axiom
from ASPIC.aspic_classes.defeasible_rule import DefeasibleRule
from ASPIC.aspic_classes.literal import Literal
from ASPIC.aspic_classes.ordinary_premise import OrdinaryPremise
from ASPIC.aspic_classes.rule import Rule
from ASPIC.aspic_classes.strict_rule import StrictRule
from ASPIC.logic.is_c_consistent import is_c_consistent


class InstantiatedArgument(Argument):
    def __init__(self, name: str, premises: Set[Literal], conclusion: Literal,
                 direct_sub_arguments: Set['InstantiatedArgument'], defeasible_rules: Set[DefeasibleRule],
                 strict_rules: Set[StrictRule], top_rule: Optional[Rule]):
        super().__init__(name)
        self.premises = premises
        self.conclusion = conclusion
        self.direct_sub_arguments = direct_sub_arguments
        self.defeasible_rules = defeasible_rules
        self.strict_rules = strict_rules
        self.top_rule = top_rule

    def __repr__(self):
        return self.name

    def __lt__(self, other):
        return str(self).__lt__(str(other))

    @classmethod
    def observation_based(cls, conclusion: Literal):
        return cls(str(conclusion), {conclusion}, conclusion, set(), set(), set(), None)

    @classmethod
    def strict_rule_based(cls, strict_rule: StrictRule, direct_sub_arguments: Set['InstantiatedArgument']):
        direct_sub_argument_conclusions = sorted([sub_argument.conclusion for sub_argument in direct_sub_arguments])
        if direct_sub_argument_conclusions != sorted(strict_rule.antecedents):
            raise ValueError('Strict rule does not match with direct subarguments.')

        name = '[' + ','.join(sorted(sub.name for sub in direct_sub_arguments)) \
               + '->' + str(strict_rule.consequent) + ']'
        premises = set().union(*[sub_argument.premises for sub_argument in direct_sub_arguments])
        conclusion = strict_rule.consequent
        def_rules = set().union(*[sub_argument.defeasible_rules for sub_argument in direct_sub_arguments])
        strict_rules = {strict_rule}.union(*[sub_argument.strict_rules for sub_argument in direct_sub_arguments])
        return cls(name, premises, conclusion, direct_sub_arguments, def_rules, strict_rules, strict_rule)

    @classmethod
    def defeasible_rule_based(cls, defeasible_rule: DefeasibleRule, direct_sub_arguments: Set['InstantiatedArgument']):
        direct_sub_argument_conclusions = sorted([sub_argument.conclusion for sub_argument in direct_sub_arguments])
        if direct_sub_argument_conclusions != sorted(defeasible_rule.antecedents):
            raise ValueError('Strict rule does not match direct subarguments.')

        name = '[' + ','.join([sub.name for sub in direct_sub_arguments]) + '=>' + \
               str(defeasible_rule.consequent) + ']'
        premises = set().union(*[sub_argument.premises for sub_argument in direct_sub_arguments])
        conclusion = defeasible_rule.consequent
        def_rules = {defeasible_rule}.union(*[sub_argument.defeasible_rules for sub_argument in direct_sub_arguments])
        strict_rules = set().union(*[sub_argument.strict_rules for sub_argument in direct_sub_arguments])
        return cls(name, premises, conclusion, direct_sub_arguments, def_rules, strict_rules, defeasible_rule)

    @property
    def is_observation_based(self):
        return self.top_rule is None

    @property
    def is_rule_based(self):
        return self.top_rule is not None

    @property
    def sub_arguments(self) -> Set['InstantiatedArgument']:
        return {self}.union(*[sub_argument.sub_arguments for sub_argument in self.direct_sub_arguments])

    @property
    def last_defeasible_rules(self) -> Set[DefeasibleRule]:
        if self.is_observation_based:
            return set()
        if self.is_rule_based and isinstance(self.top_rule, DefeasibleRule):
            return {self.top_rule}
        return set().union(*[dir_sub.last_defeasible_rules for dir_sub in self.direct_sub_arguments])

    @property
    def ordinary_premises(self) -> Set[OrdinaryPremise]:
        return {premise for premise in self.premises if isinstance(premise, OrdinaryPremise)}

    @property
    def axiom_premises(self) -> Set[Axiom]:
        return {premise for premise in self.premises if isinstance(premise, Axiom)}

    @property
    def is_strict(self) -> bool:
        return len(self.defeasible_rules) == 0

    @property
    def is_defeasible(self) -> bool:
        return not self.is_strict

    @property
    def is_firm(self) -> bool:
        return all([isinstance(premise, Axiom) for premise in self.premises])

    @property
    def is_plausible(self) -> bool:
        return any([isinstance(premise, OrdinaryPremise) for premise in self.premises])

    @property
    def is_fallible(self) -> bool:
        return self.is_defeasible or self.is_plausible

    @property
    def is_c_consistent(self) -> bool:
        return is_c_consistent(self.premises, self.strict_rules)
