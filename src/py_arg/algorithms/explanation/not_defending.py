from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.algorithms.explanation.reach_and_dist import get_reach


def get_not_defending(argumentation_framework: AbstractArgumentationFramework, argument: Argument, extensions):
    """
    Obtain for each extension without the argument the set of arguments that attack the argument and to which the
    extension provides no defense.
    In papers: NoDefAgainst. 
    
    :param argumentation_framework: the argumentation framework the explanation should be about
    :param argument: the argument that is not accepted
    :param extensions: the extensions (sets of accepted arguments) of the argumentation framework.
    :return: a list of sets of arguments, each representing one or more extensions, containing the arguments that
        attack the argument and to which the extension provides to defense.
    """
    reach, distance = get_reach(argumentation_framework, argument)

    attackers = set()
    not_defending_sets = []
    for pot_def_arg in reach:
        dist_pot_arg = distance[str(pot_def_arg)]
        for dist in dist_pot_arg:
            if dist % 2:
                attackers.add(pot_def_arg)
                break

    for extension in extensions:
        not_def_ext = set()
        if argument not in extension:
            for defeater in attackers:
                reach_def, distance_def = get_reach(argumentation_framework, defeater)
                defenders = set()
                for pot_defender in reach_def:
                    dist_pot_def = distance_def[str(pot_defender)]
                    for dist in dist_pot_def:
                        if dist % 2:
                            defenders.add(pot_defender)
                no_def_against = [nodefense for nodefense in defenders if nodefense not in extension]
                if no_def_against == list(defenders):
                    not_def_ext.add(defeater)
            if not_def_ext not in not_defending_sets:
                not_defending_sets.append(not_def_ext)

    return not_defending_sets


def get_no_dir_defending(argumentation_framework: AbstractArgumentationFramework, argument: Argument, extensions):
    """
    Obtain for each extension without the argument the set of arguments that directly attack the argument and to which
    the extension provides no direct defense.
    In papers: NoDirDefense. 
    
    :param argumentation_framework: the argumentation framework the explanation should be about
    :param argument: the argument that is not accepted
    :param extensions: the extensions (sets of accepted arguments) of the argumentation framework.
    :return: a list of sets of arguments, each representing one or more extensions, containing the arguments that
        directly attack the argument and to which the extension provides to direct defense.
    """
    not_dir_def_sets = []
    for extension in extensions:
        attackers = argumentation_framework.get_incoming_defeat_arguments(argument)
        not_def_ext = set()
        if argument not in extension:
            for attacker in argumentation_framework.get_incoming_defeat_arguments(argument):
                if [dirdf for dirdf in argumentation_framework.get_incoming_defeat_arguments(attacker)
                    if dirdf in extension] == []:
                    not_def_ext.add(attacker)
            if not_def_ext not in not_dir_def_sets:
                not_dir_def_sets.append(not_def_ext)

    return not_dir_def_sets


def get_no_self_defense(argumentation_framework: AbstractArgumentationFramework, argument: Argument, extensions):
    """
    Obtain for each set obtained with get_not_defending the arguments that are not attacked by the argument. 
    In papers: NoSelfDefense. 
    
    :param argumentation_framework: the argumentation framework the explanation should be about
    :param argument: the argument that is not accepted
    :param extensions: the extensions (sets of accepted arguments) of the argumentation framework.
    :return: a list of sets of arguments, each representing one or more extensions, containing the arguments that attack
        the argument, to which the extension provides to defense and which the argument itself does not (in)directly
        attack either.
    """
    not_defending = get_not_defending(argumentation_framework, argument, extensions)

    not_dir_defending_sets = []
    for not_def_ext in not_defending:
        not_ddef_ext = set()
        for attacker in not_def_ext:
            reach_att, distance_att = get_reach(argumentation_framework, attacker)
            defenders = set()
            for pot_defender in reach_att:
                dist_pot_def = distance_att[str(pot_defender)]
                for dist in dist_pot_def:
                    if dist % 2:
                        defenders.add(pot_defender)
            if argument not in defenders:
                not_ddef_ext.add(attacker)
        if not_ddef_ext not in not_dir_defending_sets:
            not_dir_defending_sets.append(not_ddef_ext)

    return not_dir_defending_sets
