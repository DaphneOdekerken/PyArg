from typing import Optional, List

from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg_tests.modgil_prakken_aij_tests import get_argumentation_theory


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
            defeat.from_argument.add_outgoing_defeat(defeat.to_argument)
            defeat.to_argument.add_ingoing_defeat(defeat.from_argument)

    @classmethod
    def from_argumentation_theory(cls, name: str, argumentation_theory: ArgumentationTheory,
                                  ordering: Optional[Ordering] = None):
        """
        Create an abstract argumentation framework based on this argumentation theory. Note: if no ordering is given,
        last link elitist ordering is chosen as default ordering.

        :param name: The name of the argumentation framework.
        :param argumentation_theory: The argumentation theory from which the argumentation framework should be inferred.
        :param ordering: Ordering that influences which attacks are defeats. Note: default is last link elitist.
        :return: Abstract argumentation framework based on this argumentation theory.

        >>> arg_theory = get_argumentation_theory()
        >>> af = AbstractArgumentationFramework.from_argumentation_theory('af', arg_theory)
        >>> arg_for_r = af.get_argument('r')
        >>> arg_for_r.name
        'r'
        >>> defeaters_of_r = arg_for_r.get_ingoing_defeat_arguments
        >>> len(defeaters_of_r)
        1
        >>> defeaters_of_r[0].name
        '-r'
        >>> defeated_by_r = arg_for_r.get_ingoing_defeat_arguments
        >>> len(defeated_by_r)
        1
        >>> defeated_by_r[0].name
        '-r'
        >>> arg_for_not_r = af.get_argument('-r')
        >>> defeated_by_not_r = arg_for_not_r.get_outgoing_defeat_arguments
        >>> len(defeated_by_not_r)
        3
        """
#        if ordering is None:
#            ordering = LastLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
#                                               argumentation_theory.ordinary_premise_preference_dict)
        return cls(name, argumentation_theory.all_arguments, argumentation_theory.recompute_all_defeats(ordering))

    def get_incoming_defeat_arguments(self, argument: Argument) -> List[Argument]:
        """
        Get a list of arguments that defeat this argument.

        :param argument: Argument for which we want to know the incoming defeating arguments.
        :return: List of arguments that defeat this argument.

        >>> a = Argument('a')
        >>> b = Argument('b')
        >>> arguments = [a, b]
        >>> defeats = [Defeat(a, b)]
        >>> af = AbstractArgumentationFramework('af', arguments, defeats)
        >>> a in af.get_incoming_defeat_arguments(a)
        False
        >>> a in af.get_incoming_defeat_arguments(b)
        True
        """
        return [defeat.from_argument for defeat in self._defeats if defeat.to_argument == argument]

    def get_outgoing_defeat_arguments(self, argument: Argument) -> List[Argument]:
        """
        Get a list of arguments that are defeated by this argument.

        :param argument: The argument for which we want to know the arguments it defeats.
        :return: List of arguments that are defeated by this argument.

        >>> a = Argument('a')
        >>> b = Argument('b')
        >>> arguments = [a, b]
        >>> defeats = [Defeat(a, b)]
        >>> af = AbstractArgumentationFramework('af', arguments, defeats)
        >>> a in af.get_outgoing_defeat_arguments(a)
        False
        >>> b in af.get_outgoing_defeat_arguments(a)
        True
        """
        return [defeat.to_argument for defeat in self._defeats if defeat.from_argument == argument]

    def is_defeated(self, argument: Argument) -> bool:
        """
        Check if this argument is defeated by any argument.

        :param argument: Argument for which we want to know if it is defeated.
        :return: Boolean indicating if this argument is defeated by any argument.

        >>> a = Argument('a')
        >>> b = Argument('b')
        >>> c = Argument('c')
        >>> arguments = [a, b, c]
        >>> defeats = [Defeat(a, b), Defeat(c, c)]
        >>> af = AbstractArgumentationFramework('af', arguments, defeats)
        >>> af.is_defeated(a)
        False
        >>> af.is_defeated(b)
        True
        >>> af.is_defeated(c)
        True
        """
        return len(self.get_incoming_defeat_arguments(argument)) > 0

    def is_in_arguments(self, argument_name: str) -> bool:
        """
        Check if an argument with this name is part of the argumentation framework's arguments.

        :param argument_name: The name of the argument we try to find.
        :return: Boolean indicating if there is an argument with this name in the argumentation framework.

        >>> a = Argument('a')
        >>> b = Argument('b')
        >>> af = AbstractArgumentationFramework('af', [a], [])
        >>> af.is_in_arguments('a')
        True
        >>> af.is_in_arguments('b')
        False
        >>> af.is_in_arguments('c')
        False
        """
        return argument_name in self._arguments

    def get_argument(self, argument_name: str) -> Argument:
        """
        Get the argument with this name (if it exists, otherwise raise ValueError).

        :param argument_name: The name of the argument we try to find.
        :return: The argument with the specified name.

        >>> a = Argument('a')
        >>> af = AbstractArgumentationFramework('af', [a], [])
        >>> found_a = af.get_argument('a')
        >>> a == found_a
        True
        >>> found_b = af.get_argument('b')
        Traceback (most recent call last):
            ...
        ValueError: There is no argument named b.
        """
        if not self.is_in_arguments(argument_name):
            raise ValueError('There is no argument named ' + argument_name + '.')
        return self._arguments[argument_name]

    @property
    def arguments(self):
        """
        Get a list of all arguments in this argumentation framework.

        :return: A list of all arguments in this argumentation framework.

        >>> arg_theory = get_argumentation_theory()
        >>> af = AbstractArgumentationFramework.from_argumentation_theory('af', arg_theory)
        >>> len(af.arguments)
        8
        """
        return list(self._arguments.values())

    @property
    def defeats(self):
        """
        Get a list of all defeats in this argumentation framework.

        :return: A list of all defeats in this argumentation framework.

        >>> arg_theory = get_argumentation_theory()
        >>> af = AbstractArgumentationFramework.from_argumentation_theory('af', arg_theory)
        >>> len(af.defeats)
        5
        """
        return self._defeats


if __name__ == "__main__":
    import doctest

    doctest.testmod()
