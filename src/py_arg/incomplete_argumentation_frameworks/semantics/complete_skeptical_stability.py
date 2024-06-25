import clingo
import pathlib

from py_arg.incomplete_argumentation_frameworks.semantics.clingo_utils import \
    add_iaf_and_topic_to_control

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class CompleteSkepticalStabilitySolver:
    def __init__(self):
        self.argument_name_to_id = None
        self.id_to_argument_name = None
        self.last_model = None

    def check_stability(self, iaf, label: str, topic_str: str) -> bool:
        control = clingo.Control()
        self.argument_name_to_id, self.id_to_argument_name = \
            add_iaf_and_topic_to_control(iaf, topic_str, control)
        control.load(str(PATH_TO_ENCODINGS / 'complete.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'valid_completion.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'labels.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        control.ground([('base', [])], context=self)
        assumption_label = clingo.Function('lab', [
            clingo.Function(label),
            clingo.Function(self.argument_name_to_id[topic_str])])
        control.solve(on_model=self._store_completion,
                      assumptions=[(assumption_label, False)])
        if self.last_model:
            return False
        return True

    def _store_completion(self, model):
        self.last_model = model.symbols(shown=True)
