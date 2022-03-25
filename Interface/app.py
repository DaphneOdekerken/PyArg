import dash
import dash_bootstrap_components as dbc

from dash import dcc
from dash import html

import dash.dependencies
import visdcc

from ASPIC.aspic_classes.argumentation_system import ArgumentationSystem
from ASPIC.aspic_classes.argumentation_theory import ArgumentationTheory
from ASPIC.aspic_classes.defeasible_rule import DefeasibleRule
from ASPIC.aspic_classes.orderings.last_link_ordering import LastLinkElitistOrdering, LastLinkDemocraticOrdering
from ASPIC.aspic_classes.literal import Literal
from ASPIC.aspic_classes.ordinary_premise import OrdinaryPremise
from ASPIC.aspic_classes.preference import Preference
from ASPIC.aspic_classes.strict_rule import StrictRule
from ASPIC.aspic_classes.orderings.weakest_link_ordering import WeakestLinkElitistOrdering, \
    WeakestLinkDemocraticOrdering
from ASPIC.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from ASPIC.abstract_argumentation_classes.argument import Argument
from ASPIC.abstract_argumentation_classes.defeat import Defeat
from ASPIC.semantics.get_admissible_sets import get_admissible_sets
from ASPIC.semantics.get_complete_extensions import get_complete_extensions
from ASPIC.semantics.get_grounded_extension import get_grounded_extension
from ASPIC.semantics.get_preferred_extensions import get_preferred_extensions
from ASPIC.semantics.get_ideal_extension import get_ideal_extension
from ASPIC.semantics.get_stable_extensions import get_stable_extensions
from ASPIC.semantics.get_semistable_extensions import get_semistable_extensions
from ASPIC.semantics.get_eager_extension import get_eager_extension

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUMEN])

abstract_setting = html.Div(children=[
    html.Div([
        html.Div([
            html.B('Arguments'),
            html.Br(),
            dcc.Textarea(
                id='abstract-arguments',
                placeholder='Add one argument per line. For example:\n A\n B\n C',
                value='',
                style={'height': 300, 'margin-top': '10px'}, ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.B('Attacks'),
            html.Br(),
            dcc.Textarea(
                id='abstract-attacks',
                placeholder='Add one attack per line. For example: \n (A,B) \n (A,C) \n (C,B)',
                value='',
                style={'height': 300, 'margin-top': '10px'}, ),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(
        [html.Button('Create AF', id='abstrAF-Calc', n_clicks=0)], style={'text-align': 'left', 'margin-left': '10px'}
    ),

    html.Div(id='abstract-argumentation', style={'whiteSpace': 'pre-line'})
])

ASPIC_setting = html.Div(children=[
    html.Div([
        html.Div([
            html.B('Axioms'),
            html.Br(),
            dcc.Textarea(
                id='aspic-axioms',
                placeholder='Add one axiom per line. For examle:\n p \n -q \n ~r',
                value='',
                style={'height': 150, 'margin-top': '10px'}, ),
        ], style={'padding': 10, 'flex': 1, 'margin-left': '10px'}),

        html.Div([
            html.B('Ordinary premises'),
            html.Br(),
            dcc.Textarea(
                id='aspic-ordinary-premises',
                placeholder='Add one ordinary premise per line. For examle:\n p \n -q \n ~r',
                value='',
                style={'height': 150, 'margin-top': '10px'}, ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.B('Ordinary premise preferences', style={'margin-left': '10px'}),
            html.Br(),
            dcc.Textarea(
                id='ordinary-prem-preferences',
                placeholder='Add one preferece between two premises per line. For example:\n p < -q \n -q > ~r',
                value='',
                style={'height': 150, 'margin-left': '10px', 'margin-top': '10px'},
            ),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div([
        html.Div([
            html.B('Strict rules', style={'margin-left': '10px'}),
            html.Br(),
            dcc.Textarea(
                id='aspic-strict-rules',
                placeholder='Add one strict rule per line. For example:\n p->q \n -q -> -r',
                value='',
                style={'height': 150, 'margin-left': '10px', 'margin-top': '10px'},
            ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.B('Defeasible rules'),
            html.Br(),
            dcc.Textarea(
                id='aspic-defeasible-rules',
                placeholder='Add one defeasible rule per line, including the rule name. '
                            'For example:\n d1: p=>q \n d2: -q => -r',
                value='',
                style={'height': 150, 'margin-top': '10px'}, ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.B('Defeasible rule preferences', style={'margin-left': '10px'}),
            html.Br(),
            dcc.Textarea(
                id='defeasible-rule-preferences',
                placeholder='Add one preference between two rules per line. For example:\n d1 < d2',
                value='',
                style={'height': 150, 'margin-left': '10px', 'margin-top': '10px'},
            ),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div([
        html.B('Ordering', style={'margin-left': '10px'}),
        html.Br(),
        html.Div([
            html.Div([
                dcc.RadioItems(
                    options=[
                        {'label': 'None', 'value': 'nochoice'},
                        {'label': 'Democratic', 'value': 'dem'},
                        {'label': 'Elitist', 'value': 'eli'}
                    ],
                    value='nochoice',
                    id='ordering-choice',
                ),
            ], style={'padding': 5, 'flex': 1}),

            html.Div([
                dcc.RadioItems(
                    options=[
                        {'label': 'None', 'value': 'nolink'},
                        {'label': 'Last link', 'value': 'lastl'},
                        {'label': 'Weakest link', 'value': 'weakl'}
                    ],
                    value='nolink',
                    id='ordering-link'
                ),
            ], style={'padding': 5, 'flex': 1}),
        ], style={'display': 'flex', 'flex-direction': 'row', 'margin-left': '10px'}),
    ]),

    html.Div(
        [html.Button('Create AF', id='strAF-Calc', n_clicks=0)], style={'text-align': 'left', 'margin-left': '10px'}
    ),

    html.Div(id='ASPIC-argumentation', style={'whiteSpace': 'pre-line'})
])

abstr_evaluation = html.Div([
    html.Div([
        html.Div([
            html.B('Semantics'),

            dcc.RadioItems(
                options=[
                    {'label': 'Admissible', 'value': 'Adm'},
                    {'label': 'Complete', 'value': 'Cmp'},
                    {'label': 'Grounded', 'value': 'Grd'},
                    {'label': 'Preferred', 'value': 'Prf'},
                    {'label': 'Ideal', 'value': 'Idl'},
                    {'label': 'Stable', 'value': 'Stb'},
                    {'label': 'Semi-stable', 'value': 'Sstb'},
                    {'label': 'Eager', 'value': 'Egr'},
                ],
                value='',
                id='abstr-evaluation-semantics',
                style={'margin-top': '10px'}
            ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.B('Evaluation strategy'),

            dcc.RadioItems(
                options=[
                    {'label': 'Credulous', 'value': 'Cred'},
                    {'label': 'Skeptical', 'value': 'Skep'}
                ],
                value='',
                id='abstr-evaluation-strategy',
                style={'margin-top': '10px'}
            ),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(
        [html.Button('Evaluate AF', id='abstrAF-Eval', n_clicks=0)], style={'text-align': 'left', 'margin-left': '10px'}
    ),

    html.Div(id='abstrAF-evaluation', style={'whiteSpace': 'pre-line'}),
])

str_evaluation = html.Div([
    html.Div([
        html.Div([
            html.B('Semantics'),

            dcc.RadioItems(
                options=[
                    {'label': 'Admissible', 'value': 'Adm'},
                    {'label': 'Complete', 'value': 'Cmp'},
                    {'label': 'Grounded', 'value': 'Grd'},
                    {'label': 'Preferred', 'value': 'Prf'},
                    {'label': 'Ideal', 'value': 'Idl'},
                    {'label': 'Stable', 'value': 'Stb'},
                    {'label': 'Semi-stable', 'value': 'Sstb'},
                    {'label': 'Eager', 'value': 'Egr'},
                ],
                value='',
                id='str-evaluation-semantics',
                style={'margin-top': '10px'}
            ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.B('Evaluation strategy'),

            dcc.RadioItems(
                options=[
                    {'label': 'Credulous', 'value': 'Cred'},
                    {'label': 'Weakly Skeptical', 'value': 'WSkep'},
                    {'label': 'Skeptical', 'value': 'Skep'}
                ],
                value='',
                id='str-evaluation-strategy',
                style={'margin-top': '10px'}
            ),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(
        [html.Button('Evaluate AF', id='strAF-Eval', n_clicks=0)], style={'text-align': 'left', 'margin-left': '10px'}
    ),

    html.Div(id='strAF-evaluation', style={'whiteSpace': 'pre-line'}),
])


def get_argumentation_framework(arguments, attacks):
    """
    Calculate the abstract argumentation theory from the given arguments and attacks between them. 

    :param arguments: The provided arguments.
    :param attacks: The provided attacks. 
    """
    arg_list = [Argument(arg) for arg in arguments.replace(",", "").split()]
    defeat_list = []

    for attack in attacks.splitlines():
        att_list = attack.replace(" ", "").replace(")", "").replace("(", "").split(",")
        if att_list[0] == "" or att_list[1] == "":
            continue
        attacker = Argument(att_list[0])
        attacked = Argument(att_list[1])
        defeat_list.append(Defeat(attacker, attacked))

    arg_framework = AbstractArgumentationFramework('AF', arg_list, defeat_list)
    return arg_framework


def get_argumentation_theory(axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences, ordering):
    """
    Calculate the argumentation theory from the axioms, ordinary premises, strict and defeasible rules, premise and 
    rule preference and the given ordering

    :param axioms: The provided axioms (premises that cannot be attacked).
    :param ordinary: The ordinary premises (premises that can be questioned).
    :param strict: The provided strict rules (rules that cannot be attacked).
    :param defeasible: The defeasible rules (rules that can be questioned).
    :param premise_preferences: The preferences over the ordinary premises.
    :param rule_preferences: The preferences over the defeasible rules.
    :param ordering: The chosen ordering, combining both last/weakest link and democratic/elitist.
    """
    arg_sys = ArgumentationSystem({}, {}, [], [])
    arg_theory = ArgumentationTheory(arg_sys, [], [])
    error_statement = ''

    axiom_list = axioms.split()
    ordinary_list = ordinary.split()
    strrule_sep = []
    for strr in strict.splitlines():
        strrule_sep += strr.replace(" ", "").replace("->", ",").split(",")
    strrule_list = []
    for strrules in strrule_sep:
        strrule_list.append(strrules)
    defrule_sep = []
    for defr in defeasible.splitlines():
        defrule_sep += defr.replace(" ", "").replace("=>", ",").replace(":", ",").split(",")
    defrule_list = []
    for defrules in defrule_sep:
        defrule_list.append(defrules)
    literal_str_list = []
    for ax in axiom_list:
        literal_str_list.append(ax)
    for op in ordinary_list:
        literal_str_list.append(op)
    for strr in strrule_list:
        literal_str_list.append(strr)
    for defr in defrule_list:
        literal_str_list.append(defr)

    literal_str_list += ['-' + literal_str for literal_str in literal_str_list]
    literal_str_list += ['~' + literal_str for literal_str in literal_str_list]

    literal_str_list = list(dict.fromkeys(literal_str_list))

    language = {literal_str: Literal(literal_str, literal_str + ' is present', literal_str + ' is absent')
                for literal_str in literal_str_list}
    contraries = {literal_str: [] for literal_str in language.keys()}
    for literal_str in language.keys():
        if literal_str[0] in ('~', '-'):
            contraries[literal_str].append(language[literal_str[1:]])
        else:
            contraries[literal_str].append(language['-' + literal_str])

    strrule_sep = strict.replace(" ", "").splitlines()
    strrules = []
    defrule_sep = defeasible.replace(" ", "").splitlines()
    defrules = []

    i = 1
    for rule in strrule_sep:
        if rule.find('=>') != -1:
            return arg_theory, html.Div([html.H4('Error', style={'color': 'red'}),
                                         'a strict rule contains a defeasible rule (i.e., the arrow =>)'])
        sep_antcon = rule.split("->")
        ant_str_list = sep_antcon[0].split(",")
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
        sep_antcon = rule.split("=>")
        rule_id = sep_antcon[0].split(":")[0]
        try:
            ant_str_list = sep_antcon[0].split(":")[1].split(",")
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

    for ordinary_premise in ordinary_premises:
        ordinary_premise.__class__ = OrdinaryPremise

    arg_theory = ArgumentationTheory(arg_sys, axioms, ordinary_premises)

    premise_preference_list = premise_preferences.replace(" ", "").splitlines()
    rule_preference_list = rule_preferences.replace(" ", "").splitlines()
    for preference in premise_preference_list:
        if preference.find('<') != -1:
            pref_items = preference.rsplit('<')
            arg_theory.add_ordinary_premise_preference(Preference(language[pref_items[0]], '<',
                                                                  language[pref_items[1]]))
        elif preference.find('>') != -1:
            pref_items = preference.rsplit('>')
            arg_theory.add_ordinary_premise_preference(Preference(language[pref_items[1]], '<',
                                                                  language[pref_items[0]]))
    for preference in rule_preference_list:
        if preference.find('<') != -1:
            pref_items = preference.rsplit('<')
            for def_rule in defrules:
                if str(def_rule.id) == pref_items[0]:
                    weaker_rule = def_rule
            for def_rule in defrules:
                if str(Literal.from_defeasible_rule(def_rule)) == pref_items[1]:
                    stronger_rule = def_rule
            arg_theory.argumentation_system.add_rule_preference(Preference(weaker_rule, '<', stronger_rule))
        elif preference.find('>') != -1:
            pref_items = preference.rsplit('>')
            for def_rule in defrules:
                if str(def_rule.id) == pref_items[1]:
                    weaker_rule = def_rule
            for def_rule in defrules:
                if str(Literal.from_defeasible_rule(def_rule)) == pref_items[0]:
                    stronger_rule = def_rule
            arg_theory.argumentation_system.add_rule_preference(Preference(weaker_rule, '<', stronger_rule))

    return arg_theory, error_statement


def get_abstr_extensions(arg_framework, semantics):
    """
    Calculate the set of extensions from the given abstract argumentation framework and chosen semantics

    :param arg_framework: The abstract argumentation framework.
    :param semantics: The chosen semantics.
    """
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
    """
    Calculate the set of extensions from the given argumentation theory, type of ordering and semantics

    :param argumentation_theory: The argumentation theory.
    :param semantics: The chosen semantics.
    :param ordering_choice: The chosen ordering, combining both last/weakest link and democratic/elitist.
    """
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

    abstractAF = AbstractArgumentationFramework.from_argumentation_theory('af', argumentation_theory, ordering)

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
    """
    Calculate the set of accepted formulas from a set of extensions (sets of arguments) and evaluation strategy

    :param extensions: The extensions (sets of collectively accepted arguments).
    :param strategy: The evaluation strategy (e.g., skeptical or credulous).
    """
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


def get_abstr_graph_data(arg_framework):
    """
    Calculate the data needed for the graphical representation of the argumentation framework

    :param arg_framework: The abstract argumentation framework that needs to be visualized.
    """
    data_nodes = [{'id': str(argument), 'label': str(argument), 'color': '#6DCDE3'}
                  for argument in arg_framework.arguments]
    data_edges = []

    for defeat in arg_framework.defeats:
        data_edges.append({'id': str(defeat.from_argument) + '-' + str(defeat.to_argument),
                           'from': str(defeat.from_argument), 'to': str(defeat.to_argument), 'arrows': 'to'})

    data = {'nodes': data_nodes, 'edges': data_edges}
    return data


def get_str_graph_data(argumentation_theory, ordering_choice):
    """
    Calculate the data needed for the graphical representation of the argumentation theory and ordering

    :param argumentation_theory: The argumentation_theory that needs to be visualized.
    :param ordering_choice: The chosen ordering, combining both last/weakest link and democratic/elitist.
    """
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


layout_abstract = html.Div([
    html.Div([
        html.Div([
            dbc.CardHeader(
                dbc.Button(
                    "Abstract Argumentation Setting",
                    style={'color': '#152A47',
                           'text-align': 'left',
                           'background-color': '#7BE7FF',
                           'border-color': '#7BE7FF',
                           'width': '100%'},
                    id="abstr-arg-setting-button",
                )
            ),
            dbc.Collapse(
                dbc.CardBody(abstract_setting),
                id="abstr-arg-setting-collapse", is_open=False
            ),

            dbc.CardHeader(
                dbc.Button(
                    "Evaluation",
                    style={'color': '#152A47',
                           'text-align': 'left',
                           'background-color': '#7BE7FF',
                           'border-color': '#7BE7FF',
                           'width': '100%'},
                    id="abstr-evaluation-button",
                )
            ),
            dbc.Collapse(
                dbc.CardBody(abstr_evaluation),
                id="abstr-evaluation-collapse", is_open=False
            ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            visdcc.Network(data={'nodes': [], 'edges': []},
                           id='abstrnet',
                           options=dict(height='600px'),
                           style={'border-radius': '8px',
                                  'border': '2px solid #152A47',
                                  'margin-right': '25px'}),
            html.Div([
                html.Div(
                    id='abstr-output',
                    style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                html.Div(
                    id='abstr-evaluation',
                    style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                )
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'})
])

layout_ASPIC = html.Div([
    html.Div([
        html.Div([
            dbc.CardHeader(
                dbc.Button(
                    "ASPIC Argumentation Setting",
                    style={'color': '#152A47',
                           'text-align': 'left',
                           'background-color': '#7BE7FF',
                           'border-color': '#7BE7FF',
                           'width': '100%'},
                    id="str-arg-setting-button",
                )
            ),
            dbc.Collapse(
                dbc.CardBody(ASPIC_setting),
                id="str-arg-setting-collapse", is_open=False
            ),

            dbc.CardHeader(
                dbc.Button(
                    "Evaluation",
                    style={'color': '#152A47',
                           'text-align': 'left',
                           'background-color': '#7BE7FF',
                           'border-color': '#7BE7FF',
                           'width': '100%'},
                    id="str-evaluation-button",
                )
            ),
            dbc.Collapse(
                dbc.CardBody(str_evaluation),
                id="str-evaluation-collapse", is_open=False
            ),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            visdcc.Network(data={'nodes': [], 'edges': []},
                           id='strnet',
                           options=dict(height='600px'),
                           style={'border-radius': '8px',
                                  'border': '2px solid #152A47',
                                  'margin-right': '25px'}),
            html.Div([
                html.Div(
                    id='str-output',
                    style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                html.Div(
                    id='str-evaluation',
                    style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                )
            ], style={'display': 'flex', 'flex-direction': 'row'})
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'})
])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('PyASPIC', className='header-title'),
        ], style={'padding': 10, 'flex': 5}),
        
        html.Div([
            html.Img(src=app.get_asset_url('UU_logo_2021_EN_RGB.png'),
                     style={'border': 'none', 'width': '30%', 'max-width': '500px', 'align': 'right',
                            'margin-right': '20px'}),
            html.P('Daphne Odekerken and AnneMarie Borg', style={'margin-right': '25px'}),
        ], style={'padding': 10, 'flex': 2, 'text-align': 'right'}),
    ], style = {'display': 'flex', 'flex-direction': 'row'}),

        

    html.Div([
        dcc.RadioItems(
            id='arg-choice',
            options=[
                {'label': 'Abstract', 'value': 'Abstr'},
                {'label': 'ASPIC+', 'value': 'ASPIC'}
            ],
            value='',
            labelStyle={'display': 'inline-block', 'margin-left': '20px'}),
    ]),
    html.Div(id='arg-layout')
])

app.validation_layout = html.Div([
    abstract_setting,
    ASPIC_setting,
    abstr_evaluation,
    str_evaluation
])


@app.callback(
    dash.dependencies.Output('arg-layout', 'children'),
    [dash.dependencies.Input('arg-choice', 'value')]
)
def setting_choice(choice):
    if choice == 'Abstr':
        return layout_abstract
    elif choice == 'ASPIC':
        return layout_ASPIC


@app.callback(
    dash.dependencies.Output("abstr-arg-setting-collapse", "is_open"),
    [dash.dependencies.Input("abstr-arg-setting-button", "n_clicks")],
    [dash.dependencies.State("abstr-arg-setting-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output("abstr-evaluation-collapse", "is_open"),
    [dash.dependencies.Input("abstr-evaluation-button", "n_clicks")],
    [dash.dependencies.State("abstr-evaluation-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output("str-arg-setting-collapse", "is_open"),
    [dash.dependencies.Input("str-arg-setting-button", "n_clicks")],
    [dash.dependencies.State("str-arg-setting-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output("str-evaluation-collapse", "is_open"),
    [dash.dependencies.Input("str-evaluation-button", "n_clicks")],
    [dash.dependencies.State("str-evaluation-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstr-output', 'children'),
    dash.dependencies.Output('abstrnet', 'data'),
    dash.dependencies.Input('abstrAF-Calc', 'n_clicks'),
    dash.dependencies.Input('abstract-arguments', 'value'),
    dash.dependencies.Input('abstract-attacks', 'value'),
    prevent_initial_call=True
)
def create_AF(click, arguments, attacks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'abstrAF-Calc' in changed_id:
        arg_framework = get_argumentation_framework(arguments, attacks)
        data = get_abstr_graph_data(arg_framework)
        admissible = get_abstr_extensions(arg_framework, 'Adm')
        cmp_extension = get_abstr_extensions(arg_framework, 'Cmp')
        grd_extension = get_abstr_extensions(arg_framework, 'Grd')
        prf_extension = get_abstr_extensions(arg_framework, 'Prf')
        idl_extension = get_abstr_extensions(arg_framework, 'Idl')
        stb_extension = get_abstr_extensions(arg_framework, 'Stb')
        sstb_extension = get_abstr_extensions(arg_framework, 'Sstb')
        egr_extension = get_abstr_extensions(arg_framework, 'Egr')
        return html.Div([html.H4('The arguments of the AF:', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(arg_framework.arguments))]), data
    else:
        data = {'nodes': [], 'edges': []}
        return 'No argumentation setting was provided', data


@app.callback(
    dash.dependencies.Output('abstr-evaluation', 'children'),
    dash.dependencies.Input('abstrAF-Eval', 'n_clicks'),
    dash.dependencies.Input('abstract-arguments', 'value'),
    dash.dependencies.Input('abstract-attacks', 'value'),
    dash.dependencies.Input('abstr-evaluation-semantics', 'value'),
    dash.dependencies.Input('abstr-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_abstrAF(click, arguments, attacks, semantics, strategy):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Eval' in changed_id:
        arg_framework = get_argumentation_framework(arguments, attacks)
        frozen_extensions = get_abstr_extensions(arg_framework, semantics)
        accepted = set()
        if semantics != 'Grd':
            extension = [set(frozen_extension) for frozen_extension in frozen_extensions]
            if strategy == 'Skep':
                accepted = set.intersection(*extension)
            elif strategy == 'Cred':
                accepted = set.union(*extension)
        elif semantics == 'Grd':
            extension = frozen_extensions
            accepted = extension
        return html.Div([html.H4('The extension(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(extension)),
                         html.H4('The accepted argument(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(accepted))])


@app.callback(
    dash.dependencies.Output('ordering-link', 'children'),
    dash.dependencies.Output('ordering-link', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
)
def choose_ordering(choice):
    if choice == 'nochoice':
        options = [{'label': 'None', 'value': 'nolink'},
                   {'label': 'Last link', 'value': 'lastl', 'disabled': True},
                   {'label': 'Weakest link', 'value': 'weakl', 'disabled': True}
                   ]
        return options, 'nolink'
    else:
        options = [{'label': 'None', 'value': 'nolink', 'state': 'disabled'},
                   {'label': 'Last link', 'value': 'lastl'},
                   {'label': 'Weakest link', 'value': 'weakl'}
                   ]
        return options, 'lastl'


@app.callback(
    dash.dependencies.Output('str-output', 'children'),
    dash.dependencies.Output('strnet', 'data'),
    dash.dependencies.Input('strAF-Calc', 'n_clicks'),
    dash.dependencies.Input('aspic-axioms', 'value'),
    dash.dependencies.Input('aspic-ordinary-premises', 'value'),
    dash.dependencies.Input('aspic-strict-rules', 'value'),
    dash.dependencies.Input('aspic-defeasible-rules', 'value'),
    dash.dependencies.Input('ordinary-prem-preferences', 'value'),
    dash.dependencies.Input('defeasible-rule-preferences', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
    dash.dependencies.Input('ordering-link', 'value'),
    prevent_initial_call=True
)
def create_AT(click, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences, choice, link):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Calc' in changed_id:
        ordering = choice + link
        arg_theory, error_message = get_argumentation_theory(axioms, ordinary, strict, defeasible, premise_preferences,
                                                             rule_preferences, ordering)
        data = get_str_graph_data(arg_theory, ordering)
        if error_message != '':
            return error_message, data
        else:
            return html.Div([html.H4('The generated argument(s):', style={'color': '#152A47'}),
                             html.H6('\n {}'.format(arg_theory.all_arguments))]), data

    else:
        data = {'nodes': [], 'edges': []}
        return 'No argumentation setting was provided', data


@app.callback(
    dash.dependencies.Output('str-evaluation', 'children'),
    dash.dependencies.Input('strAF-Eval', 'n_clicks'),
    dash.dependencies.Input('aspic-axioms', 'value'),
    dash.dependencies.Input('aspic-ordinary-premises', 'value'),
    dash.dependencies.Input('aspic-strict-rules', 'value'),
    dash.dependencies.Input('aspic-defeasible-rules', 'value'),
    dash.dependencies.Input('ordinary-prem-preferences', 'value'),
    dash.dependencies.Input('defeasible-rule-preferences', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
    dash.dependencies.Input('ordering-link', 'value'),
    dash.dependencies.Input('str-evaluation-semantics', 'value'),
    dash.dependencies.Input('str-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_strAF(click, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences, choice, link,
                   semantics, strategy):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Eval' in changed_id:
        ordering = choice + link
        arg_theory, error_message = get_argumentation_theory(axioms, ordinary, strict, defeasible, premise_preferences,
                                                             rule_preferences, ordering)
        if error_message != '':
            return error_message
        frozen_extensions = get_str_extensions(arg_theory, semantics, ordering)
        accepted = set()
        if semantics != 'Grd':
            extension = [set(frozen_extension) for frozen_extension in frozen_extensions]
            accepted = get_accepted_formulas(extension, strategy)
        elif semantics == 'Grd':
            extension = frozen_extensions
            accepted = extension
        return html.Div([html.H4('The extension(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(extension)),
                         html.H4('The accepted formula(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(accepted))])


if __name__ == '__main__':
    app.run_server(debug=True)
