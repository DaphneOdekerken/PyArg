import clingo

from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework


def add_iaf_and_topic_to_control(
        iaf: IncompleteArgumentationFramework,
        topic: str,
        clingo_control: clingo.Control):
    argument_name_to_id = {}
    id_to_argument_name = {}
    all_arguments = \
        list(iaf.arguments.values()) + list(iaf.uncertain_arguments.values())
    for arg_id, argument in enumerate(all_arguments):
        argument_name_to_id[argument.name] = 'a' + str(arg_id)
        id_to_argument_name['a' + str(arg_id)] = argument.name

    for argument in iaf.arguments.values():
        clingo_control.add('base', [],
                           f'argument({argument_name_to_id[argument.name]}).')
    for uarg in iaf.uncertain_arguments.values():
        clingo_control.add('base', [],
                           f'uarg({argument_name_to_id[uarg.name]}).')
    for att in iaf.defeats:
        clingo_control.add('base', [],
                           f'att('
                           f'{argument_name_to_id[att.from_argument.name]},'
                           f'{argument_name_to_id[att.to_argument.name]}).')
    for uatt in iaf.uncertain_defeats:
        clingo_control.add('base', [],
                           f'uatt('
                           f'{argument_name_to_id[uatt.from_argument.name]},'
                           f'{argument_name_to_id[uatt.to_argument.name]}).')
    clingo_control.add('base', [], f'topic({argument_name_to_id[topic]}).')

    return argument_name_to_id, id_to_argument_name
