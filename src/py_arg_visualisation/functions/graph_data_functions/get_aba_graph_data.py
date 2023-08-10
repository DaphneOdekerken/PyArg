from typing import List, Dict

from py_arg.aba_classes.aba_framework import ABAF
from py_arg_visualisation.functions.graph_data_functions.get_color import get_color


def apply(abaf: ABAF, selected_arguments: Dict[str, List[str]],
          color_blind_mode: bool):
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

    argument_long_str_to_id = {}
    data_nodes = []
    for argument_id, argument in enumerate(abaf.generate_af_full().arguments):
        readable_id = 'A' + str(argument_id + 1)
        argument_long_str_to_id[argument.name] = readable_id
        if argument.name in blue:
            color = get_color('blue', color_blind_mode)
        elif argument.name in green:
            color = get_color('green', color_blind_mode)
        elif argument.name in yellow:
            color = get_color('yellow', color_blind_mode)
        elif argument.name in red:
            color = get_color('red', color_blind_mode)
        else:
            color = get_color('gray', color_blind_mode)
        data_nodes.append({'id': readable_id, 'label': argument.name, 'color': color})

    data_edges = []
    for defeat in abaf.generate_af_full().defeats:
        argument_a_id = argument_long_str_to_id[defeat.from_argument.name]
        argument_b_id = argument_long_str_to_id[defeat.to_argument.name]

        data_edges.append({'id': str(argument_a_id) + '-' + str(argument_b_id),
                           'from': argument_a_id, 'to': argument_b_id, 'arrows': 'to'})

    data = {'nodes': data_nodes, 'edges': data_edges}
    return data
