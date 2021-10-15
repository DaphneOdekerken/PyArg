from typing import Set

from .literal import Literal


class Rule:
    """
    A Rule has a list of antecedents and a single consequent. Furthermore, it has a string rule description.
    """
    def __init__(self, rule_id: int, antecedents: Set[Literal], consequent: Literal, rule_description: str):
        self.id = rule_id
        self.antecedents = antecedents
        self.consequent = consequent
        self.rule_description = rule_description
        self.rule_str = ','.join([str(antecedent) for antecedent in self.antecedents]) + '=>' + str(self.consequent)
        self.rule_hash = hash(self.rule_str)

    def is_rule_for(self, literal: Literal) -> bool:
        """
        Check if this is a Rule for a specific Literal.

        :param literal: The specific Literal for which this might be a Rule.
        :return: Boolean indicating if this is a Rule for the Literal.
        """
        return literal == self.consequent

    def __eq__(self, other):
        return list(self.antecedents) == list(other.antecedents) and self.consequent == other.consequent

    def __str__(self):
        return self.rule_str

    def __hash__(self):
        return self.rule_hash


if __name__ == "__main__":
    import doctest
    doctest.testmod()
