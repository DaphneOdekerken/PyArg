from typing import List

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework


def get_argumentation_framework_graph_data(arg_framework: AbstractArgumentationFramework,
                                           selected_arguments: List[str]):
    """
    Calculate the data needed for the graphical representation of the argumentation framework

    :param arg_framework: The abstract argumentation framework that needs to be visualized.
    :param selected_arguments: Arguments to be marked with a different color (e.g. because they are in some extension)
    """
    if not selected_arguments:
        selected_arguments = []

    data_nodes_selected = [{'id': str(argument), 'label': str(argument), 'color': '#6DCDE3'}
                           for argument in arg_framework.arguments
                           if argument.name in selected_arguments]
    data_nodes_unselected = [{'id': str(argument), 'label': str(argument), 'color': '#AAAAAA'}
                             for argument in arg_framework.arguments
                             if argument.name not in selected_arguments]
    data_nodes = data_nodes_selected + data_nodes_unselected

    data_edges = [{'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
                   'from': str(defeat.from_argument), 'to': str(defeat.to_argument), 'arrows': 'to'}
                  for defeat in arg_framework.defeats]
    data = {'nodes': data_nodes, 'edges': data_edges}
    return data
