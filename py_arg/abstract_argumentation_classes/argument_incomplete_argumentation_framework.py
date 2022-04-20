from typing import Optional, List, Set, Tuple, Dict

from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.aspic_classes.orderings.last_link_ordering import LastLinkElitistOrdering
from py_arg.aspic_classes.orderings.ordering import Ordering
from py_arg.dynamic_aspic_classes.potential_argumentation_theory import PotentialArgumentationTheory


class ArgumentIncompleteArgumentationFramework:
    # TODO: Docstrings and tests.

    def __init__(self, name: str = '',
                 arguments: Optional[List[Argument]] = None,
                 uncertain_arguments: Optional[List[Argument]] = None,
                 defeats: Optional[List[Defeat]] = None):
        self.name = name

        if arguments is None:
            self._arguments = {}
        else:
            self._arguments = {argument.name: argument for argument in arguments}

        if uncertain_arguments is None:
            self._uncertain_arguments = {}
        else:
            if any(uncertain_argument in arguments for uncertain_argument in uncertain_arguments):
                raise ValueError('Argument cannot be both certain and uncertain.')
            self._uncertain_arguments = {argument.name: argument for argument in uncertain_arguments}

        if defeats is None:
            self._defeats = []
        else:
            self._defeats = defeats

        for defeat in defeats:
            if defeat.from_argument.name in self._arguments.keys():
                defeat_from_argument = self._arguments[defeat.from_argument.name]
            else:
                defeat_from_argument = self._uncertain_arguments[defeat.from_argument.name]
            if defeat.to_argument.name in self._arguments.keys():
                defeat_to_argument = self._arguments[defeat.to_argument.name]
            else:
                defeat_to_argument = self._uncertain_arguments[defeat.to_argument.name]
            defeat_from_argument.add_outgoing_defeat(defeat.to_argument)
            defeat_to_argument.add_ingoing_defeat(defeat.from_argument)

    @classmethod
    def from_potential_argumentation_theory(cls, name: str,
                                            potential_argumentation_theory: PotentialArgumentationTheory,
                                            ordering: Optional[Ordering] = None):
        if ordering is None:
            ordering = LastLinkElitistOrdering(potential_argumentation_theory.argumentation_system.rule_preference_dict,
                                               potential_argumentation_theory.ordinary_premise_preference_dict)
        arguments = potential_argumentation_theory.all_arguments
        uncertain_arguments = [pot_arg for pot_arg in potential_argumentation_theory.all_potential_arguments
                               if pot_arg not in arguments]
        defeats = potential_argumentation_theory.get_all_potential_defeats(ordering)
        return cls(name, arguments, uncertain_arguments, defeats)

    def get_necessary_grounded_extension(self) -> Tuple[Set[Argument], Set[Argument]]:
        ng = {argument for argument in self._arguments.values() if not argument.get_ingoing_defeat_arguments}
        ang = {argument for ng_argument in ng for argument in ng_argument.get_outgoing_defeat_arguments}

        change = True
        while change:
            new_in_ng = {argument for argument in self._arguments.values()
                         if argument not in ng and
                         all(attacking_argument in ang
                             for attacking_argument in argument.get_ingoing_defeat_arguments)}
            if new_in_ng:
                change = True
                ng = ng | new_in_ng
                ang = ang | {argument for ng_argument in ng for argument in ng_argument.get_outgoing_defeat_arguments}
            else:
                change = False

        return ng, ang

    @property
    def arguments(self) -> Dict[str, Argument]:
        return self._arguments

    @property
    def uncertain_arguments(self) -> Dict[str, Argument]:
        return self._uncertain_arguments

    def get_possible_grounded_extension(self) -> Tuple[Set[Argument], Set[Argument]]:
        all_certain_or_uncertain_arguments = list(self._uncertain_arguments.values()) + list(self._arguments.values())

        pg = {argument for argument in all_certain_or_uncertain_arguments
              if all(str(attacking_argument) not in self._arguments.keys()
                     for attacking_argument in argument.get_ingoing_defeat_arguments)}
        apg = {argument
               for pg_argument in pg
               for argument in pg_argument.get_outgoing_defeat_arguments
               if argument.name in self._arguments}

        change = True
        while change:
            new_in_pg = {argument for argument in all_certain_or_uncertain_arguments
                         if argument not in pg and
                         all(attacking_argument in apg
                             for attacking_argument in argument.get_ingoing_defeat_arguments)}
            if new_in_pg:
                change = True
                pg = pg | new_in_pg
                apg = apg | {argument for pg_argument in pg for argument in pg_argument.get_outgoing_defeat_arguments
                             if argument.name in self._arguments}
            else:
                change = False

        return pg, apg
