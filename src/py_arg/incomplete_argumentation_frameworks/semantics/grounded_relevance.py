import clingo
import pathlib

from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg.incomplete_argumentation_frameworks.semantics.clingo_utils import \
    add_iaf_and_topic_to_control

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class GroundedRelevanceWithPreprocessingSolver:
    def __init__(self):
        self.last_model = None
        self.id_to_argument_name = None

    def on_model(self, model):
        self.last_model = model.symbols(shown=True)

    def get_relevant_args_and_atts(self):
        relevant_arg = set()
        relevant_att = set()
        for symbols in self.last_model:
            q1 = self.id_to_argument_name[symbols.arguments[1].name]
            if symbols.name in ['add_query_relevant_for',
                                'remove_query_relevant_for']:
                relevant_arg.add(q1)
            else:
                q2 = self.id_to_argument_name[symbols.arguments[2].name]
                relevant_att.add((q1, q2))

        return relevant_arg, relevant_att

    def get_printable_result(self, justification_status):
        result = []
        for symbols in self.last_model:
            if justification_status == symbols.arguments[0].name:
                q1 = self.id_to_argument_name[symbols.arguments[1].name]
                q2 = self.id_to_argument_name[symbols.arguments[2].name]
                if symbols.name == 'add_query_relevant_for':
                    result.append(f'Adding {q1} is '
                                  f'{justification_status.upper()}-'
                                  f'relevant for {q2}.')
                elif symbols.name == 'remove_query_relevant_for':
                    result.append(f'Removing {q1} is '
                                  f'{justification_status.upper()}-'
                                  f'relevant for {q2}.')
                else:
                    q3 = self.id_to_argument_name[symbols.arguments[3].name]
                    if symbols.name == 'add_query_att_relevant_for':
                        result.append(f'Adding ({q1}, {q2}) is '
                                      f'{justification_status.upper()}-'
                                      f'relevant for {q3}.')
                    if symbols.name == 'remove_query_att_relevant_for':
                        result.append(f'Removing ({q1}, {q2}) is '
                                      f'{justification_status.upper()}-'
                                      f'relevant for {q3}.')
        return result

    def enumerate_grounded_relevant_updates(
            self, iaf: IncompleteArgumentationFramework, topic_str: str):
        control = clingo.Control(arguments=['--enum-mode=brave'])
        _, self.id_to_argument_name = \
            add_iaf_and_topic_to_control(iaf, topic_str, control)
        control.load(str(PATH_TO_ENCODINGS / 'filter.lp'))
        control.load(str(PATH_TO_ENCODINGS / 'grounded.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'labels.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'valid_completion.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'grounded_relevant_args.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'query_arg.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'grounded_relevant_atts.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'query_att.dl'))
        control.ground([('base', [])], context=self)
        control.solve(on_model=self.on_model)
