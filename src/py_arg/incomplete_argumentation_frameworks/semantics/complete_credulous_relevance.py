import clingo
import pathlib

from grounded_relevance import ReachabilityPreprocessor

PATH_TO_ENCODINGS = pathlib.Path('encodings')


class CompleteRelevanceSolver:
    def __init__(self):
        self.last_model = None
        self.new_completion_model = None
        self.uncertain_arguments = []
        self.uncertain_attacks = []

    def enumerate_complete_credulous_relevant_updates(
            self, iaf_file, label: str, topic: str):
        file = ReachabilityPreprocessor().enumerate_reachable(iaf_file)
        iaf_file = file

        # Parse input so that we can iterate over uncertain arguments/attacks.
        self._parse_input(iaf_file)

        # Line 2: instantiate relevant to add and remove.
        relevant_arguments_to_add = set()
        relevant_attacks_to_add = set()
        relevant_arguments_to_remove = set()
        relevant_attacks_to_remove = set()

        # Line 3: prepare clingo.
        completion_control, guess_control = \
            self._init_clingo(iaf_file, topic, label)

        completions_tried = 0

        # Line 4.
        while True:
            # Line 5.
            with guess_control.solve(
                    on_model=self._store_completion, async_=True) as handle:
                handle.wait(5)
                handle.cancel()

            # Line 6.
            if self.last_model:
                completions_tried += 1
                # print(completions_tried)
                # Line 7 and 8: get the completion corresponding to last_model.
                last_completion_arguments, last_completion_attacks = \
                    self._get_guessed_completion()

                # Line 9 (for uncertain arguments).
                for query_uncertain_argument in self.uncertain_arguments:
                    # Line 10: check if query is new in this completion.
                    if query_uncertain_argument in last_completion_arguments:
                        # Line 11-15: is adding this argument relevant?
                        new_arguments = \
                            [arg for arg in last_completion_arguments
                             if arg != query_uncertain_argument]
                        addition_of_argument_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, new_arguments,
                                last_completion_attacks)
                        if addition_of_argument_is_relevant:
                            relevant_arguments_to_add.add(
                                query_uncertain_argument)

                    # Line 16.
                    else:
                        # Line 17-21: is removing this argument relevant?
                        new_arguments = last_completion_arguments + \
                                        [query_uncertain_argument]
                        removal_of_argument_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, new_arguments,
                                last_completion_attacks)
                        if removal_of_argument_is_relevant:
                            relevant_arguments_to_remove.add(
                                query_uncertain_argument)

                # Line 9 (for uncertain attacks).
                for query_uncertain_attack in self.uncertain_attacks:
                    # Line 10: check if query is new in this completion.
                    if query_uncertain_attack in last_completion_attacks:
                        # Line 11-15: is adding this attack relevant?
                        new_attacks = \
                            [att for att in last_completion_attacks
                             if att != query_uncertain_attack]
                        addition_of_attack_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, last_completion_arguments,
                                new_attacks)
                        if addition_of_attack_is_relevant:
                            relevant_attacks_to_add.add(
                                query_uncertain_attack)

                    # Line 16.
                    else:
                        # Line 17-21: is removing this attack relevant?
                        new_attacks = \
                            last_completion_attacks + [query_uncertain_attack]
                        removal_of_attack_is_relevant = \
                            self._check_answer_set_with_new_completion(
                                completion_control, last_completion_arguments,
                                new_attacks)
                        if removal_of_attack_is_relevant:
                            relevant_attacks_to_remove.add(
                                query_uncertain_attack)

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

    def _parse_input(self, iaf_file):
        with open(iaf_file, 'r') as infile:
            text = infile.read().split("\n")

        for line in text:
            if line.startswith('uarg'):
                self.uncertain_arguments.append(
                    line.split('(')[1].split(')')[0])
            elif line.startswith('uatt'):
                attack_from, attack_to = \
                    map(str.strip, line.split('(')[1].split(')')[0].split(','))
                self.uncertain_attacks.append((attack_from, attack_to))

    def _store_completion(self, model):
        self.last_model = model.symbols(shown=True)

    def _store_satisfiable(self, model):
        self.new_completion_model = model.symbols(shown=True)

    def _init_clingo(self, iaf_file, topic: str, label: str):
        guess_control = clingo.Control()
        guess_control.load(str(iaf_file))
        guess_control.add(f':- not lab({label},{topic}).')
        guess_control.load(str(PATH_TO_ENCODINGS / 'complete.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'valid_completion.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'labels.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'externals.dl'))
        guess_control.load(str(PATH_TO_ENCODINGS / 'guess.dl'))
        guess_control.ground([('base', [])], context=self)

        completion_control = clingo.Control()
        completion_control.load(str(iaf_file))
        completion_control.add(f':- not lab({label},{topic}).')
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
                if u_att[0] in last_completion_arguments and \
                        u_att[1] in last_completion_arguments:
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
        with completion_control.solve(
                on_model=self._store_satisfiable, async_=True) as handle:
            handle.wait(5)
            handle.cancel()

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


if __name__ == '__main__':
    example = pathlib.Path('examples') / 'ac.lp'
    solver = CompleteRelevanceSolver()
    rel_arguments_to_add, rel_attacks_to_add, \
        rel_arguments_to_remove, rel_attacks_to_remove = \
        solver.enumerate_complete_credulous_relevant_updates(
            example, 'undec', 'c')
    print('Relevant to add:')
    print(rel_arguments_to_add)
    print(rel_attacks_to_add)
    print('Relevant to remove:')
    print(rel_arguments_to_remove)
    print(rel_attacks_to_remove)
