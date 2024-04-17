from typing import List, Optional, Dict

from py_arg.incomplete_argumentation_frameworks.classes. \
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg_visualisation.functions.graph_data_functions.get_color \
    import get_color


def get_iaf_graph_data(
        iaf: IncompleteArgumentationFramework,
        selected_arguments: Optional[Dict[str, List[str]]],
        color_blind_mode: bool):
    """
    Calculate the data needed for the graphical representation of the
    argumentation framework

    :param iaf: The incomplete argumentation framework that needs to be
    visualized.
    :param selected_arguments: The arguments to be marked in a specific color.
    :param color_blind_mode: Is the color-blind mode on?
    """
    if selected_arguments and 'blue' in selected_arguments:
        blue = selected_arguments['blue']
    else:
        blue = []
    if selected_arguments and 'green' in selected_arguments:
        green = selected_arguments['green']
    else:
        green = []
    if selected_arguments and 'yellow' in selected_arguments:
        yellow = selected_arguments['yellow']
    else:
        yellow = []
    if selected_arguments and 'red' in selected_arguments:
        red = selected_arguments['red']
    else:
        red = []
    all_arguments = list(iaf.arguments.values()) + \
                    list(iaf.uncertain_arguments.values())
    other_arguments = [str(argument) for argument in all_arguments
                       if argument.name not in blue + green + yellow + red]

    def get_custom_color(custom_color):
        return {'background': get_color(custom_color, color_blind_mode),
                'border': get_color('black', color_blind_mode)}

    data_nodes_blue = [{'id': str(argument), 'label': str(argument),
                        'color': get_custom_color('blue'),
                        'shapeProperties': {'borderDashes': False}}
                       for argument in iaf.arguments.values()
                       if argument.name in blue]
    data_nodes_green = [{'id': str(argument), 'label': str(argument),
                         'color': get_custom_color('green'),
                         'shapeProperties': {'borderDashes': False}}
                        for argument in iaf.arguments.values()
                        if argument.name in green]
    data_nodes_yellow = [{'id': str(argument), 'label': str(argument),
                          'color': get_custom_color('yellow'),
                          'shapeProperties': {'borderDashes': False}}
                         for argument in iaf.arguments.values()
                         if argument.name in yellow]
    data_nodes_red = [{'id': str(argument), 'label': str(argument),
                       'color': get_custom_color('red'),
                       'shapeProperties': {'borderDashes': False}}
                      for argument in iaf.arguments.values()
                      if argument.name in red]
    data_nodes_unselected = [{'id': str(argument), 'label': str(argument),
                              'color': get_custom_color('gray'),
                              'shapeProperties': {'borderDashes': False}}
                             for argument in iaf.arguments.values()
                             if argument.name in other_arguments]
    data_nodes = data_nodes_blue + data_nodes_red + data_nodes_yellow + \
                 data_nodes_green + data_nodes_unselected

    uncertain_data_nodes_blue = [{'id': str(argument), 'label': str(argument),
                                  'color': get_custom_color('blue'),
                                  'shapeProperties': {'borderDashes': [2, 2]}}
                                 for argument in
                                 iaf.uncertain_arguments.values()
                                 if argument.name in blue]
    uncertain_data_nodes_green = [{'id': str(argument), 'label': str(argument),
                                   'color': get_custom_color('green'),
                                   'shapeProperties': {'borderDashes': [2, 2]}}
                                  for argument in
                                  iaf.uncertain_arguments.values()
                                  if argument.name in green]
    uncertain_data_nodes_yellow = [
        {'id': str(argument), 'label': str(argument),
         'color': get_custom_color('yellow'),
         'shapeProperties': {'borderDashes': [2, 2]}}
        for argument in iaf.uncertain_arguments.values()
        if argument.name in yellow]
    uncertain_data_nodes_red = [{'id': str(argument), 'label': str(argument),
                                 'color': get_custom_color('red'),
                                 'shapeProperties': {'borderDashes': [2, 2]}}
                                for argument in
                                iaf.uncertain_arguments.values()
                                if argument.name in red]
    uncertain_data_nodes_unselected = [
        {'id': str(argument), 'label': str(argument),
         'color': get_custom_color('gray'),
         'shapeProperties': {'borderDashes': [2, 2]}}
        for argument in iaf.uncertain_arguments.values()
        if argument.name in other_arguments]
    uncertain_data_nodes = \
        uncertain_data_nodes_blue + uncertain_data_nodes_red + \
        uncertain_data_nodes_yellow + uncertain_data_nodes_green + \
        uncertain_data_nodes_unselected

    all_nodes = data_nodes + uncertain_data_nodes

    data_edges = [{
        'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
        'from': str(defeat.from_argument),
        'to': str(defeat.to_argument), 'arrows': 'to'}
        for defeat in iaf.defeats]
    uncertain_data_edges = [{
        'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
        'from': str(defeat.from_argument),
        'to': str(defeat.to_argument), 'arrows': 'to',
        'dashes': [2, 2]
    }
        for defeat in iaf.uncertain_defeats]
    all_edges = data_edges + uncertain_data_edges
    data = {'nodes': all_nodes, 'edges': all_edges}
    return data
