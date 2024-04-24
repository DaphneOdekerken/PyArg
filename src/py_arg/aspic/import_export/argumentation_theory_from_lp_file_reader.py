from py_arg.aspic.classes.argumentation_system import ArgumentationSystem
from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic.classes.defeasible_rule import DefeasibleRule
from py_arg.aspic.classes.literal import Literal
from py_arg.aspic.classes.orderings.preference_preorder import \
    PreferencePreorder
from py_arg.aspic.classes.strict_rule import StrictRule


class ArgumentationTheoryFromLPFileReader:
    def __init__(self):
        pass

    @staticmethod
    def read_from_lp_file(file_path: str) -> ArgumentationTheory:
        axiom_strs = []
        premise_strs = []
        defeasible_rule_bodies = []
        defeasible_rule_heads = []
        strict_rule_bodies = []
        strict_rule_heads = []
        contradiction_pairs = []
        preferred_pairs = []

        def get_argument(line_str):
            return line_str.split('(', 1)[1].split(')', 1)[0].strip()

        def get_arguments(line_str):
            args = (line_str.split('(', 1)[1].split(')', 1)[0]).split(',', 1)
            return args[0].strip(), args[1].strip()

        reader = open(file_path, 'r')
        for line in reader:
            if line.startswith('axiom'):
                axiom_strs.append(get_argument(line))
            elif line.startswith('premise'):
                premise_strs.append(get_argument(line))
            elif line.startswith('body'):
                defeasible_rule_bodies.append(get_arguments(line))
            elif line.startswith('head'):
                defeasible_rule_heads.append(get_arguments(line))
            elif line.startswith('strict_body'):
                strict_rule_bodies.append(get_arguments(line))
            elif line.startswith('strict_head'):
                strict_rule_heads.append(get_arguments(line))
            elif line.startswith('contrary'):
                contradiction_pairs.append(get_arguments(line))
            elif line.startswith('contradictory'):
                contra_1, contra_2 = get_arguments(line)
                contradiction_pairs.append((contra_1, contra_2))
                contradiction_pairs.append((contra_2, contra_1))
            elif line.startswith('preferred'):
                preferred_pairs.append(get_arguments(line))
        reader.close()

        all_literals = set()
        for axiom in axiom_strs:
            all_literals.add(axiom)
        for premise in premise_strs:
            all_literals.add(premise)
        for defeasible_rule_head in defeasible_rule_heads:
            all_literals.add(defeasible_rule_head[1])
        for defeasible_rule_body in defeasible_rule_bodies:
            all_literals.add(defeasible_rule_body[1])
        for strict_rule_head in strict_rule_heads:
            all_literals.add(strict_rule_head[1])
        for strict_rule_body in strict_rule_bodies:
            all_literals.add(strict_rule_body[1])
        for contradiction_pair in contradiction_pairs:
            all_literals.add(contradiction_pair[0])
            all_literals.add(contradiction_pair[1])
        language = {lit_str: Literal(lit_str) for lit_str in all_literals}

        contraries_and_contradictories = \
            {lit_str: set() for lit_str in all_literals}
        for contra_from, contra_to in contradiction_pairs:
            contraries_and_contradictories[contra_from].add(
                language[contra_to])

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

        strict_rules = []
        for rule_nr, rule_head in strict_rule_heads:
            rule_antecedents = [
                rule_body_literal
                for rule_body_nr, rule_body_literal in strict_rule_bodies
                if rule_body_nr == rule_nr]
            strict_rule = StrictRule(
                rule_nr, {language[ant_str] for ant_str in rule_antecedents},
                language[rule_head])
            strict_rules.append(strict_rule)

        def_rules_lookup = {defeasible_rule.id: defeasible_rule
                            for defeasible_rule in defeasible_rules}
        rule_preference_preorder = PreferencePreorder(
            [(def_rules_lookup[rule_a], def_rules_lookup[rule_b])
             for rule_b, rule_a in preferred_pairs
             if rule_a in def_rules_lookup])
        rule_preference_preorder.fix_transitivity()

        argumentation_system = ArgumentationSystem(
            language=language,
            contraries_and_contradictories=contraries_and_contradictories,
            strict_rules=strict_rules, defeasible_rules=defeasible_rules,
            defeasible_rule_preferences=rule_preference_preorder,
            add_defeasible_rule_literals=True)

        knowledge_base_axioms = [
            language[axiom_str] for axiom_str in axiom_strs]
        knowledge_base_ordinary_premises = [
            language[premise_str] for premise_str in premise_strs]
        premise_preference_preorder = PreferencePreorder(
            [(language[prem_a], language[prem_b])
             for prem_b, prem_a in preferred_pairs
             if prem_a in language])
        premise_preference_preorder.fix_transitivity()

        return ArgumentationTheory(
            argumentation_system=argumentation_system,
            knowledge_base_axioms=knowledge_base_axioms,
            knowledge_base_ordinary_premises=knowledge_base_ordinary_premises,
            ordinary_premise_preferences=premise_preference_preorder
        )
