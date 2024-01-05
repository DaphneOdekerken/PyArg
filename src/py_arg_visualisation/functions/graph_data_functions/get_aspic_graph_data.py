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
    :param ordering_specification: The chosen ordering, combining both
    last/weakest link and democratic/elitist.
    :param selected_arguments: Arguments to be marked with a different
    color (e.g. because they are in some extension)
    :param color_blind_mode: Is the color-blind mode on?
    :param show_contradictories: Do we display the contradictories?
    """
    data_nodes = []
    data_edges = []

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
                               'level': 0, 'shape': 'database',
                               'font': {'color': 'white'},
                               'color': '#000000'})
        elif literal in argumentation_theory.knowledge_base_ordinary_premises:
            data_nodes.append({'id': literal.s1, 'label': literal.s1,
                               'level': 0, 'shape': 'database',
                               'color': '#808080'})
        else:
            if any(contra in argumentation_theory.knowledge_base
                   for contra in literal.contraries_and_contradictories):
                level = 0
            else:
                level = 2
            data_nodes.append({'id': literal.s1, 'label': literal.s1,
                               'level': level, 'shape': 'box',
                               'color': '#c0c0c0'})

    # Create nodes for defeasible rules
    for def_rule in argumentation_theory.argumentation_system.defeasible_rules:
        data_nodes.append({'id': def_rule.id, 'label': '⇒',
                           'shape': 'ellipse',
                           'level': 1})
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
        data_nodes.append({'id': strict_rule.id, 'label': '→',
                           'shape': 'ellipse',
                           'level': 1})
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
