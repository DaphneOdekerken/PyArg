from typing import List, Dict

from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory


def get_argumentation_theory_aspic_graph_data(
        argumentation_theory: ArgumentationTheory,
        selected_arguments: Dict[str, List[str]],
        color_blind_mode: bool, show_contradictories: bool):
    """
    Calculate the data needed for the graphical representation of the
    argumentation theory and ordering

    :param argumentation_theory: The argumentation_theory that needs to be
    visualized.
    :param selected_arguments: Arguments to be marked with a different
    color (e.g. because they are in some extension)
    :param color_blind_mode: Is the color-blind mode on?
    :param show_contradictories: Do we display the contradictories?
    """
    data_nodes = []
    data_edges = []

    literal_layers = {literal_str: -1 for literal_str in
                      argumentation_theory.argumentation_system.language}
    rule_layers = {rule.id: -1 for rule in
                   argumentation_theory.argumentation_system.rules}
    for knowledge in argumentation_theory.knowledge_base:
        literal_layers[knowledge.s1] = 0
        if show_contradictories:
            for contra in knowledge.contraries_and_contradictories:
                literal_layers[contra.s1] = 0

    change = True
    iteration = 0
    max_iterations = len(argumentation_theory.argumentation_system.rules)
    while change and iteration < max_iterations:
        change = False
        iteration += 1
        for rule in argumentation_theory.argumentation_system.rules:
            if all(literal_layers[ant.s1] >= 0 for ant in rule.antecedents):
                max_literal_layer = \
                    max(literal_layers[ant.s1] for ant in rule.antecedents)
                rule_layers[rule.id] = max_literal_layer + 1
                if literal_layers[rule.consequent.s1] < 0:
                    literal_layers[rule.consequent.s1] = max_literal_layer + 2
                    for contra in \
                            rule.consequent.contraries_and_contradictories:
                        if literal_layers[contra.s1] < 0:
                            literal_layers[contra.s1] = max_literal_layer + 2
                change = True

    used_literals = set()
    for knowledge in argumentation_theory.knowledge_base:
        used_literals.add(knowledge)
        if show_contradictories:
            for contra in knowledge.contraries_and_contradictories:
                used_literals.add(contra)
    for rule in argumentation_theory.argumentation_system.rules:
        for antecedent in rule.antecedents:
            used_literals.add(antecedent)
            if show_contradictories:
                for contra in antecedent.contraries_and_contradictories:
                    used_literals.add(contra)
        used_literals.add(rule.consequent)
        if show_contradictories:
            for contra in rule.consequent.contraries_and_contradictories:
                used_literals.add(contra)

    # Contradictories
    if show_contradictories:
        contra_counter = 0
        for literal in used_literals:
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

    # Create nodes for used literals
    for literal in used_literals:
        if literal in argumentation_theory.knowledge_base_axioms:
            data_nodes.append({'id': literal.s1, 'label': literal.s1,
                               'level': literal_layers[literal.s1],
                               'shape': 'database',
                               'font': {'color': 'white'},
                               'color': '#000000'})
        elif literal in argumentation_theory.knowledge_base_ordinary_premises:
            data_nodes.append({'id': literal.s1, 'label': literal.s1,
                               'level': literal_layers[literal.s1],
                               'shape': 'database',
                               'color': '#808080'})
        else:
            if literal_layers[literal.s1] >= 0:
                data_nodes.append({'id': literal.s1, 'label': literal.s1,
                                   'level': literal_layers[literal.s1],
                                   'shape': 'box',
                                   'color': '#c0c0c0'})

    # Create nodes for defeasible rules
    for def_rule in argumentation_theory.argumentation_system.defeasible_rules:
        if rule_layers[def_rule.id] >= 0:
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
    for strict_rule in argumentation_theory.argumentation_system.strict_rules:
        if rule_layers[strict_rule.id] >= 0:
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
