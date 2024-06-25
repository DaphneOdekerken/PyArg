from typing import List, Optional, Tuple

from py_arg.incomplete_argumentation_frameworks.classes. \
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg_visualisation.functions.graph_data_functions.get_color \
    import get_color


def get_iaf_graph_data(
        iaf: IncompleteArgumentationFramework,
        topic_argument: Optional[str],
        blue_arguments: Optional[List[str]],
        blue_attacks: Optional[List[Tuple[str, str]]],
        color_blind_mode: bool):
    """
    Calculate the data needed for the graphical representation of the
    argumentation framework

    :param iaf: The incomplete argumentation framework that needs to be
    visualized.
    :param topic_argument: The topic argument.
    :param blue_arguments: The arguments to be marked in blue.
    :param blue_attacks: The attacks to be marked in blue.
    :param color_blind_mode: Is the color-blind mode on?
    """
    dark_blue = {'background': get_color('dark-blue', color_blind_mode),
                 'border': get_color('black', color_blind_mode)}
    blue = {'background': get_color('blue', color_blind_mode),
            'border': get_color('black', color_blind_mode)}
    gray = {'background': get_color('gray', color_blind_mode),
            'border': get_color('black', color_blind_mode)}
    no_dashes = {'borderDashes': False}
    dashes = {'borderDashes': [2, 2]}

    data_nodes = []
    for argument_name in iaf.arguments.keys():
        if argument_name == topic_argument:
            color = dark_blue
        else:
            color = gray
        new_node = {'id': argument_name, 'label': argument_name,
                    'color': color, 'shapeProperties': no_dashes}
        data_nodes.append(new_node)
    for argument_name in iaf.uncertain_arguments.keys():
        if argument_name in blue_arguments:
            color = blue
        else:
            color = gray
        new_node = {'id': argument_name, 'label': argument_name,
                    'color': color, 'shapeProperties': dashes}
        data_nodes.append(new_node)

    data_edges = []
    for defeat in iaf.defeats:
        edge_color = get_color('black', color_blind_mode)
        new_edge = {
            'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
            'from': str(defeat.from_argument),
            'to': str(defeat.to_argument), 'arrows': 'to',
            'dashes': False, 'color': {'color': edge_color}}
        data_edges.append(new_edge)
    for defeat in iaf.uncertain_defeats:
        if (str(defeat.from_argument), str(defeat.to_argument)) in \
                blue_attacks:
            edge_color = get_color('blue', color_blind_mode)
        else:
            edge_color = get_color('black', color_blind_mode)
        new_edge = {
            'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
            'from': str(defeat.from_argument),
            'to': str(defeat.to_argument), 'arrows': 'to',
            'dashes': [2, 2], 'color': {'color': edge_color}}
        data_edges.append(new_edge)

    data = {'nodes': data_nodes, 'edges': data_edges}
    return data
