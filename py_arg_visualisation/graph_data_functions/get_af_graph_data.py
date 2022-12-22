from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework


def get_argumentation_framework_graph_data(arg_framework: AbstractArgumentationFramework):
    """
    Calculate the data needed for the graphical representation of the argumentation framework

    :param arg_framework: The abstract argumentation framework that needs to be visualized.
    """
    data_nodes = [{'id': str(argument), 'label': str(argument), 'color': '#6DCDE3'}
                  for argument in arg_framework.arguments]
    data_edges = [{'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
                   'from': str(defeat.from_argument), 'to': str(defeat.to_argument), 'arrows': 'to'}
                  for defeat in arg_framework.defeats]
    data = {'nodes': data_nodes, 'edges': data_edges}
    return data
