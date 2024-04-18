import random
from datetime import datetime
from typing import Optional

from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class IAFGenerator:
    def __init__(self, nr_of_arguments: int, nr_of_defeats: int,
                 ratio_uncertain: float):
        """
        Construct a generator for making random IAFs.

        :param nr_of_arguments: The desired number of arguments.
        :param nr_of_defeats: The desired number of defeats.
        :param ratio_uncertain: Ratio of uncertain elements.
        """
        self.nr_of_arguments = nr_of_arguments
        self.nr_of_defeats = nr_of_defeats
        self.ratio_uncertain = ratio_uncertain

        if self.nr_of_defeats >\
                self.nr_of_arguments * self.nr_of_arguments:
            raise ValueError('The number of defeats cannot be so high.')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i)
                                   for i in range(self.nr_of_arguments)]

    def generate(self, name: Optional[str] = None) -> \
            IncompleteArgumentationFramework:
        """
        Generate a new IAF.

        :param name: Name of the new framework (optional).
        :return: The resulting random IAF.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_Generated' + \
                   datetime.now().strftime('%d/%m/%Y,%H:%M:%S')

        # Construct arguments and randomly generate defeats.
        nr_uncertain_arguments = \
            int(self.ratio_uncertain * self.nr_of_arguments)
        shuffle_arguments = \
            random.sample(range(self.nr_of_arguments), self.nr_of_arguments)

        certain_arguments = []
        uncertain_arguments = []
        certain_defeats = []
        uncertain_defeats = []
        all_argument_dict = {}

        for argument_index in shuffle_arguments[:nr_uncertain_arguments]:
            new_argument = Argument(self.argument_names[argument_index])
            uncertain_arguments.append(new_argument)
            all_argument_dict[argument_index] = new_argument
        for argument_index in shuffle_arguments[nr_uncertain_arguments:]:
            new_argument = Argument(self.argument_names[argument_index])
            certain_arguments.append(new_argument)
            all_argument_dict[argument_index] = new_argument

        # Get all (certain or uncertain) defeats
        defeats = []
        while len(defeats) < self.nr_of_defeats:
            defeat = random.choices(range(self.nr_of_arguments), k=2)
            if defeat not in defeats:
                defeats.append(defeat)
        # Partition between certain and uncertain
        nr_of_uncertain_defeats = \
            int(self.ratio_uncertain * self.nr_of_defeats)
        shuffle_defeats = random.sample(range(self.nr_of_defeats),
                                        self.nr_of_defeats)
        for defeat_i in shuffle_defeats[:nr_of_uncertain_defeats]:
            from_argument = all_argument_dict[defeats[defeat_i][0]]
            to_argument = all_argument_dict[defeats[defeat_i][1]]
            uncertain_defeats.append(Defeat(from_argument, to_argument))
        for defeat_i in shuffle_defeats[nr_of_uncertain_defeats:]:
            from_argument = all_argument_dict[defeats[defeat_i][0]]
            to_argument = all_argument_dict[defeats[defeat_i][1]]
            certain_defeats.append(Defeat(from_argument, to_argument))

        return IncompleteArgumentationFramework(
            name, certain_arguments, uncertain_arguments,
            certain_defeats, uncertain_defeats)
