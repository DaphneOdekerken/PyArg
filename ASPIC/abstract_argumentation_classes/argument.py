from typing import List


class Argument:
    def __init__(self, name: str):
        self.name = name
        self._ingoing_defeat_arguments = []
        self._outgoing_defeat_arguments = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(str(self))

    def add_ingoing_defeat(self, other: 'Argument'):
        """
        Add ingoing defeat from the other argument. NOTE: does not add an outgoing defeat from other to this argument!

        :param other: The argument defeating this argument.
        """
        self._ingoing_defeat_arguments.append(other)

    def add_outgoing_defeat(self, other: 'Argument'):
        """
        Add outgoing defeat to the other argument. NOTE: does not add an ingoing defeat to the other argument!

        :param other: The argument defeated by this argument.
        """
        self._outgoing_defeat_arguments.append(other)

    @property
    def get_ingoing_defeat_arguments(self) -> List['Argument']:
        """
        Get all arguments that defeat this argument.

        :return: Arguments defeating this argument.

        >>> a = Argument('a')
        >>> b = Argument('b')
        >>> c = Argument('c')
        >>> a.add_ingoing_defeat(b)
        >>> a.add_ingoing_defeat(c)
        >>> a.get_ingoing_defeat_arguments
        [b, c]
        >>> b.add_outgoing_defeat(c)
        >>> c.get_ingoing_defeat_arguments
        []
        """
        return self._ingoing_defeat_arguments

    @property
    def get_outgoing_defeat_arguments(self) -> List['Argument']:
        """
        Get all arguments that are defeated by this argument.

        :return: Arguments defeated by this argument.

        >>> a = Argument('a')
        >>> b = Argument('b')
        >>> c = Argument('c')
        >>> a.add_outgoing_defeat(b)
        >>> a.add_outgoing_defeat(c)
        >>> a.get_outgoing_defeat_arguments
        [b, c]
        >>> b.add_ingoing_defeat(c)
        >>> c.get_outgoing_defeat_arguments
        []
        """
        return self._outgoing_defeat_arguments


if __name__ == "__main__":
    import doctest

    doctest.testmod()
