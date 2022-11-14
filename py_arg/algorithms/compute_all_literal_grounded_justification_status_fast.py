from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.labels.enum_justification_label import EnumJustificationLabel
from py_arg.labels.literal_labels import LiteralLabels


def compute_all_literal_grounded_justification_status_fast(argumentation_theory: ArgumentationTheory,
                                                           ordering: Ordering) -> LiteralLabels:
    # Connect parents and children
    all_rules = argumentation_theory.argumentation_system.defeasible_rules + \
                argumentation_theory.argumentation_system.strict_rules
    for rule in all_rules:
        for antecedent in rule.antecedents:
            antecedent.parents.append(rule)
        rule.consequent.children.append(rule)

    # Phase 1: UNSATISFIABLE / BLOCKED labelling
    result = {literal: EnumJustificationLabel.UNSATISFIABLE
              for literal in argumentation_theory.argumentation_system.language.values()}
    todo_literals = argumentation_theory.knowledge_base_axioms + argumentation_theory.knowledge_base_ordinary_premises
    todo_rules = set()
    for literal in todo_literals:
        result[literal] = EnumJustificationLabel.BLOCKED
        for rule in literal.parents:
            todo_rules.add(rule)
    while todo_rules:
        todo_rule = todo_rules.pop()
        literal = todo_rule.consequent
        if result[literal] == EnumJustificationLabel.UNSATISFIABLE:
            if all(result[antecedent] == EnumJustificationLabel.BLOCKED for antecedent in todo_rule.antecedents):
                result[literal] = EnumJustificationLabel.BLOCKED
                for rule in literal.parents:
                    todo_rules.add(rule)

    # Phase 2: DEFENDED / OUT labelling
    # Start with all literals for which there is an unattacked argument
    todo_literals = [literal for literal in argumentation_theory.argumentation_system.language.values()
                     if literal in argumentation_theory.knowledge_base_axioms or
                     (result[literal] != EnumJustificationLabel.UNSATISFIABLE and
                      all(result[contrary_literal] == EnumJustificationLabel.UNSATISFIABLE
                          for contrary_literal in literal.contraries))
                     ]
    todo_rules = set()
    for literal in todo_literals:
        result[literal] = EnumJustificationLabel.DEFENDED
        for rule in literal.parents:
            todo_rules.add(rule)
        for contrary_literal in literal.contraries:
            if result[contrary_literal] == EnumJustificationLabel.BLOCKED:
                result[contrary_literal] = EnumJustificationLabel.OUT
                for rule in literal.parents:
                    todo_rules.add(rule)
    while todo_rules:
        todo_rule = todo_rules.pop()
        old_conclusion_label = result[todo_rule.consequent]
        if old_conclusion_label == EnumJustificationLabel.BLOCKED:
            # Maybe this literal will change label
            if all(result[antecedent] == EnumJustificationLabel.DEFENDED for antecedent in todo_rule.antecedents):
                # There is an argument based on this rule such that all subarguments are in the grounded extension.
                # Is the argument attacked on its conclusion?
                if todo_rule in argumentation_theory.argumentation_system.strict_rules or \
                        all(contrary_literal not in argumentation_theory.knowledge_base_axioms and
                            contrary_literal not in argumentation_theory.knowledge_base_ordinary_premises and
                            all(any(result[contrary_antecedent] in [EnumJustificationLabel.UNSATISFIABLE,
                                                                    EnumJustificationLabel.OUT]
                                    for contrary_antecedent in contrary_rule.antecedents)
                                for contrary_rule in contrary_literal.children)
                            for contrary_literal in todo_rule.consequent.contraries):
                    result[todo_rule.consequent] = EnumJustificationLabel.DEFENDED
                    for parent_rule in todo_rule.consequent.parents:
                        todo_rules.add(parent_rule)
                    for contrary_literal in todo_rule.consequent.contraries:
                        result[contrary_literal] = EnumJustificationLabel.OUT
                        for contrary_parent_rule in contrary_literal.parents:
                            todo_rules.add(contrary_parent_rule)
            elif any(result[antecedent] == EnumJustificationLabel.OUT for antecedent in todo_rule.antecedents):
                result[todo_rule.consequent] = EnumJustificationLabel.OUT
                for parent_rule in todo_rule.consequent.parents:
                    todo_rules.add(parent_rule)
                for contrary_literal in todo_rule.consequent.contraries:
                    for contrary_parent_rule in contrary_literal.parents:
                        todo_rules.add(contrary_parent_rule)

    return LiteralLabels(result)
