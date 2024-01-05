from typing import Set

from py_arg.aspic.algorithms.justification.connected_literal import \
    ConnectedLiteral
from py_arg.incomplete_aspic.algorithms.stability.stability_labels import \
    StabilityLabels
from py_arg.incomplete_aspic.classes.incomplete_argumentation_theory import \
    IncompleteArgumentationTheory


def get_incomplete_aspic_graph_data(
        incomplete_argumentation_theory: IncompleteArgumentationTheory,
        stability_labeler_labels: StabilityLabels,
        topic_literal: ConnectedLiteral, questions: Set[ConnectedLiteral]):
    literal_layers = \
        {literal_str: 1 for literal_str in
         incomplete_argumentation_theory.argumentation_system.language}
    rule_layers = \
        {rule.id: 1 for rule in
         incomplete_argumentation_theory.argumentation_system.rules}

    change = True
    todo_rules = topic_literal.children
    literal_layers[topic_literal.s1] = 0
    for contrary_literal in topic_literal.contraries_and_contradictories:
        literal_layers[contrary_literal.s1] = 0
        todo_rules += contrary_literal.children

    next_layer = -1
    while change:
        change = False

        todo_literals = []
        for rule in todo_rules:
            if rule_layers[rule.id] > 0:
                rule_layers[rule.id] = next_layer
                change = True
                for antecedent in rule.antecedents:
                    todo_literals.append(antecedent)

        next_layer -= 1

        todo_rules = []
        for literal in todo_literals:
            if literal_layers[literal.s1] > 0:
                literal_layers[literal.s1] = next_layer
                for rule in literal.children:
                    todo_rules.append(rule)
                for contra in literal.contraries_and_contradictories:
                    if literal_layers[contra.s1] > 0:
                        literal_layers[contra.s1] = next_layer
                        for rule in contra.children:
                            todo_rules.append(rule)
        next_layer -= 1

    data_nodes = []
    data_edges = []
    iat = incomplete_argumentation_theory
    for literal in iat.argumentation_system.language.values():
        if literal_layers[literal.s1] <= 0:
            if literal in questions:
                data_nodes.append({'id': literal.s1, 'label': literal.s1,
                                   'level': literal_layers[literal.s1],
                                   'shape': 'box',
                                   'color': 'blue'})
            elif stability_labeler_labels.literal_labeling[
                    literal].is_stable_defended:
                data_nodes.append({'id': literal.s1, 'label': literal.s1,
                                   'level': literal_layers[literal.s1],
                                   'shape': 'box',
                                   'color': 'green'})
            else:
                data_nodes.append({'id': literal.s1, 'label': literal.s1,
                                   'level': literal_layers[literal.s1],
                                   'shape': 'box',
                                   'color': '#c0c0c0'})

    contra_counter = 0
    for literal in iat.argumentation_system.language.values():
        if literal_layers[literal.s1] <= 0:
            for contrary in literal.contraries_and_contradictories:
                if literal <= contrary:
                    contra_id = 'C' + str(contra_counter)
                    data_edges.append({'id': contra_id, 'arrows': '',
                                       'from': literal.s1, 'to': contrary.s1,
                                       'color': {'color': 'red'},
                                       'smooth': {
                                           'enabled': True,
                                           'type': 'curvedCCW'}})
                    contra_counter += 1

    # Create nodes for defeasible rules
    for def_rule in iat.argumentation_system.defeasible_rules:
        if rule_layers[def_rule.id] < 0:
            data_nodes.append({'id': def_rule.id, 'label': '⇒',
                               'shape': 'ellipse',
                               'level': rule_layers[def_rule.id]})
            for antecedent in def_rule.antecedents:
                data_edges.append(
                    {'id': antecedent.s1 + '-' + str(def_rule.id),
                     'from': antecedent.s1, 'to': def_rule.id,
                     'arrows': 'to'})
            data_edges.append(
                {'id': str(def_rule.id) + '-' + def_rule.consequent.s1,
                 'from': def_rule.id, 'to': def_rule.consequent.s1,
                 'arrows': 'to'})

    # Create nodes for strict rules
    for strict_rule in iat.argumentation_system.strict_rules:
        if rule_layers[strict_rule.id] < 0:
            data_nodes.append({'id': strict_rule.id, 'label': '→',
                               'shape': 'ellipse',
                               'level': rule_layers[strict_rule.id]})
            for antecedent in strict_rule.antecedents:
                data_edges.append(
                    {'id': antecedent.s1 + '-' + str(strict_rule.id),
                     'from': antecedent.s1, 'to': strict_rule.id,
                     'arrows': 'to'})
            data_edges.append(
                {'id': str(strict_rule.id) + '-' + strict_rule.consequent.s1,
                 'from': strict_rule.id, 'to': strict_rule.consequent.s1,
                 'arrows': 'to'})

    data = {'nodes': data_nodes, 'edges': data_edges}
    return data

