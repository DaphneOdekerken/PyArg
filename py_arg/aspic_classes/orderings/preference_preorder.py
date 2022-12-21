from typing import List, Tuple, Hashable


class PreferencePreorder:
    def __init__(self, preference_tuples: List[Tuple[Hashable, Hashable]]):
        self.preference_tuples = preference_tuples

    def is_weaker_than(self, object_a, object_b):
        return (object_a, object_b) in self.preference_tuples

    def is_strictly_weaker_than(self, object_a, object_b):
        return self.is_weaker_than(object_a, object_b) and not self.is_weaker_than(object_b, object_a)

    def __eq__(self, other):
        return set(sorted(self.preference_tuples)) == set(sorted(other.preference_tuples))

    def append(self, item):
        self.preference_tuples.append(item)
