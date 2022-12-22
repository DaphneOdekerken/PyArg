from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg_visualisation.ordering_functions.get_ordering_by_specification import get_ordering_by_specification


def get_argumentation_theory_graph_data(argumentation_theory: ArgumentationTheory, ordering_specification: str):
    """
    Calculate the data needed for the graphical representation of the argumentation theory and ordering

    :param argumentation_theory: The argumentation_theory that needs to be visualized.
    :param ordering_specification: The chosen ordering, combining both last/weakest link and democratic/elitist.
    """
    argument_str_to_id = {argument.short_name: 'A' + str(argument_id + 1)
                          for argument_id, argument in enumerate(argumentation_theory.all_arguments)}

    data_nodes = [{'id': argument_id, 'label': argument_str, 'color': '#6DCDE3'}
                  for argument_str, argument_id in argument_str_to_id.items()]

    ordering = get_ordering_by_specification(argumentation_theory, ordering_specification)
    data_edges = []
    for defeat in argumentation_theory.recompute_all_defeats(ordering):
        argument_a_id = argument_str_to_id[defeat.from_argument.short_name]
        argument_b_id = argument_str_to_id[defeat.to_argument.short_name]

        data_edges.append({'id': str(argument_a_id) + '-' + str(argument_b_id),
                           'from': argument_a_id, 'to': argument_b_id, 'arrows': 'to'})

    data = {'nodes': data_nodes, 'edges': data_edges}
    return data
