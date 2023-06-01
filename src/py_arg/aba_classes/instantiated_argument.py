from typing import Set

from src.py_arg.aba_classes import Atom
from py_arg.abstract_argumentation_classes.argument import Argument


class InstantiatedArgument(Argument):
    """
    A Rule has a list of antecedents and a single consequent.
    """
    def __init__(self, argument_id: str, premise: Set[Atom], conclusion: Atom):
        self.id = str(argument_id)
        self.premise = premise
        self.conclusion = conclusion
        self.arg_str = ','.join([str(atom) for atom in sorted(self.premise)]) + '|-' + str(self.conclusion)
        super.__init__(self.arg_str)
        self.arg_hash = hash(self.arg_str)

    def __eq__(self, other):
        return self.arg_hash == other.arg_hash

    def __str__(self):
        return self.arg_str

    def __hash__(self):
        return self.arg_hash

    def __lt__(self, other):
        return self.arg_hash < other.arg_hash

