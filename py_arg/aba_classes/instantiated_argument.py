from typing import Set

from py_arg.aba_classes.atom import Atom
from py_arg.abstract_argumentation_classes.argument import Argument


class InstantiatedArgument(Argument):
    """
    A Rule has a list of antecedents and a single consequent.
    """
    def __init__(self, argument_id: str, premise: Set[Atom], conclusion: Atom):
        super().__init__(','.join([str(atom) for atom in sorted(premise)]) + '|-' + str(conclusion))
        self.id = str(argument_id)
        self.premise = premise
        self.conclusion = conclusion
        self.arg_hash = hash(self.name)

    def __eq__(self, other):
        return self.arg_hash == other.arg_hash

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.arg_hash

    def __lt__(self, other):
        return self.arg_hash < other.arg_hash

