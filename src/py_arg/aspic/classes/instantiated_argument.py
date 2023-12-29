from typing import Optional, Set

from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.aspic.classes.defeasible_rule import DefeasibleRule
from py_arg.aspic.classes.literal import Literal
from py_arg.aspic.classes.rule import Rule
from py_arg.aspic.classes.strict_rule import StrictRule


class InstantiatedArgument(Argument):
    def __init__(self, name: str,
                 axiom_premises: Set[Literal],
                 ordinary_premises: Set[Literal],
                 conclusion: Literal,
                 direct_sub_arguments: Set['InstantiatedArgument'],
                 defeasible_rules: Set[DefeasibleRule],
                 strict_rules: Set[StrictRule],
                 top_rule: Optional[Rule]):
        super().__init__(name)
        self.sub_conclusions = None
        self.axiom_premises = axiom_premises
        self.ordinary_premises = ordinary_premises
        self.conclusion = conclusion
        self.direct_sub_arguments = direct_sub_arguments
        self.defeasible_rules = defeasible_rules
        self.strict_rules = strict_rules
        self.top_rule = top_rule
        self.sub_conclusions = {
            sub_conclusion for dir_sub in self.direct_sub_arguments
            for sub_conclusion in dir_sub.sub_conclusions}
        self.sub_conclusions.add(self.conclusion)
        self.short_name = self.name.replace(' (axiom)', '').replace(
            ' (ordinary premise)', '')

    @classmethod
    def axiom_based(cls, conclusion: Literal):
        return cls(str(conclusion) + ' (axiom)', {conclusion}, set(),
                   conclusion, set(), set(), set(), None)

    @classmethod
    def ordinary_premise_based(cls, conclusion: Literal):
        return cls(str(conclusion) + ' (ordinary premise)', set(),
                   {conclusion}, conclusion, set(), set(), set(), None)

    @classmethod
    def strict_rule_based(cls, strict_rule: StrictRule,
                          direct_sub_arguments: Set['InstantiatedArgument']):
        direct_sub_argument_conclusions = sorted([
            sub_argument.conclusion
            for sub_argument in direct_sub_arguments])
        if direct_sub_argument_conclusions != sorted(strict_rule.antecedents):
            raise ValueError(
                'Strict rule does not match with direct subarguments.')

        name = '[' + ','.join(sorted(sub.name
                                     for sub in direct_sub_arguments)) \
               + '->' + str(strict_rule.consequent) + ']'
        axiom_premises = set().union(*[
            sub_argument.axiom_premises
            for sub_argument in direct_sub_arguments])
        ordinary_premises = set().union(*[
            sub_argument.ordinary_premises
            for sub_argument in direct_sub_arguments])
        conclusion = strict_rule.consequent
        def_rules = set().union(*[
            sub_argument.defeasible_rules
            for sub_argument in direct_sub_arguments])
        strict_rules = {strict_rule}.union(*[
            sub_argument.strict_rules
            for sub_argument in direct_sub_arguments])
        return cls(name, axiom_premises, ordinary_premises, conclusion,
                   direct_sub_arguments, def_rules,
                   strict_rules, strict_rule)

    @classmethod
    def defeasible_rule_based(
            cls, defeasible_rule: DefeasibleRule,
            direct_sub_arguments: Set['InstantiatedArgument']):
        direct_sub_argument_conclusions = sorted([
            sub_argument.conclusion for sub_argument in direct_sub_arguments])
        if direct_sub_argument_conclusions != sorted(
                defeasible_rule.antecedents):
            raise ValueError('Strict rule does not match direct subarguments.')

        name = '[' + ','.join([sub.name
                               for sub in direct_sub_arguments]) + '=>' + \
               str(defeasible_rule.consequent) + ']'
        axiom_premises = set().union(*[
            sub_argument.axiom_premises
            for sub_argument in direct_sub_arguments])
        ordinary_premises = set().union(*[
            sub_argument.ordinary_premises
            for sub_argument in direct_sub_arguments])
        conclusion = defeasible_rule.consequent
        def_rules = {defeasible_rule}.union(*[
            sub_argument.defeasible_rules
            for sub_argument in direct_sub_arguments])
        strict_rules = set().union(*[
            sub_argument.strict_rules
            for sub_argument in direct_sub_arguments])
        return cls(name, axiom_premises, ordinary_premises, conclusion,
                   direct_sub_arguments, def_rules,
                   strict_rules, defeasible_rule)

    @property
    def premises(self):
        return self.axiom_premises | self.ordinary_premises

    @property
    def is_observation_based(self):
        return self.top_rule is None

    @property
    def is_rule_based(self):
        return self.top_rule is not None

    @property
    def sub_arguments(self) -> Set['InstantiatedArgument']:
        return {self}.union(*[sub_argument.sub_arguments
                              for sub_argument in self.direct_sub_arguments])

    @property
    def last_defeasible_rules(self) -> Set[DefeasibleRule]:
        if self.is_observation_based:
            return set()
        if self.is_rule_based and isinstance(self.top_rule, DefeasibleRule):
            return {self.top_rule}
        return set().union(*[dir_sub.last_defeasible_rules
                             for dir_sub in self.direct_sub_arguments])

    @property
    def is_strict(self) -> bool:
        return not self.defeasible_rules

    @property
    def is_defeasible(self) -> bool:
        return not self.is_strict

    @property
    def is_firm(self) -> bool:
        return not self.ordinary_premises

    @property
    def is_plausible(self) -> bool:
        return not self.is_firm

    @property
    def is_fallible(self) -> bool:
        return self.is_defeasible or self.is_plausible

    @property
    def is_c_consistent(self) -> bool:
        closure = self._get_closure(self.premises, self.strict_rules)
        return any(literal_a in literal_b.contraries_and_contradictories
                   for literal_a in closure for literal_b in closure)

    @staticmethod
    def _get_closure(literals: Set[Literal], strict_rules: Set[StrictRule]):
        closure = literals.copy()
        change = True
        while change:
            change = False
            interesting_strict_rules = \
                {strict_rule for strict_rule in strict_rules
                 if strict_rule.consequent not in closure}
            for strict_rule in interesting_strict_rules:
                if all([antecedent in closure
                        for antecedent in strict_rule.antecedents]):
                    closure.add(strict_rule.consequent)
                    change = True
        return closure
