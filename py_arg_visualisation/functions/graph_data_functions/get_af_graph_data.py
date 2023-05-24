from typing import List, Optional

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework


def get_argumentation_framework_graph_data(arg_framework: AbstractArgumentationFramework,
                                           blue_arguments: Optional[List[str]],
                                           green_arguments: Optional[List[str]],
                                           yellow_arguments: Optional[List[str]],
                                           red_arguments: Optional[List[str]]
                                           ):
    """
    Calculate the data needed for the graphical representation of the argumentation framework

    :param arg_framework: The abstract argumentation framework that needs to be visualized.
    :param blue_arguments: Arguments to be marked in blue
    :param green_arguments: Arguments to be marked in green
    :param yellow_arguments: Arguments to be marked in yellow
    :param red_arguments: Arguments to be marked in red
    """
    if not blue_arguments:
        blue_arguments = []
    if not green_arguments:
        green_arguments = []
    if not yellow_arguments:
        yellow_arguments = []
    if not red_arguments:
        red_arguments = []
    other_arguments = [str(argument) for argument in arg_framework.arguments
                       if argument.name not in blue_arguments + green_arguments + yellow_arguments + red_arguments]

    data_nodes_blue = [{'id': str(argument), 'label': str(argument), 'color': '#6dcde3'}
                           for argument in arg_framework.arguments
                           if argument.name in blue_arguments]
    data_nodes_green = [{'id': str(argument), 'label': str(argument), 'color': '#2ac2ab'}
                       for argument in arg_framework.arguments
                       if argument.name in green_arguments]
    data_nodes_yellow = [{'id': str(argument), 'label': str(argument), 'color': '#fff2cc'}
                       for argument in arg_framework.arguments
                       if argument.name in yellow_arguments]
    data_nodes_red = [{'id': str(argument), 'label': str(argument), 'color': '#e60c3f'}
                       for argument in arg_framework.arguments
                       if argument.name in red_arguments]
    data_nodes_unselected = [{'id': str(argument), 'label': str(argument), 'color': '#AAAAAA'}
                             for argument in arg_framework.arguments
                             if argument.name in other_arguments]
    data_nodes = data_nodes_blue + data_nodes_red + data_nodes_yellow + data_nodes_green + data_nodes_unselected

    data_edges = [{'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
                   'from': str(defeat.from_argument), 'to': str(defeat.to_argument), 'arrows': 'to'}
                  for defeat in arg_framework.defeats]
    data = {'nodes': data_nodes, 'edges': data_edges}
    return data
