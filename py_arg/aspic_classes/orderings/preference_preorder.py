from typing import List, Tuple, Hashable, Optional


class PreferencePreorder:
    def __init__(self, preference_tuples: Optional[List[Tuple[Hashable, Hashable]]] = None):
        if preference_tuples:
            self.preference_tuples = preference_tuples
        else:
            self.preference_tuples = []

    def is_weaker_than(self, object_a, object_b):
        return (object_a, object_b) in self.preference_tuples

    def is_strictly_weaker_than(self, object_a, object_b):
        return self.is_weaker_than(object_a, object_b) and not self.is_weaker_than(object_b, object_a)

    def __eq__(self, other):
        return set(sorted(self.preference_tuples)) == set(sorted(other.preference_tuples))

    def append(self, item: Tuple[Hashable, Hashable]):
        self.preference_tuples.append(item)

    @classmethod
    def create_reflexive_preorder(cls, items_to_be_ordered: List[Hashable]):
        preference_tuples = [(item_to_be_ordered, item_to_be_ordered) for item_to_be_ordered in items_to_be_ordered]
        return cls(preference_tuples)
