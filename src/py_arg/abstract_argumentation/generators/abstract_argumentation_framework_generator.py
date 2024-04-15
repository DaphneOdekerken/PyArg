import random
from datetime import datetime
from typing import Optional

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class AbstractArgumentationFrameworkGenerator:
    def __init__(self, nr_of_arguments: int, nr_of_defeats: int,
                 allow_self_defeats: bool = True):
        """
        Construct a generator for making random AbstractArgumentationFramework
        objects.

        :param nr_of_arguments: The desired number of arguments.
        :param nr_of_defeats: The desired number of defeats.
        :param allow_self_defeats: Boolean indicating whether to allow
            self-defeats.
        """
        self.nr_of_arguments = nr_of_arguments
        self.nr_of_defeats = nr_of_defeats
        self.allow_self_defeats = allow_self_defeats

        if self.allow_self_defeats:
            if self.nr_of_defeats >\
                    self.nr_of_arguments * self.nr_of_arguments:
                raise ValueError('The number of defeats cannot be so high.')
        else:
            if self.nr_of_defeats > self.nr_of_arguments * \
                    (self.nr_of_arguments - 1):
                raise ValueError('The number of defeats cannot be so high.')

        if self.nr_of_arguments <= 26:
            self.argument_names = ALPHABET[:self.nr_of_arguments]
        else:
            self.argument_names = ['A' + str(i)
                                   for i in range(self.nr_of_arguments)]

    def generate(self, name: Optional[str] = None) -> \
            AbstractArgumentationFramework:
        """
        Generate a new AbstractArgumentationFramework.

        :param name: Name of the new framework (optional).
        :return: The resulting random AbstractArgumentationFramework.

        >>> generator = AbstractArgumentationFrameworkGenerator(3, 4, True)
        >>> af = generator.generate('MyAF')
        >>> len(af.arguments)
        3
        >>> len(af.defeats)
        4
        >>> af.name
        'MyAF'
        >>> generator = AbstractArgumentationFrameworkGenerator(1, 2, True)
        Traceback (most recent call last):
            ...
        ValueError: The number of defeats cannot be so high.
        >>> generator = AbstractArgumentationFrameworkGenerator(1, 1, False)
        Traceback (most recent call last):
            ...
        ValueError: The number of defeats cannot be so high.
        """
        # If no name is specified, a name containing a timestamp is generated.
        if not name:
            name = 'AF_Generated' + \
                   datetime.now().strftime('%d/%m/%Y,%H:%M:%S')

        # Construct arguments and randomly generate defeats.
        arguments = [Argument(arg_name) for arg_name in self.argument_names]
        defeats = []
        while len(defeats) < self.nr_of_defeats:
            defeat_from = random.choice(arguments)
            defeat_to = random.choice(arguments)
            if defeat_from != defeat_to or self.allow_self_defeats:
                # Self-defeat is not a problem here
                candidate_defeat = Defeat(defeat_from, defeat_to)
                if candidate_defeat not in defeats:
                    # This is a new defeat, so we can add it.
                    defeats.append(candidate_defeat)

        return AbstractArgumentationFramework(name, arguments, defeats)
