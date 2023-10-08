import itertools
from typing import Optional, List, Dict

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat


class IncompleteArgumentationFramework:
    """
    An incomplete argumentation framework (IAF) is an extension to abstract argumentation frameworks
    in which the sets of arguments and defeats are each split in two disjoint parts: a certain part
    and an uncertain part.
    """
    def __init__(self, name: str = '',
                 arguments: Optional[List[Argument]] = None,
                 uncertain_arguments: Optional[List[Argument]] = None,
                 defeats: Optional[List[Defeat]] = None,
                 uncertain_defeats: Optional[List[Defeat]] = None):
        self.name = name

        if arguments is None:
            self._arguments = {}
        else:
            self._arguments = {argument.name: argument for argument in arguments}

        if uncertain_arguments is None:
            self._uncertain_arguments = {}
        else:
            if any(uncertain_argument in arguments for uncertain_argument in uncertain_arguments):
                raise ValueError('Argument cannot be both certain and uncertain.')
            self._uncertain_arguments = {argument.name: argument for argument in uncertain_arguments}

        if defeats is None:
            self._defeats = []
        else:
            self._defeats = defeats

        if uncertain_defeats is None:
            self._uncertain_defeats = []
        else:
            self._uncertain_defeats = uncertain_defeats

        for defeat in self._defeats + self._uncertain_defeats:
            if defeat.from_argument.name in self._arguments.keys():
                defeat_from_argument = self._arguments[defeat.from_argument.name]
            else:
                defeat_from_argument = self._uncertain_arguments[defeat.from_argument.name]
            if defeat.to_argument.name in self._arguments.keys():
                defeat_to_argument = self._arguments[defeat.to_argument.name]
            else:
                defeat_to_argument = self._uncertain_arguments[defeat.to_argument.name]
            defeat_from_argument.add_outgoing_defeat(defeat.to_argument)
            defeat_to_argument.add_ingoing_defeat(defeat.from_argument)

    def __eq__(self, other):
        return isinstance(other, IncompleteArgumentationFramework) and \
            self.arguments == other.arguments and \
            self.uncertain_arguments == other.uncertain_arguments and \
            self.defeats == other.defeats and \
            self.uncertain_defeats == other.uncertain_defeats

    def __repr__(self):
        return '( [' + ', '.join(argument_key for argument_key in self.arguments.keys()) + \
            '], [' + ', '.join(argument_key for argument_key in self.uncertain_arguments.keys()) + \
            '], [' + ', '.join(defeat.__repr__() for defeat in self.defeats) + \
            '], [' + ', '.join(defeat.__repr__() for defeat in self.uncertain_defeats) + '] )'

    @property
    def arguments(self) -> Dict[str, Argument]:
        """
        Obtain the (certain) arguments of the IAF.
        """
        return self._arguments

    @property
    def uncertain_arguments(self) -> Dict[str, Argument]:
        """
        Obtain the uncertain arguments of the IAF.
        """
        return self._uncertain_arguments

    @property
    def defeats(self) -> List[Defeat]:
        """
        Obtain the (certain) defeats of the IAF.
        """
        return self._defeats

    @property
    def uncertain_defeats(self) -> List[Defeat]:
        """
        Obtain the uncertain defeats of the IAF.
        """
        return self._uncertain_defeats

    @property
    def certain_projection(self) -> AbstractArgumentationFramework:
        """
        The certain projection consists of all certain arguments and all certain defeats between two
        certain arguments.
        """
        arguments = list(self._arguments.values())
        return AbstractArgumentationFramework(arguments=arguments,
                                              defeats=[defeat for defeat in self._defeats
                                                       if defeat.from_argument in arguments and
                                                       defeat.to_argument in arguments])

    def get_all_completions(self) -> List[AbstractArgumentationFramework]:
        """
        The set of completions consists of all abstract AFs that can be obtained by resolving the
        uncertainties of the IAF.
        """

        def powerset(s):
            return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

        remaining_uncertain_argument_options = powerset(self.uncertain_arguments.values())
        remaining_uncertain_defeat_options = powerset(self.uncertain_defeats)
        combined_options = itertools.product(remaining_uncertain_argument_options, remaining_uncertain_defeat_options)

        result = []
        arguments = list(self.arguments.values())
        for uncertain_arguments, uncertain_defeats in combined_options:
            all_arguments = sorted(arguments + list(uncertain_arguments))
            all_defeats = sorted(self.defeats + list(uncertain_defeats))
            completion = AbstractArgumentationFramework(
                arguments=all_arguments,
                defeats=[defeat for defeat in all_defeats
                         if defeat.to_argument in all_arguments and defeat.from_argument in all_arguments]
            )
            if completion not in result:
                result.append(completion)

        return result

    def get_all_partial_completions(self) -> List['IncompleteArgumentationFramework']:
        """
        The set of partial completions consists of all IAFs that can be obtained by resolving some of the
        uncertainties of the IAF, as well as the original IAF itself.
        """

        def powerset(s):
            return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

        # Remember the old values.
        old_certain_arguments = list(self.arguments.values())
        old_certain_defeats = self.defeats
        old_uncertain_arguments = self.uncertain_arguments.values()
        old_uncertain_defeats = self.uncertain_defeats

        # Construct all possible combinations of uncertain elements.
        remaining_uncertain_argument_options = powerset(old_uncertain_arguments)
        remaining_uncertain_defeat_options = powerset(old_uncertain_defeats)
        combined_options = itertools.product(remaining_uncertain_argument_options, remaining_uncertain_defeat_options)

        result = []
        for uncertain_arguments, uncertain_defeats in combined_options:
            # This is a particular guess for the uncertain elements that will remain (as either certain or uncertain
            # arguments) in the partial completion.

            # Now construct all possible combinations of these remaining elements.
            new_certain_argument_options = powerset(uncertain_arguments)
            new_certain_defeat_options = powerset(uncertain_defeats)
            new_combined_options = itertools.product(new_certain_argument_options, new_certain_defeat_options)

            for new_certain_arguments, new_certain_defeats in new_combined_options:
                # This is a particular guess for the elements that will become the new certain elements in the partial
                # completion.
                all_new_certain_arguments = sorted(old_certain_arguments + list(new_certain_arguments))
                all_new_certain_defeats = sorted(old_certain_defeats + list(new_certain_defeats))
                new_uncertain_arguments = sorted([arg for arg in uncertain_arguments
                                                  if arg not in new_certain_arguments])
                new_uncertain_defeats = sorted([defeat for defeat in uncertain_defeats
                                                if defeat not in new_certain_defeats])

                all_new_certain_or_uncertain_arguments = all_new_certain_arguments + new_uncertain_arguments

                partial_completion = IncompleteArgumentationFramework(
                    arguments=all_new_certain_arguments,
                    uncertain_arguments=new_uncertain_arguments,
                    defeats=[defeat for defeat in all_new_certain_defeats
                             if defeat.to_argument in all_new_certain_or_uncertain_arguments and
                             defeat.from_argument in all_new_certain_or_uncertain_arguments],
                    uncertain_defeats=[defeat for defeat in new_uncertain_defeats
                                       if defeat.to_argument in all_new_certain_or_uncertain_arguments and
                                       defeat.from_argument in all_new_certain_or_uncertain_arguments]
                )
                if partial_completion not in result:
                    result.append(partial_completion)

        return result
