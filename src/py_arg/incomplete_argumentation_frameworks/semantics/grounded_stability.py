import clingo
import pathlib

from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg.incomplete_argumentation_frameworks.semantics.clingo_utils import \
    add_iaf_and_topic_to_control

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class GroundedStabilitySolver:
    def __init__(self):
        self.last_model = None
        self.id_to_argument_name = None

    def on_model(self, model):
        self.last_model = model.symbols(shown=True)

    def enumerate_stable_arguments(
            self, iaf: IncompleteArgumentationFramework, topic_str: str):
        control = clingo.Control(arguments=['--enum-mode=cautious'])
        _, self.id_to_argument_name = \
            add_iaf_and_topic_to_control(iaf, topic_str, control)
        control.load(str(PATH_TO_ENCODINGS / 'stability_filter.lp'))
        control.load(str(PATH_TO_ENCODINGS / 'grounded.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'labels.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'valid_completion.dl'))
        control.ground([('base', [])], context=self)
        control.solve(on_model=self.on_model)

    def get_result(self):
        for symbols in self.last_model:
            topic_argument = \
                self.id_to_argument_name[symbols.arguments[0].name]
            if symbols.name == 'is_in':
                return f'{topic_argument} is Stable-IN.'
            if symbols.name == 'is_out':
                return f'{topic_argument} is Stable-OUT.'
            if symbols.name == 'is_undec':
                return f'{topic_argument} is Stable-UNDEC.'
