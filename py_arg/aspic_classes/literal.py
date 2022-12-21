from functools import total_ordering


@total_ordering
class Literal:
    def __init__(self, literal_str: str):
        self.s1 = literal_str
        self.s1_hash = hash(self.s1)
        self.contraries_and_contradictories = []

    @classmethod
    def from_defeasible_rule(cls, defeasible_rule):
        return cls(defeasible_rule.id_str)

    @classmethod
    def from_defeasible_rule_negation(cls, defeasible_rule):
        return cls('-' + defeasible_rule.id_str)

    @classmethod
    def from_defeasible_rule_naf(cls, defeasible_rule):
        return cls('~' + defeasible_rule.id_str)

    def __str__(self):
        return self.s1

    def __repr__(self):
        return self.s1

    def __eq__(self, other):
        return self.s1_hash == other.s1_hash

    def __lt__(self, other):
        return str(self) < str(other)

    def is_contrary_or_contradictory_of(self, other) -> bool:
        """
        Boolean indicating if this Literal is a contrary or contradictory of some other Literal.

        :param other: Some other Literal that might be contrary or contradictory.
        """
        return other in self.contraries_and_contradictories

    def is_contradictory_of(self, other) -> bool:
        """
        Boolean indicating if this Literal is a contradictory of some other Literal.

        :param other: Some other Literal that might be contradictory.
        """
        return self.is_contrary_or_contradictory_of(other) and other.is_contrary_or_contradictory_of(self)

    def is_contrary_of(self, other) -> bool:
        """
        Boolean indicating if this Literal is a contrary of some other Literal.

        :param other: Some other Literal that might be contrary.
        """
        return self.is_contrary_or_contradictory_of(other) and not other.is_contrary_or_contradictory_of(self)

    def __hash__(self):
        return self.s1_hash
