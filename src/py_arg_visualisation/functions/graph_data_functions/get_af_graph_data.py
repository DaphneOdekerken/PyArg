from typing import List, Optional, Dict

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg_visualisation.functions.graph_data_functions.get_color import get_color


def get_argumentation_framework_graph_data(arg_framework: AbstractArgumentationFramework,
                                           selected_arguments: Optional[Dict[str, List[str]]],
                                           color_blind_mode: bool):
    """
    Calculate the data needed for the graphical representation of the argumentation framework

    :param arg_framework: The abstract argumentation framework that needs to be visualized.
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
    other_arguments = [str(argument) for argument in arg_framework.arguments
                       if argument.name not in blue + green + yellow + red]

    data_nodes_blue = [{'id': str(argument), 'label': str(argument),
                        'color': get_color('blue', color_blind_mode)}
                       for argument in arg_framework.arguments
                       if argument.name in blue]
    data_nodes_green = [{'id': str(argument), 'label': str(argument),
                         'color': get_color('green', color_blind_mode)}
                        for argument in arg_framework.arguments
                        if argument.name in green]
    data_nodes_yellow = [{'id': str(argument), 'label': str(argument),
                          'color': get_color('yellow', color_blind_mode)}
                         for argument in arg_framework.arguments
                         if argument.name in yellow]
    data_nodes_red = [{'id': str(argument), 'label': str(argument),
                       'color': get_color('red', color_blind_mode)}
                      for argument in arg_framework.arguments
                      if argument.name in red]
    data_nodes_unselected = [{'id': str(argument), 'label': str(argument),
                              'color': get_color('gray', color_blind_mode)}
                             for argument in arg_framework.arguments
                             if argument.name in other_arguments]
    data_nodes = data_nodes_blue + data_nodes_red + data_nodes_yellow + data_nodes_green + data_nodes_unselected

    data_edges = [{'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
                   'from': str(defeat.from_argument), 'to': str(defeat.to_argument), 'arrows': 'to'}
                  for defeat in arg_framework.defeats]
    data = {'nodes': data_nodes, 'edges': data_edges}
    return data
