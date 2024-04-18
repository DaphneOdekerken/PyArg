import clingo
import pathlib

from py_arg.incomplete_argumentation_frameworks.semantics.clingo_utils import \
    add_iaf_and_topic_to_control
from py_arg.incomplete_argumentation_frameworks.semantics.\
    reachability_preprocessor import ReachabilityPreprocessor

PATH_TO_ENCODINGS = pathlib.Path(__file__).parent / 'encodings'


class CompleteSkepticalRelevanceSolver:
    def __init__(self):
        self.last_model = None
        self.new_completion_model = None
        self.uncertain_arguments = []
        self.uncertain_attacks = []
        self.argument_name_to_id = None
        self.id_to_argument_name = None

    def enumerate_relevant_updates(self, iaf, label: str, topic: str):
        new_iaf = ReachabilityPreprocessor().enumerate_reachable(iaf, topic)

        # Line 2: instantiate relevant to add and remove.
        relevant_arguments_to_add = set()
        relevant_attacks_to_add = set()
        relevant_arguments_to_remove = set()
        relevant_attacks_to_remove = set()

        # Line 3: prepare clingo.
        completion_control, guess_control = \
            self._init_clingo(new_iaf, topic, label)

        # Parse input so that we can iterate over uncertain arguments/attacks.
        self.uncertain_arguments = \
            [self.argument_name_to_id[arg_name]
             for arg_name in new_iaf.uncertain_arguments.keys()]
        self.uncertain_attacks = \
            [(self.argument_name_to_id[defeat.from_argument.name],
              self.argument_name_to_id[defeat.to_argument.name])
             for defeat in new_iaf.uncertain_defeats]

        # Line 4.
        while True:
            # Line 5.
            guess_control.solve(on_model=self._store_completion)

            # Line 6.
            if self.last_model:
                # Line 7 and 8: get the completion corresponding to last_model.
                last_completion_arguments, last_completion_attacks = \
                    self._get_guessed_completion()

                # Line 9 (for uncertain arguments).
                for query_uncertain_argument in self.uncertain_arguments:
                    # Line 10: check if query is new in this completion.
                    if query_uncertain_argument not in \
                            last_completion_arguments:
                        # Line 11-15: is adding this argument relevant?
                        new_arguments = last_completion_arguments + \
                                        [query_uncertain_argument]
                        addition_of_argument_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, new_arguments,
                                last_completion_attacks)
                        if addition_of_argument_is_relevant:
                            relevant_arguments_to_add.add(
                                self.id_to_argument_name[
                                    query_uncertain_argument])

                    # Line 16.
                    else:
                        # Line 17-21: is removing this argument relevant?
                        new_arguments = \
                            [arg for arg in last_completion_arguments
                             if arg != query_uncertain_argument]
                        removal_of_argument_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, new_arguments,
                                last_completion_attacks)
                        if removal_of_argument_is_relevant:
                            relevant_arguments_to_remove.add(
                                self.id_to_argument_name[
                                    query_uncertain_argument])

                # Line 9 (for uncertain attacks).
                for query_uncertain_attack in self.uncertain_attacks:
                    # Line 10: check if query is new in this completion.
                    if query_uncertain_attack not in last_completion_attacks:
                        # Line 11-15: is adding this attack relevant?
                        new_attacks = \
                            last_completion_attacks + [query_uncertain_attack]
                        addition_of_attack_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, last_completion_arguments,
                                new_attacks)
                        if addition_of_attack_is_relevant:
                            relevant_attacks_to_add.add(
                                (self.id_to_argument_name[
                                    query_uncertain_attack[0]],
                                 self.id_to_argument_name[
                                     query_uncertain_attack[1]]))

                    # Line 16.
                    else:
                        # Line 17-21: is removing this attack relevant?
                        new_attacks = \
                            [att for att in last_completion_attacks
                             if att != query_uncertain_attack]
                        removal_of_attack_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, last_completion_arguments,
                                new_attacks)
                        if removal_of_attack_is_relevant:
                            relevant_attacks_to_remove.add(
                                (self.id_to_argument_name[
                                     query_uncertain_attack[0]],
                                 self.id_to_argument_name[
                                     query_uncertain_attack[1]]))

                # Line 22: refine the original solver.
                self._refine_guess_control(guess_control,
                                           last_completion_arguments,
                                           last_completion_attacks)

                # Cleaning up.
                self.last_model = None

            # Line 23.
            else:
                # Line 24.
                return relevant_arguments_to_add, relevant_attacks_to_add, \
                    relevant_arguments_to_remove, relevant_attacks_to_remove

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

    def _init_clingo(self, iaf, topic: str, label: str):
        guess_control = clingo.Control()
        self.argument_name_to_id, self.id_to_argument_name = \
            add_iaf_and_topic_to_control(iaf, topic, guess_control)
        guess_control.add(f':- lab({label},'
                          f'{self.argument_name_to_id[topic]}).')
        guess_control.load(str(PATH_TO_ENCODINGS / 'complete.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'valid_completion.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'labels.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'externals.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        guess_control.ground([('base', [])], context=self)

        completion_control = clingo.Control()
        add_iaf_and_topic_to_control(iaf, topic, completion_control)
        completion_control.add(f':- lab({label},'
                               f'{self.argument_name_to_id[topic]}).')
        completion_control.load(str(PATH_TO_ENCODINGS / 'complete.dl'))
        completion_control.load(str(PATH_TO_ENCODINGS / 'valid_completion.dl'))
        completion_control.load(str(PATH_TO_ENCODINGS / 'labels.dl'))
        completion_control.load(str(PATH_TO_ENCODINGS / 'externals.dl'))
        completion_control.ground([('base', [])], context=self)

        return completion_control, guess_control

    def _refine_guess_control(self, guess_control, last_completion_arguments,
                              last_completion_attacks):
        with guess_control.backend() as backend:
            refinement_rule_body = []
            for uncertain_arg in self.uncertain_arguments:
                if uncertain_arg in last_completion_arguments:
                    argument_sym = clingo.Function(
                        'argument', [clingo.Function(uncertain_arg)])
                    argument_atom = backend.add_atom(argument_sym)
                    refinement_rule_body.append(argument_atom)
                else:
                    not_arg_sym = clingo.Function(
                        'nargument', [clingo.Function(uncertain_arg)])
                    not_argument_atom = backend.add_atom(not_arg_sym)
                    refinement_rule_body.append(not_argument_atom)
            for u_att in self.uncertain_attacks:
                if u_att in last_completion_attacks:
                    attack_sym = clingo.Function(
                        'att', [clingo.Function(u_att[0]),
                                clingo.Function(u_att[1])])
                    attack_atom = backend.add_atom(attack_sym)
                    refinement_rule_body.append(attack_atom)
                else:
                    not_attack_sym = clingo.Function(
                        'natt', [clingo.Function(u_att[0]),
                                 clingo.Function(u_att[1])])
                    not_attack_atom = backend.add_atom(
                        not_attack_sym)
                    refinement_rule_body.append(not_attack_atom)
            backend.add_rule(head=[], body=refinement_rule_body)

    def _check_answer_set_with_new_completion(
            self, completion_control, new_arguments, new_attacks) -> bool:
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
        completion_control.solve(on_model=self._store_satisfiable)

        # Check satisfiability and store result.
        result = False
        if not self.new_completion_model:
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
