class Preference:
    def __init__(self, object_a, relation: str, object_b):
        if relation not in ['<', '=', '>', '?']:
            raise ValueError

        self.object_a = object_a
        self.relation = relation
        self.object_b = object_b

    def __str__(self):
        return str(self.object_a) + ' ' + self.relation + ' ' + str(self.object_b)

    def __eq__(self, other):
        if not isinstance(other, Preference):
            return False
        return self.object_a == other.object_a and self.object_b == other.object_b and self.relation == other.relation

    @classmethod
    def inversion(cls, preference: 'Preference'):
        if preference.relation == '<':
            inverted_relation = '>'
        else:
            inverted_relation = preference.relation
        return cls(preference.object_b, inverted_relation, preference.object_a)

    @property
    def is_strictly_weaker(self):
        return self.relation == '<'

    @property
    def is_weaker_or_equal(self):
        return self.relation in ['<', '=']

    @property
    def is_equally_strong(self):
        return self.relation == '='

    @property
    def is_stronger_or_equal(self):
        return self.relation in ['=', '>']

    @property
    def is_strictly_stronger(self):
        return self.relation == '>'
