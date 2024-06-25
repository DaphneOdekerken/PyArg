import clingo
import pathlib

from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg.incomplete_argumentation_frameworks.semantics.clingo_utils import \
    add_iaf_and_topic_to_control

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class ReachabilityPreprocessor:
    def __init__(self):
        self.last_model = None

    def on_model(self, model):
        self.last_model = model.symbols(shown=True)

    def enumerate_reachable(self, iaf, topic_str):
        control = clingo.Control()
        argument_name_to_id, id_to_argument_name = \
            add_iaf_and_topic_to_control(iaf, topic_str, control)
        control.load(str(PATH_TO_ENCODINGS / 'reachable_preprocessing.dl'))
        control.ground([('base', [])], context=self)
        control.solve(on_model=self.on_model)

        all_arguments = {}
        arguments = []
        uncertain_arguments = []
        attacks = []
        uncertain_attacks = []
        if self.last_model:
            for symbols in self.last_model:
                if symbols.name == 'r_argument':
                    arg_name = id_to_argument_name[symbols.arguments[0].name]
                    new_argument = Argument(arg_name)
                    all_arguments[arg_name] = new_argument
                    arguments.append(new_argument)
                elif symbols.name == 'r_uarg':
                    arg_name = id_to_argument_name[
                        symbols.arguments[0].name]
                    new_argument = Argument(arg_name)
                    all_arguments[arg_name] = new_argument
                    uncertain_arguments.append(new_argument)
            for symbols in self.last_model:
                if symbols.name == 'r_att':
                    from_arg_name = id_to_argument_name[
                        symbols.arguments[0].name]
                    to_arg_name = id_to_argument_name[
                        symbols.arguments[1].name]
                    new_defeat = Defeat(all_arguments[from_arg_name],
                                        all_arguments[to_arg_name])
                    attacks.append(new_defeat)
                elif symbols.name == 'r_uatt':
                    from_arg_name = id_to_argument_name[
                        symbols.arguments[0].name]
                    to_arg_name = id_to_argument_name[
                        symbols.arguments[1].name]
                    new_defeat = Defeat(all_arguments[from_arg_name],
                                        all_arguments[to_arg_name])
                    uncertain_attacks.append(new_defeat)
        new_iaf = IncompleteArgumentationFramework(
            iaf.name, arguments, uncertain_arguments,
            attacks, uncertain_attacks)
        return new_iaf
