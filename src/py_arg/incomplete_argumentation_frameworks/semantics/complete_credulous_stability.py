import clingo
import pathlib

from py_arg.incomplete_argumentation_frameworks.semantics.clingo_utils import \
    add_iaf_and_topic_to_control

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class CompleteCredulousStabilitySolver:
    def __init__(self):
        self.argument_name_to_id = None
        self.id_to_argument_name = None
        self.last_model = None
        self.new_completion_model = None
        self.uncertain_arguments = []
        self.uncertain_attacks = []

    def check_stability(
            self, iaf, label: str, topic_str: str) -> bool:
        control = clingo.Control()
        self.argument_name_to_id, self.id_to_argument_name = \
            add_iaf_and_topic_to_control(iaf, topic_str, control)
        control.load(str(PATH_TO_ENCODINGS / 'complete.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'valid_completion.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'labels.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'externals.dl'))
        control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        control.ground([('base', [])], context=self)

        # Store certain and uncertain arguments (with clingo-friendly names).
        self.uncertain_arguments = \
            [self.argument_name_to_id[arg_name]
             for arg_name in iaf.uncertain_arguments.keys()]
        self.uncertain_attacks = \
            [(self.argument_name_to_id[defeat.from_argument.name],
              self.argument_name_to_id[defeat.to_argument.name])
             for defeat in iaf.uncertain_defeats]

        while True:
            # First search for a completion in which the topic does not have
            # the label.
            assumption_label = clingo.Function(
                'lab', [
                    clingo.Function(label),
                    clingo.Function(self.argument_name_to_id[topic_str])])
            control.solve(on_model=self._store_completion,
                          assumptions=[(assumption_label, False)])

            if self.last_model:
                # For now assume the completion corresponding to last_model.
                last_completion_arguments, last_completion_attacks = \
                    self._get_guessed_completion()

                # Can the topic have the label in this completion?
                topic_has_label = self._check_answer_set_with_new_completion(
                    control, last_completion_arguments,
                    last_completion_attacks, assumption_label)
                if not topic_has_label:
                    # If not, the topic is not stable-credulous-label.
                    return False

                # Refine to go to the next completion.
                self._refine_guess_control(control, last_completion_arguments,
                                           last_completion_attacks)

                # Reset last model.
                self.last_model = None

            else:
                # We did not find a completion where the topic is not
                # credulous-label, so it is stable.
                return True

    def _get_guessed_completion(self):
        last_completion_arguments = []
        last_completion_attacks = []
        for symbol in self.last_model:
            if symbol.name == 'argument':
                last_completion_arguments.append(
                    symbol.arguments[0].name)
            elif symbol.name == 'att':
                last_completion_attacks.append(
                    (symbol.arguments[0].name,
                     symbol.arguments[1].name))
        return last_completion_arguments, last_completion_attacks

    def _store_completion(self, model):
        self.last_model = model.symbols(shown=True)

    def _store_satisfiable(self, model):
        self.new_completion_model = model.symbols(shown=True)

    def _refine_guess_control(self, guess_control, last_completion_arguments,
                              last_completion_attacks):
        with guess_control.backend() as backend:
            refinement_rule_body = []
            for uncertain_arg in self.uncertain_arguments:
                if uncertain_arg in last_completion_arguments:
                    argument_sym = clingo.Function(
                        'eargument', [clingo.Function(uncertain_arg)])
                    argument_atom = backend.add_atom(argument_sym)
                    refinement_rule_body.append(argument_atom)
                else:
                    not_arg_sym = clingo.Function(
                        'enargument', [clingo.Function(uncertain_arg)])
                    not_argument_atom = backend.add_atom(not_arg_sym)
                    refinement_rule_body.append(not_argument_atom)
            for u_att in self.uncertain_attacks:
                if u_att in last_completion_attacks:
                    attack_sym = clingo.Function(
                        'eatt', [clingo.Function(u_att[0]),
                                clingo.Function(u_att[1])])
                    attack_atom = backend.add_atom(attack_sym)
                    refinement_rule_body.append(attack_atom)
                else:
                    not_attack_sym = clingo.Function(
                        'enatt', [clingo.Function(u_att[0]),
                                 clingo.Function(u_att[1])])
                    not_attack_atom = backend.add_atom(
                        not_attack_sym)
                    refinement_rule_body.append(not_attack_atom)
            backend.add_rule(head=[], body=refinement_rule_body)

    def _check_answer_set_with_new_completion(
            self, completion_control, new_arguments, new_attacks,
            assumption_label) -> bool:
        # Make completion with(out) query.
        externals_to_remove_later = []
        for uarg in self.uncertain_arguments:
            if uarg in new_arguments:
                new_a = clingo.Function(
                    'eargument', [clingo.Function(uarg)])
            else:
                new_a = clingo.Function(
                    'enargument', [clingo.Function(uarg)])
            completion_control.assign_external(new_a, True)
            externals_to_remove_later.append(new_a)
        for uatt in self.uncertain_attacks:
            if uatt in new_attacks:
                new_a = clingo.Function(
                    'eatt', [clingo.Function(uatt[0]),
                             clingo.Function(uatt[1])])
            else:
                new_a = clingo.Function(
                    'enatt', [clingo.Function(uatt[0]),
                              clingo.Function(uatt[1])])
            completion_control.assign_external(new_a, True)
            externals_to_remove_later.append(new_a)
        # Run solver for completion.
        completion_control.solve(on_model=self._store_satisfiable,
                                 assumptions=[(assumption_label, True)])

        # Check satisfiability and store result.
        result = False
        if self.new_completion_model:
            result = True

        # Cleaning up.
        self._clean_up_after_completion(
            completion_control, externals_to_remove_later)
        return result

    def _clean_up_after_completion(self, completion_control,
                                   externals_to_remove_later):
        for external_to_remove in externals_to_remove_later:
            completion_control.assign_external(external_to_remove, False)
        self.new_completion_model = None
