from py_arg.aspic.classes.argumentation_system import ArgumentationSystem
from py_arg.aspic.classes.defeasible_rule import DefeasibleRule
from py_arg.aspic.classes.literal import Literal
from py_arg.aspic.classes.orderings.preference_preorder import \
    PreferencePreorder
from py_arg.incomplete_aspic.classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


class IncompleteArgumentationTheoryFromLPFileReader:
    def __init__(self):
        pass

    @staticmethod
    def read_from_lp_file(file_path: str) -> IncompleteArgumentationTheory:
        positive_queryable_strs = []
        axiom_strs = []
        defeasible_rule_bodies = []
        defeasible_rule_heads = []
        contradiction_pairs = []
        preferred_pairs = []

        reader = open(file_path, 'r')
        for line in reader:
            if line.startswith('queryable'):
                positive_queryable_strs.append(line.split(
                    '(', 1)[1].split(')', 1)[0])
            if line.startswith('axiom'):
                axiom_strs.append(line.split('(', 1)[1].split(')', 1)[0])
            if line.startswith('body'):
                defeasible_rule_bodies.append((line.split(
                    '(', 1)[1].split(')', 1)[0]).split(', ', 1))
            if line.startswith('head'):
                defeasible_rule_heads.append((line.split(
                    '(', 1)[1].split(')', 1)[0]).split(', ', 1))
            if line.startswith('neg'):
                contradiction_pairs.append((line.split(
                    '(', 1)[1].split(')', 1)[0]).split(', ', 1))
            if line.startswith('preferred'):
                preferred_pairs.append((line.split(
                    '(', 1)[1].split(')', 1)[0]).split(', ', 1))
        reader.close()

        all_positive_literals = set(positive_queryable_strs)
        for axiom in axiom_strs:
            all_positive_literals.add(axiom.replace('-', ''))
        for defeasible_rule_head in defeasible_rule_heads:
            all_positive_literals.add(defeasible_rule_head[1].replace('-', ''))
        for defeasible_rule_body in defeasible_rule_bodies:
            all_positive_literals.add(defeasible_rule_body[1].replace('-', ''))
        for contradiction_pair in contradiction_pairs:
            all_positive_literals.add(contradiction_pair[0])
        all_negative_literals = {'-' + pos_literal
                                 for pos_literal in all_positive_literals}
        all_literals = all_positive_literals | all_negative_literals
        language = {lit_str: Literal(lit_str) for lit_str in all_literals}

        contraries_and_contradictories = {}
        for pos, neg in contradiction_pairs:
            contraries_and_contradictories[pos] = {language[neg]}
            contraries_and_contradictories[neg] = {language[pos]}

        defeasible_rules = []
        for rule_nr, rule_head in defeasible_rule_heads:
            rule_antecedents = [
                rule_body_literal
                for rule_body_nr, rule_body_literal in defeasible_rule_bodies
                if rule_body_nr == rule_nr]
            defeasible_rule = DefeasibleRule(
                rule_nr, {language[ant_str] for ant_str in rule_antecedents},
                language[rule_head])
            defeasible_rules.append(defeasible_rule)

        def_rules_lookup = {defeasible_rule.id: defeasible_rule
                            for defeasible_rule in defeasible_rules}
        preference_preorder = PreferencePreorder(
            [(def_rules_lookup[rule_a], def_rules_lookup[rule_b])
             for rule_a, rule_b in preferred_pairs])

        argumentation_system = ArgumentationSystem(
            language=language,
            contraries_and_contradictories=contraries_and_contradictories,
            strict_rules=[], defeasible_rules=defeasible_rules,
            defeasible_rule_preferences=preference_preorder,
            add_defeasible_rule_literals=False)

        negative_queryable_strs = [
            '-' + queryable for queryable in positive_queryable_strs]
        queryables = [
            language[queryable]
            for queryable in positive_queryable_strs + negative_queryable_strs]
        knowledge_base_axioms = [
            language[axiom_str] for axiom_str in axiom_strs]

        return IncompleteArgumentationTheory(
            argumentation_system=argumentation_system,
            queryables=queryables,
            knowledge_base_axioms=knowledge_base_axioms,
            knowledge_base_ordinary_premises=[],
            ordinary_premise_preferences=None
        )
