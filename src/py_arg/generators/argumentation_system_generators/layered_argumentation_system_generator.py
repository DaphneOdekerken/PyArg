import itertools
import random
from typing import Dict, List, Tuple, Set

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.preference_preorder import PreferencePreorder
from py_arg.aspic_classes.strict_rule import StrictRule


class LayeredArgumentationSystemGenerator:
    def __init__(self, nr_of_literals: int, nr_of_rules: int,
                 rule_antecedent_distribution: Dict[int, int],
                 literal_layer_distribution: Dict[int, int],
                 strict_rule_ratio: float):
        """
        Construct a generator for making random Argumentation Systems with a layered structure

        :param nr_of_literals: The desired number of literals.
        :param nr_of_rules: The desired number of rules.
        :param rule_antecedent_distribution: Number of rules (value) with specific number of antecedents (key)
        :param literal_layer_distribution: Number of literals (value) in a specific layer (key)
        :param strict_rule_ratio: Ratio of strict rules given all rules.
        """
        if nr_of_literals % 2 != 0:
            raise ValueError('Language size should be even, since each literal should have a negated version.')
        self.nr_of_literals = nr_of_literals

        required_rules = sum([value for key, value in literal_layer_distribution.items() if key != 0])
        if nr_of_rules < required_rules:
            raise ValueError('You need more rules to enable this literal layer distribution.')
        self.nr_of_rules = nr_of_rules

        possible_layers = sorted(literal_layer_distribution.keys())
        if 0 not in possible_layers:
            raise ValueError('There should at least be a literal of layer 0.')
        if any([x + 1 != y for x, y in zip(possible_layers[:-1], possible_layers[1:])]):
            raise ValueError('Each layer between the minimum and maximum should have a value.')
        if sum(literal_layer_distribution.values()) != nr_of_literals:
            raise ValueError('The sum of the literal layer distribution should equal the language size.')
        self.literal_layer_distribution = literal_layer_distribution

        if sum(rule_antecedent_distribution.values()) != nr_of_rules:
            raise ValueError('The sum of the rule antecedent distribution should equal the rule size.')
        self.rule_antecedent_distribution = rule_antecedent_distribution

        if any([nr_antecedents > nr_of_literals / 2 for nr_antecedents in self.rule_antecedent_distribution.keys()]):
            raise ValueError('Rules cannot have more antecedents than half of the language size.')

        if strict_rule_ratio < 0 or strict_rule_ratio > 1:
            raise ValueError('Strict rule ratio should be between zero and one.')
        self.strict_rule_ratio = strict_rule_ratio

    def generate(self, return_layered_language: bool = False, add_rule_preferences=True):
        max_remaining_tries = 25
        while max_remaining_tries > 0:
            try:
                max_remaining_tries -= 1
                layered_language, contraries = self._generate_language_and_contradictories_initial()
                strict_rules, defeasible_rules, def_rule_preferences = self._generate_rules(layered_language,
                                                                                            add_rule_preferences,
                                                                                            contraries)
                language = {str(literal): literal for literals in layered_language.values() for literal in literals}

                argumentation_system = ArgumentationSystem(language, contraries, strict_rules, defeasible_rules,
                                                           add_defeasible_rule_literals=False,
                                                           defeasible_rule_preferences=def_rule_preferences)
                if return_layered_language:
                    return argumentation_system, layered_language
                return argumentation_system
            except ValueError:
                pass
        raise ValueError('Could not generate an ArgumentationSystem with these properties.')

    def _generate_language_and_contradictories_initial(self) -> \
            Tuple[Dict[int, List[Literal]], Dict[str, Set[Literal]]]:
        positive_language_size = int(self.nr_of_literals / 2)
        layers = self.literal_layer_distribution.copy()

        layered_language = {layer_nr: [] for layer_nr in layers.keys()}
        contradictories = dict()

        for pos_literal_index in range(positive_language_size):
            literal_str_positive = 'l' + str(pos_literal_index)
            literal_str_negative = '-l' + str(pos_literal_index)

            # Get layer and update layers for future random layer choices
            new_literal_positive_layer = random.choices(list(layers.keys()), list(layers.values()), k=1)[0]
            layers[new_literal_positive_layer] -= 1
            new_literal_negative_layer = random.choices(list(layers.keys()), list(layers.values()), k=1)[0]
            layers[new_literal_negative_layer] -= 1

            # Generate a Literal: positive version
            new_literal_positive = Literal(literal_str_positive)
            # Generate a Literal: negative version
            new_literal_negative = Literal(literal_str_negative)

            # Connect negations / contradictories
            contradictories[literal_str_positive] = {new_literal_negative}
            contradictories[literal_str_negative] = {new_literal_positive}

            # Add to layered language dict
            layered_language[new_literal_positive_layer].append(new_literal_positive)
            layered_language[new_literal_negative_layer].append(new_literal_negative)

        return layered_language, contradictories

    def _generate_rules(self, layered_language: Dict[int, List[Literal]], add_rule_preferences: bool,
                        contradictories: Dict[str, Set[Literal]]) -> \
            Tuple[List[StrictRule], List[DefeasibleRule], PreferencePreorder]:
        # Keep track of remaining antecedent options
        r_a_d = self.rule_antecedent_distribution.copy()

        strict_rules = []
        defeasible_rules = []

        # Start with the necessary rules
        necessary_consequents = [(literal, layer) for layer, literals in layered_language.items()
                                 for literal in literals
                                 if layer > 0]
        for consequent, consequent_layer in necessary_consequents:
            antecedents = []

            if not layered_language[consequent_layer - 1]:
                raise ValueError('Could not add a rule with the required number of literals')
            highest_antecedent = random.choice(layered_language[consequent_layer - 1])
            antecedents.append(highest_antecedent)

            nr_of_antecedents = random.choices(list(r_a_d.keys()), list(r_a_d.values()), k=1)[0]
            r_a_d[nr_of_antecedents] -= 1

            while len(antecedents) < nr_of_antecedents:
                antecedent_candidates = []
                for other_layer, other_literals in layered_language.items():
                    if other_layer < consequent_layer:
                        for other_literal in other_literals:
                            if other_literal not in antecedents and other_literal != consequent and \
                                    all([contrary not in antecedents and contrary != consequent
                                         for contrary in contradictories[str(other_literal)]]):
                                antecedent_candidates.append(other_literal)

                if not antecedent_candidates:
                    raise ValueError('Could not add a rule with the required number of literals')

                new_antecedent = random.choice(antecedent_candidates)
                antecedents.append(new_antecedent)

            # Decide if this rule will be strict or defeasible
            rule_will_be_strict = random.choices([True, False],
                                                 weights=[self.strict_rule_ratio, 1 - self.strict_rule_ratio])[0]
            if rule_will_be_strict:
                new_rule = StrictRule('r' + str(len(strict_rules)), set(antecedents), consequent)
                strict_rules.append(new_rule)
            else:
                new_rule = DefeasibleRule('d' + str(len(defeasible_rules)), set(antecedents), consequent)
                defeasible_rules.append(new_rule)

        # Add additional rules
        while len(strict_rules) + len(defeasible_rules) < self.nr_of_rules:
            if not necessary_consequents:
                raise ValueError('It is not possible to generate the required number of rules.')
            consequent, consequent_layer = random.choice(necessary_consequents)

            # Find antecedents
            nr_of_antecedents = random.choices(list(r_a_d.keys()), list(r_a_d.values()), k=1)[0]
            r_a_d[nr_of_antecedents] -= 1

            antecedents = []
            while len(antecedents) < nr_of_antecedents:
                antecedent_candidates = []
                for other_layer, other_literals in layered_language.items():
                    if other_layer < consequent_layer:
                        for other_literal in other_literals:
                            if other_literal not in antecedents and other_literal != consequent and \
                                    all([contrary not in antecedents and contrary != consequent
                                         for contrary in contradictories[str(other_literal)]]):
                                antecedent_candidates.append(other_literal)

                if not antecedent_candidates:
                    raise ValueError('Could not add a rule with the required number of literals')

                new_antecedent = random.choice(antecedent_candidates)
                antecedents.append(new_antecedent)

            # Decide if this rule will be strict or defeasible
            rule_will_be_strict = random.choices([True, False],
                                                 weights=[self.strict_rule_ratio, 1 - self.strict_rule_ratio])[0]
            if rule_will_be_strict:
                new_rule = StrictRule('r' + str(len(strict_rules)), set(antecedents), consequent)
                strict_rules.append(new_rule)
            else:
                new_rule = DefeasibleRule('d' + str(len(defeasible_rules)), set(antecedents), consequent)
                defeasible_rules.append(new_rule)

        if add_rule_preferences:
            rule_preferences = PreferencePreorder()
            shuffled_defeasible_rules = defeasible_rules.copy()
            random.shuffle(shuffled_defeasible_rules)
            contradicting_rules = {(rule_a, rule_b)
                                   for rule_a, rule_b in itertools.combinations(shuffled_defeasible_rules, 2)
                                   if rule_a.consequent in contradictories[str(rule_b.consequent)]}
            leq_rules = random.sample(list(contradicting_rules), int(len(contradicting_rules) / 2))
            for geq_tuple in leq_rules:
                rule_preferences.append(geq_tuple)
        else:
            rule_preferences = PreferencePreorder.create_reflexive_preorder([])

        return strict_rules, defeasible_rules, rule_preferences
