from py_arg.algorithms.classes.connected_literal import \
    connect_parents_and_children
from py_arg.algorithms.stability.stability_labels import StabilityLabels
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.rule import Rule
from py_arg.incomplete_aspic_classes.incomplete_argumentation_theory import IncompleteArgumentationTheory


class FourBoolRelevanceLister:
    def __init__(self):
        self.relevance_list = dict()
        self.u_relevant_literal = None
        self.d_relevant_literal = None
        self.o_relevant_literal = None
        self.b_relevant_literal = None
        self.u_relevant_rule = None
        self.d_relevant_rule = None
        self.o_relevant_rule = None
        self.b_relevant_rule = None
        self.four_bool_labels = None
        self.relevance_visited = None
        self.parents = None
        self.children = None

    def update(self, iat: IncompleteArgumentationTheory,
               four_bool_labels: StabilityLabels,
               parents=None,
               children=None):
        literals = iat.argumentation_system.language.values()
        rules = iat.argumentation_system.rules

        if parents and children:
            self.parents = parents
            self.children = children
        else:
            # Connect literals, so we can ask for their children and parents
            self.parents, self.children = connect_parents_and_children(iat)

        self.u_relevant_literal = {literal: set() for literal in literals}
        self.d_relevant_literal = {literal: set() for literal in literals}
        self.o_relevant_literal = {literal: set() for literal in literals}
        self.b_relevant_literal = {literal: set() for literal in literals}
        self.u_relevant_rule = {rule: set() for rule in rules}
        self.d_relevant_rule = {rule: set() for rule in rules}
        self.o_relevant_rule = {rule: set() for rule in rules}
        self.b_relevant_rule = {rule: set() for rule in rules}

        self.four_bool_labels = four_bool_labels

        # Start by collecting relevant observables of leaves (or-nodes for which there is no rule) and observables
        nodes_to_update_relevancy_round = \
            [literal for literal in literals
             if not self.children[literal.s1] or iat.is_queryable(literal)]

        while nodes_to_update_relevancy_round:
            # Update literals
            new_rules_to_update_relevancy = set()
            for literal in nodes_to_update_relevancy_round:
                old_relevancy = self._get_current_relevancy_for_literal(literal)
                self._update_relevant_literals_for_literal(iat,
                                                           literal, iat.knowledge_base)
                new_relevancy = self._get_current_relevancy_for_literal(literal)
                if old_relevancy != new_relevancy:
                    new_rules_to_update_relevancy = new_rules_to_update_relevancy | set(self.parents[literal.s1])
            nodes_to_update_relevancy_round = new_rules_to_update_relevancy

            # Update rules
            new_literals_to_update_relevancy = set()
            for rule in nodes_to_update_relevancy_round:
                old_relevancy = self._get_current_relevancy_for_rule(rule)
                self._update_relevant_literals_for_rule(rule)
                new_relevancy = self._get_current_relevancy_for_rule(rule)
                if old_relevancy != new_relevancy:
                    new_literals_to_update_relevancy = new_literals_to_update_relevancy | set(
                        [rule.consequent] + list(rule.consequent.contraries_and_contradictories))
            nodes_to_update_relevancy_round = new_literals_to_update_relevancy

        for literal in literals:
            self.relevance_list[literal] = self._get_current_relevancy_for_literal(literal)

    def _get_current_relevancy_for_literal(self, literal: Literal):
        return self.u_relevant_literal[literal] | self.d_relevant_literal[literal] | \
               self.o_relevant_literal[literal] | self.b_relevant_literal[literal]

    def _get_current_relevancy_for_rule(self, rule: Rule):
        return self.u_relevant_rule[rule] | self.d_relevant_rule[rule] | \
               self.o_relevant_rule[rule] | self.b_relevant_rule[rule]

    def _lit_label(self, literal: Literal):
        return self.four_bool_labels.literal_labeling[literal]

    def _rule_label(self, rule: Rule):
        return self.four_bool_labels.rule_labeling[rule]

    def _update_relevant_literals_for_literal(self, incomplete_argumentation_theory: IncompleteArgumentationTheory,
                                              literal: Literal, knowledge_base):
        self._update_relevant_literals_u_literal(incomplete_argumentation_theory, knowledge_base, literal)
        self._update_relevant_literals_d_literal(incomplete_argumentation_theory, knowledge_base, literal)
        self._update_relevant_literals_o_literal(incomplete_argumentation_theory, knowledge_base, literal)
        self._update_relevant_literals_b_literal(incomplete_argumentation_theory, literal)

    def _update_relevant_literals_for_rule(self, rule: Rule):
        self._update_relevant_literals_u_rule(rule)
        self._update_relevant_literals_d_rule(rule)
        self._update_relevant_literals_o_rule(rule)
        self._update_relevant_literals_b_rule(rule)

    def _update_relevant_literals_u_literal(self, incomplete_argumentation_theory, knowledge_base, literal):
        u_relevant = set()

        if self._lit_label(literal).unsatisfiable:
            if incomplete_argumentation_theory.is_queryable(literal):
                if literal not in knowledge_base and all([contrary not in knowledge_base
                                                          for contrary in literal.contraries_and_contradictories]):
                    u_relevant.add(literal)

            for rule in self.children[literal.s1]:
                if self._rule_label(rule).unsatisfiable:
                    u_relevant = u_relevant | self.u_relevant_rule[rule]

        self.u_relevant_literal[literal] = u_relevant

    def _update_relevant_literals_d_literal(self, incomplete_argumentation_theory, knowledge_base, literal):
        d_relevant = set()

        if self._lit_label(literal).defended:
            if incomplete_argumentation_theory.is_queryable(literal):
                if literal not in knowledge_base and \
                        all([contrary not in knowledge_base for contrary in literal.contraries_and_contradictories]):
                    for contrary in literal.contraries_and_contradictories:
                        if all([contrary_contrary not in knowledge_base for contrary_contrary in contrary.contraries_and_contradictories]):
                            d_relevant.add(contrary)
            else:
                if all([self._rule_label(rule).unsatisfiable or self._rule_label(rule).out
                        or self._rule_label(rule).blocked
                        for rule in self.children[literal.s1]]):
                    for rule in self.children[literal.s1]:
                        if self._rule_label(rule).defended:
                            d_relevant = d_relevant | self.d_relevant_rule[rule]

                for contrary in literal.contraries_and_contradictories:
                    for contrary_rule in self.children[contrary.s1]:
                        if self._rule_label(contrary_rule).defended or self._rule_label(contrary_rule).blocked:
                            if self._rule_label(contrary_rule).unsatisfiable:
                                d_relevant = d_relevant | self.u_relevant_rule[contrary_rule]
                            if self._rule_label(contrary_rule).out:
                                d_relevant = d_relevant | self.o_relevant_rule[contrary_rule]

        self.d_relevant_literal[literal] = d_relevant

    def _update_relevant_literals_o_literal(self, incomplete_argumentation_theory, knowledge_base, literal):
        o_relevant = set()

        if self._lit_label(literal).out:
            if all([self._rule_label(rule).unsatisfiable for rule in self.children[literal.s1]]):
                for rule in self.children[literal.s1]:
                    if self._rule_label(rule).defended:
                        o_relevant = o_relevant | self.d_relevant_rule[rule]
                    if self._rule_label(rule).out:
                        o_relevant = o_relevant | self.o_relevant_rule[rule]
                    if self._rule_label(rule).blocked:
                        o_relevant = o_relevant | self.b_relevant_rule[rule]

            if incomplete_argumentation_theory.is_queryable(literal):
                if literal not in knowledge_base and all([contrary not in knowledge_base
                                                          for contrary in literal.contraries_and_contradictories]):
                    o_relevant.add(literal)
            else:
                if all([self._rule_label(rule).unsatisfiable or self._rule_label(rule).defended
                        or self._rule_label(rule).blocked
                        for rule in self.children[literal.s1]]):
                    for rule in self.children[literal.s1]:
                        o_relevant = o_relevant | self.o_relevant_rule[rule]
                for rule in self.children[literal.s1]:
                    if self._rule_label(rule).defended or self._rule_label(rule).blocked:
                        if self._rule_label(rule).unsatisfiable:
                            o_relevant = o_relevant | self.u_relevant_rule[rule]
                        if self._rule_label(rule).out:
                            o_relevant = o_relevant | self.o_relevant_rule[rule]

        self.o_relevant_literal[literal] = o_relevant

    def _update_relevant_literals_b_literal(self, incomplete_argumentation_theory, literal):
        b_relevant = set()

        if self._lit_label(literal).blocked and not incomplete_argumentation_theory.is_queryable(literal):
            if all([self._rule_label(rule).unsatisfiable or self._rule_label(rule).out for rule in self.children[literal.s1]]):
                for rule in self.children[literal.s1]:
                    if self._rule_label(rule).defended:
                        b_relevant = b_relevant | self.d_relevant_rule[rule]
                    if self._rule_label(rule).blocked:
                        b_relevant = b_relevant | self.b_relevant_rule[rule]

            if all([self._rule_label(contrary_rule).unsatisfiable or self._rule_label(contrary_rule).out
                    for contrary in literal.contraries_and_contradictories for contrary_rule in self.children[contrary.s1]]):
                if all([self._rule_label(rule).unsatisfiable or self._rule_label(rule).defended
                        or self._rule_label(rule).out
                        for rule in self.children[literal.s1]]):
                    for rule in self.children[literal.s1]:
                        if self._rule_label(rule).blocked:
                            b_relevant = b_relevant | self.b_relevant_rule[rule]
                    for contrary in literal.contraries_and_contradictories:
                        for contrary_rule in self.children[contrary.s1]:
                            if self._rule_label(contrary_rule).defended:
                                b_relevant = b_relevant | self.d_relevant_rule[contrary_rule]
                            if self._rule_label(contrary_rule).blocked:
                                b_relevant = b_relevant | self.b_relevant_rule[contrary_rule]

                for rule in self.children[literal.s1]:
                    if self._rule_label(rule).defended:
                        if self._rule_label(rule).unsatisfiable:
                            b_relevant = b_relevant | self.u_relevant_rule[rule]
                        if self._rule_label(rule).out:
                            b_relevant = b_relevant | self.o_relevant_rule[rule]
                        if self._rule_label(rule).blocked:
                            b_relevant = b_relevant | self.b_relevant_rule[rule]
                for contrary in literal.contraries_and_contradictories:
                    for contrary_rule in self.children[contrary.s1]:
                        if self._rule_label(contrary_rule).defended:
                            b_relevant = b_relevant | self.d_relevant_rule[contrary_rule]
                        if self._rule_label(contrary_rule).blocked:
                            b_relevant = b_relevant | self.b_relevant_rule[contrary_rule]

        self.b_relevant_literal[literal] = b_relevant

    def _update_relevant_literals_u_rule(self, rule):
        u_relevant = set()

        if self._rule_label(rule).unsatisfiable and \
                all([self._lit_label(literal).defended or self._lit_label(literal).out
                     or self._lit_label(literal).blocked
                     for literal in rule.antecedents]):
            for literal in rule.antecedents:
                if self._lit_label(literal).unsatisfiable:
                    u_relevant = u_relevant | self.u_relevant_literal[literal]

        self.u_relevant_rule[rule] = u_relevant

    def _update_relevant_literals_d_rule(self, rule):
        d_relevant = set()

        if self._rule_label(rule).defended:
            for literal in rule.antecedents:
                if self._lit_label(literal).defended:
                    d_relevant = d_relevant | self.d_relevant_literal[literal]

        self.d_relevant_rule[rule] = d_relevant

    def _update_relevant_literals_o_rule(self, rule):
        o_relevant = set()

        if self._rule_label(rule).out:
            if all([self._lit_label(literal).unsatisfiable or self._lit_label(literal).defended
                    or self._lit_label(literal).blocked
                    for literal in rule.antecedents]):
                for literal in rule.antecedents:
                    if self._lit_label(literal).out:
                        o_relevant = o_relevant | self.o_relevant_literal[literal]

            for literal in rule.antecedents:
                if self._lit_label(literal).unsatisfiable:
                    if self._lit_label(literal).defended:
                        o_relevant = o_relevant | self.d_relevant_literal[literal]
                    if self._lit_label(literal).out:
                        o_relevant = o_relevant | self.o_relevant_literal[literal]
                    if self._lit_label(literal).blocked:
                        o_relevant = o_relevant | self.b_relevant_literal[literal]

        self.o_relevant_rule[rule] = o_relevant

    def _update_relevant_literals_b_rule(self, rule):
        b_relevant = set()

        if self._rule_label(rule).blocked:
            if all([self._lit_label(literal).unsatisfiable or self._lit_label(literal).defended or
                    self._lit_label(literal).blocked
                    for literal in rule.antecedents]):
                for literal in rule.antecedents:
                    if self._lit_label(literal).blocked:
                        b_relevant = b_relevant | self.b_relevant_literal[literal]

            for literal in rule.antecedents:
                if self._lit_label(literal).unsatisfiable or self._lit_label(literal).out:
                    if self._lit_label(literal).defended:
                        b_relevant = b_relevant | self.d_relevant_literal[literal]
                    if self._lit_label(literal).blocked:
                        b_relevant = b_relevant | self.b_relevant_literal[literal]

        self.b_relevant_rule[rule] = b_relevant
