from typing import Optional, List

from ASPIC.abstract_argumentation_classes.argument import Argument
from ASPIC.abstract_argumentation_classes.defeat import Defeat
from ASPIC.aspic_classes.argumentation_theory import ArgumentationTheory
from ASPIC.aspic_classes.last_link_ordering import LastLinkElitistOrdering
from ASPIC.aspic_classes.ordering import Ordering


class AbstractArgumentationFramework:
    def __init__(self, name: str = '',
                 arguments: Optional[List[Argument]] = None,
                 defeats: Optional[List[Defeat]] = None):
        self.name = name

        if arguments is None:
            self._arguments = {}
        else:
            self._arguments = {argument.name: argument for argument in arguments}

        if defeats is None:
            self._defeats = []
        else:
            self._defeats = defeats

        for defeat in defeats:
            defeat.from_argument.add_outgoing_attack(defeat.to_argument)
            defeat.to_argument.add_ingoing_attack(defeat.from_argument)

    @classmethod
    def from_argumentation_theory(cls, name: str, argumentation_theory: ArgumentationTheory,
                                  ordering: Optional[Ordering] = None):
        if ordering is None:
            ordering = LastLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                               argumentation_theory.ordinary_premise_preference_dict)
        return cls(name, argumentation_theory.all_arguments, argumentation_theory.get_all_defeats(ordering))

    def get_incoming_defeat_arguments(self, argument: Argument) -> List[Argument]:
        """

        :param argument:
        :return:

        >>> a = Argument('a')
        >>> b = Argument('b')
        >>> arguments = [a, b]
        >>> attacks = [Defeat(a, b)]
        >>> af = AbstractArgumentationFramework('af', arguments, attacks)
        >>> a in af.get_incoming_defeat_arguments(a)
        False
        >>> a in af.get_incoming_defeat_arguments(b)
        True
        """
        return [defeat.from_argument for defeat in self._defeats if defeat.to_argument == argument]

    def get_outgoing_defeat_arguments(self, argument: Argument) -> List[Argument]:
        return [defeat.to_argument for defeat in self._defeats if defeat.from_argument == argument]

    def is_defeated(self, argument: Argument) -> bool:
        return len(self.get_incoming_defeat_arguments(argument)) > 0

    def is_in_arguments(self, argument_name: str) -> bool:
        return argument_name in self._arguments

    def get_argument(self, argument_name: str) -> Argument:
        if not self.is_in_arguments(argument_name):
            raise ValueError('There is no argument named ' + argument_name + '.')
        return self._arguments[argument_name]

    @property
    def arguments(self):
        return list(self._arguments.values())

    @property
    def defeats(self):
        return self._defeats


if __name__ == "__main__":
    import doctest

    doctest.testmod()
