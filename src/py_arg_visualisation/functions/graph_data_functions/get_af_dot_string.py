import pathlib

import clingo

from py_arg_visualisation.functions.graph_data_functions.get_color import \
    get_color

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


def generate_plain_dot_string(argumentation_framework, layout=any):
    dot_string = "digraph {\n"
    dot_string += " rankdir={}  // Node defaults can be set here if needed\n".format(layout)

    # Adding node information
    for argument in argumentation_framework.arguments:
        dot_string += f'    "{argument.name}" [fontsize=14]\n'

    # Adding edge information
    dot_string += f'    edge[labeldistance=1.5 fontsize=12]\n'
    for attack in argumentation_framework.defeats:
        dot_string += f'    "{attack.from_argument}" -> ' \
                      f'"{attack.to_argument}"\n'
    dot_string += "}"
    return dot_string


def generate_dot_string(
        argumentation_framework, selected_arguments, color_blind_mode=False, layout=any):
    gr_status_by_arg, number_by_argument = get_numbered_grounded_extension(
        argumentation_framework)
    dot_string = "digraph {\n"
    dot_string +=" rankdir={}  // Node defaults can be set here if needed\n".format(layout)

    # Adding node information
    is_extension_representation = False
    argument_extension_state = {}
    unselected_arguments = \
        {arg.name for arg in argumentation_framework.arguments}
    for color, arguments in selected_arguments.items():
        if color in ['green', 'red', 'yellow']:
            is_extension_representation = True
        if color == 'green':
            status = 'accepted'
        elif color == 'red':
            status = 'defeated'
        elif color == 'yellow':
            status = 'undefined'
        else:
            status = 'other'
        for argument_name in arguments:
            if argument_name != '':
                number = number_by_argument[argument_name]
                argument_extension_state[argument_name] = status
                if gr_status_by_arg[argument_name] == 'undefined' and \
                        status in ['accepted', 'defeated']:
                    argument_color = get_color(
                        f'light-{color}', color_blind_mode)
                else:
                    argument_color = get_color(color, color_blind_mode)
                if is_extension_representation:
                    argument_label = f'{argument_name}.{number}'
                else:
                    argument_label = argument_name
                node = f'    "{argument_name}" [style="filled" ' \
                       f'fillcolor="{argument_color}" ' \
                       f'label="{argument_label}" ' \
                       f'fontsize=14]\n'
                dot_string += node

                unselected_arguments.remove(argument_name)
    for argument_name in unselected_arguments:
        dot_string += f'    "{argument_name}" [fontsize=14]\n'

    # Adding edge information
    dot_string += f'    edge[labeldistance=1.5 fontsize=12]\n'
    for attack in argumentation_framework.defeats:
        if is_extension_representation:
            from_argument_grounded_state = gr_status_by_arg[
                attack.from_argument.name]
            to_argument_grounded_state = gr_status_by_arg[
                attack.to_argument.name]
            from_argument_extension_state = argument_extension_state[
                attack.from_argument.name]
            to_argument_extension_state = argument_extension_state[
                attack.to_argument.name]
            from_argument_number = \
                number_by_argument[attack.from_argument.name]

            constraint = False
            style = 'solid'
            try:
                num = int(from_argument_number)
                label = str( num + 1)
            except ValueError:
                label = from_argument_number
            if from_argument_grounded_state == 'accepted' and \
                    to_argument_grounded_state == 'defeated':
                full_color = get_color('green', color_blind_mode)
            elif from_argument_grounded_state == 'defeated' and \
                    to_argument_grounded_state == 'accepted':
                full_color = get_color('red', color_blind_mode)
            elif from_argument_grounded_state != 'accepted' and \
                    to_argument_grounded_state == 'defeated':
                constraint = True
                full_color = get_color('black', color_blind_mode)
                style = 'dashed'
                label = ''
            else:
                grounded_edge_color = get_color('yellow', color_blind_mode)
                if from_argument_extension_state == 'accepted' and \
                        to_argument_extension_state == 'defeated':
                    extension_edge_color = get_color('green', color_blind_mode)
                    full_color = \
                        f'{extension_edge_color}:{grounded_edge_color}'
                elif from_argument_extension_state == 'defeated' and \
                        to_argument_extension_state == 'accepted':
                    extension_edge_color = get_color('red', color_blind_mode)
                    full_color = \
                        f'{extension_edge_color}:{grounded_edge_color}'
                elif from_argument_extension_state == 'undefined' and \
                        to_argument_extension_state == 'undefined':
                    full_color = get_color('dark-yellow', color_blind_mode)
                else:
                    extension_edge_color = get_color('black', color_blind_mode)
                    full_color = \
                        f'{extension_edge_color}:{grounded_edge_color}'
                    style = 'dashed'
                    label = ''

            if constraint:
                constraint_str = "constraint=false"
            else:
                constraint_str = ''

            edge = f'"{attack.from_argument.name}" -> ' \
                   f'"{attack.to_argument.name}" ' \
                   f'[color="{full_color}" ' \
                   f'style="{style}" ' \
                   f'taillabel="{label}" {constraint_str}]\n'
        else:
            edge = f'"{attack.from_argument.name}" -> ' \
                   f'"{attack.to_argument.name}"\n'
        dot_string += "    "+edge

    dot_string += "}"
    return dot_string


def get_numbered_grounded_extension(argumentation_framework):
    # Keep argument ID dictionary.
    argument_name_to_id = {}
    id_to_argument_name = {}
    for arg_id, argument in enumerate(argumentation_framework.arguments):
        argument_name_to_id[argument.name] = 'a' + str(arg_id)
        id_to_argument_name['a' + str(arg_id)] = argument.name

    # Run clingo solver.
    ctl = clingo.Control()
    ctl.load(str(PATH_TO_ENCODINGS / 'grounded_encoding.dl'))
    for argument in argumentation_framework.arguments:
        ctl.add('base', [], f'pos({argument_name_to_id[argument.name]}).')
    for defeat in argumentation_framework.defeats:
        ctl.add('base', [],
                f'attack({argument_name_to_id[defeat.from_argument.name]}, '
                f'{argument_name_to_id[defeat.to_argument.name]}).')
    ctl.ground([("base", [])])
    models = []
    ctl.solve(on_model=lambda m: models.append(m.symbols(shown=True)))

    # Read output of clingo solver.
    atoms = models[0]
    number_by_argument = {}
    status_by_argument = {}
    for atom in atoms:
        if atom.name == 'len':
            argument_name = id_to_argument_name[atom.arguments[1].name]
            if atom.arguments[0].name == 'undefined':
                number_by_argument[argument_name] = '∞'
            else:
                number_by_argument[argument_name] = str(atom.arguments[2])
            status_by_argument[argument_name] = atom.arguments[0].name
    return status_by_argument, number_by_argument
