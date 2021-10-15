from typing import List


class Argument:
    def __init__(self, name: str):
        self.name = name
        self._ingoing_attack_arguments = []
        self._outgoing_attack_arguments = []

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(str(self))

    def add_ingoing_attack(self, other: 'Argument'):
        self._ingoing_attack_arguments.append(other)

    def add_outgoing_attack(self, other: 'Argument'):
        self._outgoing_attack_arguments.append(other)

    @property
    def get_ingoing_attack_arguments(self) -> List['Argument']:
        return self._ingoing_attack_arguments

    @property
    def get_outgoing_attack_arguments(self) -> List['Argument']:
        return self._outgoing_attack_arguments
