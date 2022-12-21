from dash import html

from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.algorithms.explanation.defending import get_defending, get_dir_defending
from py_arg.algorithms.explanation.not_defending import get_not_defending, get_no_dir_defending, get_no_self_defense
from py_arg.algorithms.explanation.suff_nec import get_suff_nec
from py_arg.algorithms.semantics.get_admissible_sets import get_admissible_sets
from py_arg.algorithms.semantics.get_complete_extensions import get_complete_extensions
from py_arg.algorithms.semantics.get_eager_extension import get_eager_extension
from py_arg.algorithms.semantics.get_grounded_extension import get_grounded_extension
from py_arg.algorithms.semantics.get_ideal_extension import get_ideal_extension
from py_arg.algorithms.semantics.get_preferred_extensions import get_preferred_extensions
from py_arg.algorithms.semantics.get_semistable_extensions import get_semistable_extensions
from py_arg.algorithms.semantics.get_stable_extensions import get_stable_extensions
from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.orderings.argument_orderings.last_link_ordering import LastLinkDemocraticOrdering, \
    LastLinkElitistOrdering
from py_arg.aspic_classes.orderings.argument_orderings.weakest_link_ordering import WeakestLinkDemocraticOrdering, \
    WeakestLinkElitistOrdering
from py_arg.aspic_classes.strict_rule import StrictRule

expl_function_options = {
    'Acc': ['Defending', 'DirDefending', 'Suff', 'MinSuff', 'Nec'],
    'NonAcc': ['NoDefAgainst', 'NoDirDefense', 'NoSelfDefense']
}


def get_argumentation_framework(arguments, attacks):
    '''
    Calculate the abstract argumentation theory from the given arguments and attacks between them.

    :param arguments: The provided arguments.
    :param attacks: The provided attacks.
    '''
    arg_list = [Argument(arg) for arg in arguments.replace(',', '').split()]
    defeat_list = []

    for attack in attacks.splitlines():
        att_list = attack.replace(' ', '').replace(')', '').replace('(', '').split(',')
        if att_list[0] == '' or att_list[1] == '':
            continue
        attacker = Argument(att_list[0])
        attacked = Argument(att_list[1])
        defeat_list.append(Defeat(attacker, attacked))

    arg_framework = AbstractArgumentationFramework('AF', arg_list, defeat_list)
    return arg_framework


def get_argumentation_theory(axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences, ordering):
    '''
    Calculate the argumentation theory from the axioms, ordinary premises, strict and defeasible rules, premise and
    rule preference and the given ordering

    :param axioms: The provided axioms (premises that cannot be attacked).
    :param ordinary: The ordinary premises (premises that can be questioned).
    :param strict: The provided strict rules (rules that cannot be attacked).
    :param defeasible: The defeasible rules (rules that can be questioned).
    :param premise_preferences: The preferences over the ordinary premises.
    :param rule_preferences: The preferences over the defeasible rules.
    :param ordering: The chosen ordering, combining both last/weakest link and democratic/elitist.
    '''
    arg_sys = ArgumentationSystem({}, {}, [], [])
    arg_theory = ArgumentationTheory(arg_sys, [], [])
    error_statement = ''

    axiom_list = axioms.split()
    ordinary_list = ordinary.split()
    strrule_sep = []
    for strr in strict.splitlines():
        strrule_sep += strr.replace(' ', '').replace('->', ',').split(',')
    strrule_list = []
    for strrules in strrule_sep:
        strrule_list.append(strrules)
    defrule_sep = []
    for defr in defeasible.splitlines():
        defrule_sep += defr.replace(' ', '').replace('=>', ',').replace(':', ',').split(',')
    defrule_list = []
    for defrules in defrule_sep:
        defrule_list.append(defrules)
    literal_str_list = set()
    for item in axiom_list + ordinary_list + strrule_list + defrule_list:
        if item[0] in '-~':
            item = item[1:]
        literal_str_list.add(item)
        literal_str_list.add('-' + item)
        literal_str_list.add('~' + item)
    literal_str_list = list(literal_str_list)

    # for ax in axiom_list:
    #     literal_str_list.append(ax)
    # for op in ordinary_list:
    #     literal_str_list.append(op)
    # for strr in strrule_list:
    #     literal_str_list.append(strr)
    # for defr in defrule_list:
    #     literal_str_list.append(defr)

    # literal_str_list += ['-' + literal_str for literal_str in literal_str_list]
    # literal_str_list += ['~' + literal_str for literal_str in literal_str_list]
    #
    # literal_str_list = list(dict.fromkeys(literal_str_list))

    language = {literal_str: Literal(literal_str)
                for literal_str in literal_str_list}
    contraries = {literal_str: [] for literal_str in language.keys()}
    for literal_str in language.keys():
        if literal_str[0] in ('~', '-'):
            contraries[literal_str].append(language[literal_str[1:]])
        else:
            contraries[literal_str].append(language['-' + literal_str])

    strrule_sep = strict.replace(' ', '').splitlines()
    strrules = []
    defrule_sep = defeasible.replace(' ', '').splitlines()
    defrules = []

    i = 1
    for rule in strrule_sep:
        if rule.find('=>') != -1:
            return arg_theory, html.Div([html.H4('Error', style={'color': 'red'}),
                                         'a strict rule contains a defeasible rule (i.e., the arrow =>)'])
        sep_antcon = rule.split('->')
        ant_str_list = sep_antcon[0].split(',')
        antecedents = set(())
        for antecedent in ant_str_list:
            lang_ant = language[antecedent]
            antecedents.add(lang_ant)
        conclusion = language[sep_antcon[1]]
        strrules.append(StrictRule(i, antecedents, conclusion, 's' + str(i)))
        i = i + 1

    j = 1
    for rule in defrule_sep:
        if rule.find('->') != -1:
            return arg_theory, html.Div([html.H4('Error', style={'color': 'red'}),
                                         'a defeasible rule contains a strict rule (i.e., the arrow ->)'])
        sep_antcon = rule.split('=>')
        rule_id = sep_antcon[0].split(':')[0]
        try:
            ant_str_list = sep_antcon[0].split(':')[1].split(',')
        except:
            return arg_theory, html.Div([html.H4('Error', style={'color': 'red'}),
                                         'defeasible rules should contain a name and at least one antecedent, '
                                         'e.g.: di: a=> b.'])
        antecedents = set(())
        for antecedent in ant_str_list:
            lang_ant = language[antecedent]
            antecedents.add(lang_ant)
        conclusion = language[sep_antcon[1]]
        defrules.append(DefeasibleRule(rule_id, antecedents, conclusion, rule_id))
        j = j + 1

    for defeasible_rule in defrules:
        defeasible_rule_literal = Literal.from_defeasible_rule(defeasible_rule)
        defeasible_rule_literal_negation = Literal.from_defeasible_rule_negation(defeasible_rule)
        language[str(defeasible_rule_literal)] = defeasible_rule_literal
        language[str(defeasible_rule_literal_negation)] = defeasible_rule_literal_negation
        contraries[str(defeasible_rule_literal)] = [defeasible_rule_literal_negation]
        contraries[str(defeasible_rule_literal_negation)] = [defeasible_rule_literal]

    arg_sys = ArgumentationSystem(language, contraries, strrules, defrules)

    axioms = [language[literal_str] for literal_str in axiom_list]
    ordinary_premises = [language[literal_str] for literal_str in ordinary_list]

    arg_theory = ArgumentationTheory(arg_sys, axioms, ordinary_premises)

    premise_preference_list = premise_preferences.replace(' ', '').splitlines()
    rule_preference_list = rule_preferences.replace(' ', '').splitlines()
    for preference in premise_preference_list:
        if preference.find('<') != -1:
            pref_items = preference.rsplit('<')
            arg_theory.ordinary_premise_preferences.append((language[pref_items[0]], language[pref_items[1]]))

        elif preference.find('>') != -1:
            pref_items = preference.rsplit('>')
            arg_theory.ordinary_premise_preferences.append((language[pref_items[1]], language[pref_items[0]]))

    for preference in rule_preference_list:
        if preference.find('<') != -1:
            pref_items = preference.rsplit('<')
            for def_rule in defrules:
                if str(def_rule.id) == pref_items[0]:
                    weaker_rule = def_rule
            for def_rule in defrules:
                if str(Literal.from_defeasible_rule(def_rule)) == pref_items[1]:
                    stronger_rule = def_rule
            arg_theory.argumentation_system.rule_preferences.append((weaker_rule, stronger_rule))
        elif preference.find('>') != -1:
            pref_items = preference.rsplit('>')
            for def_rule in defrules:
                if str(def_rule.id) == pref_items[1]:
                    weaker_rule = def_rule
            for def_rule in defrules:
                if str(Literal.from_defeasible_rule(def_rule)) == pref_items[0]:
                    stronger_rule = def_rule
            arg_theory.argumentation_system.rule_preferences.append((weaker_rule, stronger_rule))

    return arg_theory, error_statement


def get_abstr_extensions(arg_framework, semantics):
    '''
    Calculate the set of extensions from the given abstract argumentation framework and chosen semantics

    :param arg_framework: The abstract argumentation framework.
    :param semantics: The chosen semantics.
    '''
    if semantics == 'Adm':
        return get_admissible_sets(arg_framework)
    if semantics == 'Cmp':
        return get_complete_extensions(arg_framework)
    if semantics == 'Grd':
        return get_grounded_extension(arg_framework)
    if semantics == 'Prf':
        return get_preferred_extensions(arg_framework)
    if semantics == 'Idl':
        return get_ideal_extension(arg_framework)
    if semantics == 'Stb':
        return get_stable_extensions(arg_framework)
    if semantics == 'Sstb':
        return get_semistable_extensions(arg_framework)
    if semantics == 'Egr':
        return get_eager_extension(arg_framework)


def get_str_extensions(argumentation_theory, semantics, ordering_choice):
    '''
    Calculate the set of extensions from the given argumentation theory, type of ordering and semantics

    :param argumentation_theory: The argumentation theory.
    :param semantics: The chosen semantics.
    :param ordering_choice: The chosen ordering, combining both last/weakest link and democratic/elitist.
    '''
    if ordering_choice == 'demlastl':
        ordering = LastLinkDemocraticOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                              argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'elilastl':
        ordering = LastLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                           argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'demweakl':
        ordering = WeakestLinkDemocraticOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                                 argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'eliweakl':
        ordering = WeakestLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                              argumentation_theory.ordinary_premise_preference_dict)
    else:
        ordering = None

    abstractAF = argumentation_theory.create_abstract_argumentation_framework('af', ordering)

    if semantics == 'Adm':
        return get_admissible_sets(abstractAF)
    if semantics == 'Cmp':
        return get_complete_extensions(abstractAF)
    if semantics == 'Grd':
        return get_grounded_extension(abstractAF)
    if semantics == 'Prf':
        return get_preferred_extensions(abstractAF)
    if semantics == 'Idl':
        return get_ideal_extension(abstractAF)
    if semantics == 'Stb':
        return get_stable_extensions(abstractAF)
    if semantics == 'Sstb':
        return get_semistable_extensions(abstractAF)
    if semantics == 'Egr':
        return get_eager_extension(abstractAF)


def get_accepted_formulas(extensions, strategy):
    '''
    Calculate the set of accepted formulas from a set of extensions (sets of arguments) and evaluation strategy

    :param extensions: The extensions (sets of collectively accepted arguments).
    :param strategy: The evaluation strategy (e.g., skeptical or credulous).
    '''
    accepted_args = set()
    accepted_formulas = set()
    if strategy == 'Skep':
        accepted_args = set.intersection(*extensions)
        set(accepted_formulas.add(arg.conclusion) for arg in accepted_args)
    elif strategy == 'Cred':
        accepted_args = set.union(*extensions)
        set(accepted_formulas.add(arg.conclusion) for arg in accepted_args)
    elif strategy == 'WSkep':
        extension_formulas = []
        for extension in extensions:
            ext_form = {arg.conclusion for arg in extension}
            extension_formulas.append(ext_form)
        accepted_formulas = set.intersection(*extension_formulas)

    return accepted_formulas


def get_abstr_explanations(arg_framework, semantics, extensions, accepted, function, expl_type, strategy):
    '''
    Calculate, for each argument, the explanations, given the function, type and strategy.

    :param arg_framework: The argumentation framework the explanation has to be calculated from.
    :param semantics: The semantics used to determine (non-)acceptance.
    :param extensions: The sets of accepted arguments in arg_framework, based on semantics.
    :param accepted: The arguments that are considered accepted given the extensions and strategy.
    :param function: The explanation function, to determine the content of the explanation.
    :param expl_type: The explanation type, to determine acceptance/non-acceptance explanation.
    :param strategy: The strategy of the explanation, whether credulous or skeptical reasoning.
    :return: A dictionary with for each (non-)accepted argument its explanation, given the parameters.
    '''
    explanation = {}
    not_accepted = [arg for arg in arg_framework.arguments if arg not in accepted]
    if expl_type == 'Acc':
        for arg in accepted:
            if function == 'Defending':
                explanation[str(arg)] = get_defending(arg_framework, arg, extensions)
            elif function == 'DirDefending':
                explanation[str(arg)] = get_dir_defending(arg_framework, arg, extensions)
            else:
                explanation[str(arg)] = get_suff_nec(arg_framework, arg, function, expl_type)
        return explanation

    elif expl_type == 'NonAcc':
        for arg in not_accepted:
            if function == 'NoDefAgainst':
                explanation[str(arg)] = get_not_defending(arg_framework, arg, extensions)
            elif function == 'NoDirDefense':
                explanation[str(arg)] = get_no_dir_defending(arg_framework, arg, extensions)
            elif function == 'NoSelfDefense':
                explanation[str(arg)] = get_no_self_defense(arg_framework, arg, extensions)
        return explanation


def get_str_explanations(argumentation_theory, semantics, ordering_choice, extensions, accepted_formulas, function, expl_type, strategy, form):
    '''
    Calculate, for each formula, the explanations, given the function, type, strategy and form.

    :param argumentation_Theory: the argumentation theory the explanation has to be calculated from.
    :param semantics: The semantics used to determine (non-)acceptance.
    :param ordering_choice: The chosen ordering, combining both last/weakest link and democratic/elitist.
    :param extensions: The sets of accepted arguments in arg_framework, based on semantics.
    :param accepted_formulas: The formulas that are considered accepted given the extensions and strategy.
    :param function: The explanation function, to determine the content of the explanation.
    :param expl_type: The explanation type, to determine acceptance/non-acceptance explanation.
    :param strategy: The strategy of the explanation, whether credulous or skeptical reasoning.
    :param form: The form of the explanation, for example, explanations in terms of arguments, rules or premises.
    :return: A dictionary with for each (non-)accepted argument its explanation, given the parameters.
    '''
    if ordering_choice == 'demlastl':
        ordering = LastLinkDemocraticOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                              argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'elilastl':
        ordering = LastLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                           argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'demweakl':
        ordering = WeakestLinkDemocraticOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                                 argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'eliweakl':
        ordering = WeakestLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                              argumentation_theory.ordinary_premise_preference_dict)
    else:
        ordering = None
    abstractAF = argumentation_theory.create_abstract_argumentation_framework('af', ordering)
    abstr_explanation = {}
    if expl_type == 'Acc':
        for formula in accepted_formulas:
            form_arg = argumentation_theory.arguments[formula]
            arg_expl = []
            suff_expl = []
            for arg in form_arg:
                if function == 'Defending':
                    arg_expl.extend(get_defending(abstractAF, arg, extensions))
                elif function == 'DirDefending':
                    arg_expl.extend(get_dir_defending(abstractAF, arg, extensions))
                else:
                    suff_expl.extend(get_suff_nec(abstractAF, arg, 'Suff', expl_type))
            if suff_expl != []:
                if function == 'Suff':
                    arg_expl.extend(suff_expl)
                else:
                    form_expl = []
                    form_expls = []
                    if form == 'Arg':
                        form_expl = suff_expl
                    else:
                        for sets in suff_expl:
                            set_expl = []
                            for arg in sets:
                                if form == 'Prem' and arg.premises not in form_expl:
                                    set_expl.append(arg.premises)
                                elif form == 'Rule':
                                    defrules = arg.defeasible_rules
                                    rules = defrules.union(arg.strict_rules)
                                    if rules not in form_expl:
                                        set_expl.append(rules)
                                elif form == 'SubArg' and arg.sub_arguments not in form_expl:
                                    set_expl.append(arg.sub_arguments)
                                elif form == 'SubArgConc':
                                    subargconc = set()
                                    for subarg in arg.sub_arguments:
                                        if subarg.conclusion not in subargconc:
                                            subargconc.add(subarg.conclusion)
                                    set_expl.append(subargconc)
                            form_expl.append(set_expl)

                        for expl in form_expl:
                            form_expls.append(set().union(*expl))
                        form_expl = form_expls

                    if function == 'MinSuff':
                        minsuff_expl = []
                        sort_form_expl = sorted(form_expl, key=len)
                        for suff in sort_form_expl:
                            minsuff_suff = []
                            for minsuff in minsuff_expl:
                                if minsuff.issubset(suff):
                                    minsuff_suff.append(minsuff)
                                if suff.issubset(minsuff):
                                    minsuff_expl.remove(minsuff)
                                    minsuff_suff.append(suff)
                            if minsuff_suff == [] and suff not in minsuff_expl:
                                minsuff_expl.append(suff)
                        arg_expl.extend(minsuff_expl)

                    elif function == 'Nec':
                        nec_expl = form_expl[0]
                        for suffexpl in form_expl:
                            nec_expl = nec_expl.intersection(suffexpl)
                        arg_expl.extend(nec_expl)
#
            abstr_explanation[str(formula)] = arg_expl

        if function == 'MinSuff' or function == 'Nec':
            return abstr_explanation

    elif expl_type == 'NonAcc':
        formulas = set()
        for arg in abstractAF.arguments:
            for subarg in arg.sub_arguments:
                formulas.add(subarg.conclusion)
        for formula in formulas.difference(accepted_formulas):
            form_arg = argumentation_theory.arguments[formula]
            arg_expl = []
            for arg in form_arg:
                if function == 'NoDefAgainst':
                    arg_expl.extend(get_not_defending(abstractAF, arg, extensions))
                elif function == 'NoDirDefense':
                    arg_expl.extend(get_no_dir_defending(abstractAF, arg, extensions))
                elif function == 'NoSelfDefense':
                    arg_expl.extend(get_no_self_defense(abstractAF, arg, extension))
            abstr_explanation[str(formula)] = arg_expl

    if form == 'Arg':
        return abstr_explanation

    else:
        for expl_form in abstr_explanation:
            explanation = abstr_explanation[expl_form]
            form_expl = []
            for sets in explanation:
                for arg in sets:
                    if form == 'Prem' and arg.premises not in form_expl:
                        form_expl.append(arg.premises)
                    elif form == 'Rule':
                        defrules = arg.defeasible_rules
                        rules = defrules.union(arg.strict_rules)
                        if rules not in form_expl:
                            form_expl.append(rules)
#                    elif form == 'TopRule':
#                        if arg.top_rule != None:
#                            if arg.top_rule not in form_expl:
#                                form_expl.append(arg.top_rule)
                    elif form == 'SubArg' and arg.sub_arguments not in form_expl:
                        form_expl.append(arg.sub_arguments)
                    elif form == 'SubArgConc':
                        subargconc = set()
                        for subarg in arg.sub_arguments:
                            if subarg.conclusion not in subargconc:
                                subargconc.add(subarg.conclusion)
                        form_expl.append(subargconc)
            abstr_explanation[expl_form] = form_expl
        return abstr_explanation


def get_abstr_graph_data(arg_framework):
    '''
    Calculate the data needed for the graphical representation of the argumentation framework

    :param arg_framework: The abstract argumentation framework that needs to be visualized.
    '''
    data_nodes = [{'id': str(argument), 'label': str(argument), 'color': '#6DCDE3'}
                  for argument in arg_framework.arguments]
    data_edges = []

    for defeat in arg_framework.defeats:
        data_edges.append({'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
                           'from': str(defeat.from_argument), 'to': str(defeat.to_argument), 'arrows': 'to'})

    data = {'nodes': data_nodes, 'edges': data_edges}
    return data


def get_str_graph_data(argumentation_theory, ordering_choice):
    '''
    Calculate the data needed for the graphical representation of the argumentation theory and ordering

    :param argumentation_theory: The argumentation_theory that needs to be visualized.
    :param ordering_choice: The chosen ordering, combining both last/weakest link and democratic/elitist.
    '''
    i = 1
    id_arguments = []
    for argument in argumentation_theory.all_arguments:
        id_arguments.append(['A' + str(i), argument])
        i = i + 1
    data_nodes = [{'id': argument[0], 'label': str(argument[1]), 'color': '#6DCDE3'} for argument in id_arguments]
    data_edges = []

    if ordering_choice == 'demlastl':
        ordering = LastLinkDemocraticOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                              argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'elilastl':
        ordering = LastLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                           argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'demweakl':
        ordering = WeakestLinkDemocraticOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                                 argumentation_theory.ordinary_premise_preference_dict)
    elif ordering_choice == 'eliweakl':
        ordering = WeakestLinkElitistOrdering(argumentation_theory.argumentation_system.rule_preference_dict,
                                              argumentation_theory.ordinary_premise_preference_dict)
    else:
        ordering = None

    for defeat in argumentation_theory.recompute_all_defeats(ordering):
        id_a = 0
        id_b = 0
        while id_a == 0 or id_b == 0:
            for argument in id_arguments:
                if argument[1] == defeat.from_argument:
                    id_a = argument[0]
                elif argument[1] == defeat.to_argument:
                    id_b = argument[0]

        data_edges.append({'id': str(id_a) + '-' + str(id_b), 'from': id_a, 'to': id_b, 'arrows': 'to'})

    data = {'nodes': data_nodes, 'edges': data_edges}
    return data