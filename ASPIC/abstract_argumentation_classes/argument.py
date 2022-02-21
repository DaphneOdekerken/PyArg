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
        self._ingoing_defeat_arguments.append(other)

    def add_outgoing_defeat(self, other: 'Argument'):
        self._outgoing_defeat_arguments.append(other)

    @property
    def get_ingoing_defeat_arguments(self) -> List['Argument']:
        return self._ingoing_defeat_arguments

    @property
    def get_outgoing_defeat_arguments(self) -> List['Argument']:
        return self._outgoing_defeat_arguments
