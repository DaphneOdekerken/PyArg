from typing import Set


class Rule:
    """
    A Rule has a list of antecedents and a single consequent.
    """
    def __init__(self, rule_id: str, body: Set[str], head: str):
        self.id = str(rule_id)
        self.body = body
        self.head = head
        self.rule_str = str(self.head) + '<-' + ','.join([str(atom) for atom in sorted(self.body)])
        self.rule_hash = hash(self.rule_str)

    def get_signature(self) -> Set[str]:
        return self.body.union({self.head})

    def __eq__(self, other):
        return self.rule_hash == other.rule_hash

    def __str__(self):
        return self.rule_str

    def __hash__(self):
        return self.rule_hash

    def __lt__(self, other):
        return self.rule_hash < other.rule_hash


if __name__ == "__main__":
    import doctest
    doctest.testmod()
