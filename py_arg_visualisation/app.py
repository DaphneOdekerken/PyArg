import dash
import dash_bootstrap_components as dbc

from dash import dcc
from dash import html
from dash.exceptions import PreventUpdate

import dash.dependencies
import visdcc

from py_arg.aspic_classes.argumentation_system import ArgumentationSystem
from py_arg.aspic_classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic_classes.defeasible_rule import DefeasibleRule
from py_arg.aspic_classes.orderings.last_link_ordering import LastLinkElitistOrdering, LastLinkDemocraticOrdering
from py_arg.aspic_classes.literal import Literal
from py_arg.aspic_classes.ordinary_premise import OrdinaryPremise
from py_arg.aspic_classes.preference import Preference
from py_arg.aspic_classes.strict_rule import StrictRule
from py_arg.aspic_classes.orderings.weakest_link_ordering import WeakestLinkElitistOrdering, \
    WeakestLinkDemocraticOrdering
from py_arg.abstract_argumentation_classes.abstract_argumentation_framework import AbstractArgumentationFramework
from py_arg.abstract_argumentation_classes.argument import Argument
from py_arg.abstract_argumentation_classes.defeat import Defeat
from py_arg.semantics.get_admissible_sets import get_admissible_sets
from py_arg.semantics.get_complete_extensions import get_complete_extensions
from py_arg.semantics.get_grounded_extension import get_grounded_extension
from py_arg.semantics.get_preferred_extensions import get_preferred_extensions
from py_arg.semantics.get_ideal_extension import get_ideal_extension
from py_arg.semantics.get_stable_extensions import get_stable_extensions
from py_arg.semantics.get_semistable_extensions import get_semistable_extensions
from py_arg.semantics.get_eager_extension import get_eager_extension
from py_arg.explanation.defending import get_defending, get_dir_defending
from py_arg.explanation.not_defending import get_not_defending, get_no_self_defense, get_no_dir_defending
from py_arg.explanation.suff_nec import get_suff_nec

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LUMEN])
server = app.server

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
                placeholder='Add one axiom per line. For example:\n p \n -q \n ~r',
                value='',
                style={'height': 150, 'margin-top': '10px'}, ),
        ], style={'padding': 10, 'flex': 1, 'margin-left': '10px'}),

        html.Div([
            html.B('Ordinary premises'),
            html.Br(),
            dcc.Textarea(
                id='aspic-ordinary-premises',
                placeholder='Add one ordinary premise per line. For example:\n p \n -q \n ~r',
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
                    inputStyle={'margin-right': '6px'}
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
                    id='ordering-link',
                    inputStyle={'margin-right': '6px'}
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
                style={'margin-top': '10px'},
                inputStyle={'margin-right': '6px'}
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
                style={'margin-top': '10px'},
                inputStyle={'margin-right': '6px'}
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
                style={'margin-top': '10px'},
                inputStyle={'margin-right': '6px'}
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
                style={'margin-top': '10px'},
                inputStyle={'margin-right': '6px'}
            ),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(
        [html.Button('Evaluate AF', id='strAF-Eval', n_clicks=0)], style={'text-align': 'left', 'margin-left': '10px'}
    ),

    html.Div(id='strAF-evaluation', style={'whiteSpace': 'pre-line'}),
])

abstr_explanation = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.B('Type'),

                dcc.RadioItems(
                    options=[
                        {'label': 'Acceptance', 'value': 'Acc'},
                        {'label': 'Non-Acceptance', 'value': 'NonAcc'}
                    ],
                    value='',
                    id='abstr-explanation-type',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ]),

            html.Div([
                html.B('Strategy'),

                dcc.RadioItems(
                    options=[
                        {'label': 'Credulous', 'value': 'Cred'},
                        {'label': 'Skeptical', 'value': 'Skep'}
                    ],
                    value='',
                    id='abstr-explanation-strategy',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'margin-top': '20px'}),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.B('Explanation function'),

            dcc.RadioItems(
                id='abstr-explanation-function',
                style={'margin-top': '10px'},
                inputStyle={'margin-right': '6px'}
            ),
        ], style={'padding': 10, 'flex': 1}),

    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(
        [html.Button('Derive Explanations', id='abstrAF-Expl', n_clicks=0)], style={'text-align': 'left',
                                                                                    'margin-left': '10px'}
    ),

    html.Div(id='abstrAF-explanation', style={'whiteSpace': 'pre-line'}),
])

str_explanation = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.B('Type'),

                dcc.RadioItems(
                    options=[
                        {'label': 'Acceptance', 'value': 'Acc'},
                        {'label': 'Non-Acceptance', 'value': 'NonAcc'}
                    ],
                    value='',
                    id='str-explanation-type',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ]),

            html.Div([
                html.B('Strategy'),

                dcc.RadioItems(
                    options=[
                        {'label': 'Credulous', 'value': 'Cred'},
                        {'label': 'Skeptical', 'value': 'Skep'}
                    ],
                    value='',
                    id='str-explanation-strategy',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'margin-top': '20px'}),
        ], style={'padding': 10, 'flex': 1}),

        html.Div([
            html.Div([
                html.B('Explanation function'),

                dcc.RadioItems(

                    id='str-explanation-function',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ]),

            html.Div([
                html.B('Explanation form'),

                dcc.RadioItems(
                    options=[
                        {'label': 'Argument', 'value': 'Arg'},
                        {'label': 'Premises', 'value': 'Prem'},
                        {'label': 'Rules', 'value': 'Rule'},
                        {'label': 'Sub-arguments', 'value': 'SubArg'},
                        {'label': 'Sub-argument conclusions', 'value': 'SubArgConc'}
                    ],
                    id='str-explanation-form',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'margin-top': '20px'}),

        ], style={'padding': 10, 'flex': 1})

    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div(
        [html.Button('Derive Explanations', id='strAF-Expl', n_clicks=0)], style={'text-align': 'left',
                                                                                  'margin-left': '10px'}
    ),

    html.Div(id='strAF-explanation', style={'whiteSpace': 'pre-line'}),
])

expl_function_options = {
    'Acc': ['Defending', 'DirDefending', 'Suff', 'MinSuff', 'Nec'],
    'NonAcc': ['NoDefAgainst', 'NoDirDefense', 'NoSelfDefense']
}


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


def get_abstr_explanations(arg_framework, semantics, extensions, accepted, function, expl_type, strategy):
    """
    Calculate, for each argument, the explanations, given the function, type and strategy.
    
    :param arg_framework: The argumentation framework the explanation has to be calculated from.
    :param semantics: The semantics used to determine (non-)acceptance.
    :param extensions: The sets of accepted arguments in arg_framework, based on semantics.
    :param accepted: The arguments that are considered accepted given the extensions and strategy.
    :param function: The explanation function, to determine the content of the explanation.
    :param expl_type: The explanation type, to determine acceptance/non-acceptance explanation.
    :param strategy: The strategy of the explanation, whether credulous or skeptical reasoning. 
    :return: A dictionary with for each (non-)accepted argument its explanation, given the parameters. 
    """
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
    """
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

            dbc.CardHeader(
                dbc.Button(
                    "Explanation",
                    style={'color': '#152A47',
                           'text-align': 'left',
                           'background-color': '#7BE7FF',
                           'border-color': '#7BE7FF',
                           'width': '100%'},
                    id="abstr-explanation-button",
                )
            ),
            dbc.Collapse(
                dbc.CardBody(abstr_explanation),
                id="abstr-explanation-collapse", is_open=False
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
                html.Div([
                    html.Div(
                        id='abstr-output',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                    html.Div(
                        id='abstr-evaluation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    ),

                    html.Div(
                        id='abstr-explanation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    )
                ], style={'display': 'flex', 'flex-direction': 'row'}),

                html.Div([
                    html.Div(
                        id='abstrnet-output',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                    html.Div(
                        id='abstrnet-evaluation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    ),

                    html.Div(
                        id='abstrnet-explanation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    )

                ], style={'display': 'flex', 'flex-direction': 'row'})
            ])
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

            dbc.CardHeader(
                dbc.Button(
                    "Explanation",
                    style={'color': '#152A47',
                           'text-align': 'left',
                           'background-color': '#7BE7FF',
                           'border-color': '#7BE7FF',
                           'width': '100%'},
                    id="str-explanation-button",
                )
            ),
            dbc.Collapse(
                dbc.CardBody(str_explanation),
                id="str-explanation-collapse", is_open=False
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
                html.Div([
                    html.Div(
                        id='str-output',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                    html.Div(
                        id='str-evaluation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    ),

                    html.Div(
                        id='str-explanation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    )
                ], style={'display': 'flex', 'flex-direction': 'row'}),

                html.Div([
                    html.Div(
                        id='strnet-output',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                    html.Div(
                        id='strnet-evaluation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    ),

                    html.Div(
                        id='strnet-explanation',
                        style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                    )

                ], style={'display': 'flex', 'flex-direction': 'row'})
            ])
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flex-direction': 'row'})
])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('PyArg', className='header-title'),
        ], style={'padding': 10, 'flex': 5}),

        html.Div([
            html.Img(src=app.get_asset_url('UU_logo_2021_EN_RGB.png'),
                     style={'border': 'none', 'width': '30%', 'max-width': '500px', 'align': 'right',
                            'margin-right': '20px'}),
            html.P('Daphne Odekerken and AnneMarie Borg', style={'margin-right': '25px'}),
        ], style={'padding': 10, 'flex': 2, 'text-align': 'right'}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    html.Div([
        dcc.RadioItems(
            id='arg-choice',
            options=[
                {'label': 'Abstract', 'value': 'Abstr'},
                {'label': 'ASPIC+', 'value': 'ASPIC'}
            ],
            value='',
            labelStyle={'display': 'inline-block', 'margin-left': '20px'},
            inputStyle={'margin-right': '6px'}),
    ]),
    html.Div(id='arg-layout')
])

app.validation_layout = html.Div([
    abstract_setting,
    ASPIC_setting,
    abstr_evaluation,
    str_evaluation,
    abstr_explanation
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
    dash.dependencies.Output("abstr-explanation-collapse", "is_open"),
    [dash.dependencies.Input("abstr-explanation-button", "n_clicks")],
    [dash.dependencies.State("abstr-explanation-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('abstr-explanation-function', 'options'),
    [dash.dependencies.Input('abstr-explanation-type', 'value')],
    prevent_initial_call=True
)
def setting_choice(choice):
    return [{'label': i, 'value': i} for i in expl_function_options[choice]]


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
    dash.dependencies.Output("str-explanation-collapse", "is_open"),
    [dash.dependencies.Input("str-explanation-button", "n_clicks")],
    [dash.dependencies.State("str-explanation-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    dash.dependencies.Output('str-explanation-function', 'options'),
    [dash.dependencies.Input('str-explanation-type', 'value')],
    prevent_initial_call=True
)
def setting_choice(choice):
    return [{'label': i, 'value': i} for i in expl_function_options[choice]]


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
                         html.H6('\n {}'.format(str(extension).replace('set()', '{}'))),
                         html.H4('The accepted argument(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(str(accepted).replace('set()', '{}')))])


@app.callback(
    dash.dependencies.Output('abstr-explanation', 'children'),
    dash.dependencies.Input('abstrAF-Expl', 'n_clicks'),
    dash.dependencies.Input('abstract-arguments', 'value'),
    dash.dependencies.Input('abstract-attacks', 'value'),
    dash.dependencies.Input('abstr-evaluation-semantics', 'value'),
    dash.dependencies.Input('abstr-explanation-function', 'value'),
    dash.dependencies.Input('abstr-explanation-type', 'value'),
    dash.dependencies.Input('abstr-explanation-strategy', 'value'),
    prevent_initial_call=True
)
def derive_abstrExpl(click, arguments, attacks, semantics, function, expltype, strategy):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Expl' in changed_id:
        if semantics == '':
            return html.Div([html.H4('Error', style={'color': 'red'}),
                             'Choose a semantics under "Evaluation" before deriving explanations.'])
        else:
            arg_framework = get_argumentation_framework(arguments, attacks)
            output_str = ''
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
            explanations = get_abstr_explanations(arg_framework, semantics, extension, accepted, function, expltype,
                                                  strategy)
            return html.Div([html.H4('The Explanation(s):', style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(explanations).replace('set()', '{}')))])


@app.callback(
    dash.dependencies.Output('abstrnet-output', 'children'),
    dash.dependencies.Output('abstrnet-evaluation', 'children'),
    dash.dependencies.Output('abstrnet-explanation', 'children'),
    dash.dependencies.Input('abstrnet', 'selection'),
    dash.dependencies.Input('abstract-arguments', 'value'),
    dash.dependencies.Input('abstract-attacks', 'value'),
    dash.dependencies.Input('abstr-evaluation-semantics', 'value'),
    dash.dependencies.Input('abstr-evaluation-strategy', 'value'),
    dash.dependencies.Input('abstr-explanation-function', 'value'),
    dash.dependencies.Input('abstr-explanation-type', 'value'),
    prevent_initial_call=True
)
def interactive_abstr_graph(selection, arguments, attacks, semantics, strategy, function, expltype):
    while selection is not None:
        arg_framework = get_argumentation_framework(arguments, attacks)
        for arg in arg_framework.arguments:
            if str(arg) == str(selection['nodes'][0]):
                argument = arg
        arg_ext = []
        output_arg = html.Div(
            [html.H4('The selected argument:', style={'color': '#152A47'}), html.H6('{}'.format(str(argument)))])
        output_accept = ''
        expl_output = ''
        output_evaluation = ''
        if semantics != '':
            frozen_extensions = get_abstr_extensions(arg_framework, semantics)
            if strategy != '':
                skep_accept = False
                cred_accept = False
                if semantics != 'Grd':
                    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
                    skep_accepted = set.intersection(*extensions)
                    cred_accepted = set.union(*extensions)
                    for ext in extensions:
                        if argument in ext:
                            arg_ext.append(ext)
                    if arg_ext == extensions:
                        skep_accept = True
                    if arg_ext != []:
                        cred_accept = True
                elif semantics == 'Grd':
                    extensions = frozen_extensions
                    if argument in extensions:
                        arg_ext.append(extensions)
                        skep_accepted = extensions
                        cred_accepted = extensions
                        skep_accept = True
                        cred_accept = True
                if skep_accept:
                    output_accept += str(argument) + ' is skeptically and credulously accepted.'
                    if function is not None and expltype == 'Acc':
                        skep_expla = get_abstr_explanations(arg_framework, semantics, extensions, skep_accepted,
                                                            function, expltype, 'Skep')
                        cred_expla = get_abstr_explanations(arg_framework, semantics, extensions, cred_accepted,
                                                            function, expltype, 'Cred')
                        expl_output = html.Div([html.H4(
                            'The skeptical acceptance explanation for {}:'.format(str(argument)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()', '{}'))), html.H4(
                                'The credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no non-acceptance explanation for argument {}, since it is '
                                                'skeptically accepted.'.format(
                                                    argument)])
                elif cred_accept:
                    output_accept += str(argument) + ' is credulously but not skeptically accepted.'
                    if function is not None and expltype == 'Acc':
                        cred_expla = get_abstr_explanations(arg_framework, semantics, extensions, cred_accepted,
                                                            function, expltype, 'Cred')
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(argument)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        skep_expla = get_abstr_explanations(arg_framework, semantics, extensions, skep_accepted,
                                                            function, expltype, 'Skep')
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(argument)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()', '{}')))])
                elif skep_accept == False and cred_accept == False:
                    output_accept += str(argument) + ' is neither  credulously nor skeptically accepted.'
                    if function is not None and expltype == 'NonAcc':
                        skep_expla = get_abstr_explanations(arg_framework, semantics, extensions, skep_accepted,
                                                            function, expltype, 'Skep')
                        cred_expla = get_abstr_explanations(arg_framework, semantics, extensions, cred_accepted,
                                                            function, expltype, 'Cred')
                        expl_output = html.Div([html.H4(
                            'The not skeptical acceptance explanation for {}:'.format(str(argument)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()', '{}'))), html.H4(
                                'The not credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()', '{}')))])
                    elif function is not None and expltype == 'Acc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no acceptance explanation for argument {}, since it is not '
                                                'credulously accepted.'.format(
                                                    argument)])
            output_evaluation = html.Div(
                [html.H4('The extensions with argument {}:'.format(str(argument)), style={'color': '#152A47'}),
                 html.H6('{}'.format(arg_ext)), html.H6('{}'.format(output_accept))])
        return output_arg, output_evaluation, expl_output
    raise PreventUpdate


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
                         html.H6('\n {}'.format(str(extension).replace('set()','{}'))),
                         html.H4('The accepted formula(s):', style={'color': '#152A47'}),
                         html.H6('\n {}'.format(str(accepted).replace('set()','{}')))])


@app.callback(
    dash.dependencies.Output('str-explanation', 'children'),
    dash.dependencies.Input('strAF-Expl', 'n_clicks'),
    dash.dependencies.Input('aspic-axioms', 'value'),
    dash.dependencies.Input('aspic-ordinary-premises', 'value'),
    dash.dependencies.Input('aspic-strict-rules', 'value'),
    dash.dependencies.Input('aspic-defeasible-rules', 'value'),
    dash.dependencies.Input('ordinary-prem-preferences', 'value'),
    dash.dependencies.Input('defeasible-rule-preferences', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
    dash.dependencies.Input('ordering-link', 'value'),
    dash.dependencies.Input('str-evaluation-semantics', 'value'),
    dash.dependencies.Input('str-explanation-function', 'value'),
    dash.dependencies.Input('str-explanation-type', 'value'),
    dash.dependencies.Input('str-explanation-strategy', 'value'),
    dash.dependencies.Input('str-explanation-form', 'value'),
    prevent_initial_call=True
)
def derive_strExpl(click, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences, choice, link,
                   semantics, function, expltype, strategy, form):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'AF-Expl' in changed_id:
        if semantics == '':
            return html.Div([html.H4('Error', style={'color': 'red'}),
                             'Choose a semantics under "Evaluation" before deriving explanations.'])
        else:
            ordering = choice + link
            arg_theory, error_message = get_argumentation_theory(axioms, ordinary, strict, defeasible,
                                                                 premise_preferences, rule_preferences, ordering)
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
            explanations = get_str_explanations(arg_theory, semantics, ordering, extension, accepted, function,
                                                expltype,
                                                strategy, form)

            return html.Div([html.H4('The Explanation(s):', style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(explanations).replace('set()','{}')))])


@app.callback(
    dash.dependencies.Output('strnet-output', 'children'),
    dash.dependencies.Output('strnet-evaluation', 'children'),
    dash.dependencies.Output('strnet-explanation', 'children'),
    dash.dependencies.Input('strnet', 'selection'),
    dash.dependencies.Input('strnet', 'data'),
    dash.dependencies.Input('aspic-axioms', 'value'),
    dash.dependencies.Input('aspic-ordinary-premises', 'value'),
    dash.dependencies.Input('aspic-strict-rules', 'value'),
    dash.dependencies.Input('aspic-defeasible-rules', 'value'),
    dash.dependencies.Input('ordinary-prem-preferences', 'value'),
    dash.dependencies.Input('defeasible-rule-preferences', 'value'),
    dash.dependencies.Input('ordering-choice', 'value'),
    dash.dependencies.Input('ordering-link', 'value'),
    dash.dependencies.Input('str-evaluation-semantics', 'value'),
    dash.dependencies.Input('str-explanation-function', 'value'),
    dash.dependencies.Input('str-explanation-type', 'value'),
    dash.dependencies.Input('str-evaluation-strategy', 'value'),
    dash.dependencies.Input('str-explanation-form', 'value'),
    prevent_initial_call=True
)
def interactive_str_graph(selection, data, axioms, ordinary, strict, defeasible, premise_preferences, rule_preferences,
                          choice, link,
                          semantics, function, expltype, strategy, form):
    while selection is not None:
        ordering = choice + link
        arg_theory, error_message = get_argumentation_theory(axioms, ordinary, strict, defeasible, premise_preferences,
                                                             rule_preferences, ordering)
        if error_message != '':
            return error_message
        select_id = selection['nodes'][0]
        for node in data['nodes']:
            if node.get('id') == select_id:
                select_node = node.get('label')
        for arg in arg_theory.all_arguments:
            if str(arg) == str(select_node):
                argument = arg
                formula = arg.conclusion
        arg_ext = []
        output_arg = html.Div(
            [html.H4('The selected argument:', style={'color': '#152A47'}), html.H6('{}'.format(str(argument))),
             html.H4('The selected conclusion:', style={'color': '#152A47'}),
             html.H6('{}'.format(str(argument.conclusion)))])
        output_accept = ''
        expl_output = ''
        output_evaluation = ''
        if semantics != '':
            frozen_extensions = get_str_extensions(arg_theory, semantics, ordering)
            if strategy != '':
                skep_accept = False
                wskep_accept = False
                cred_accept = False
                if semantics != 'Grd':
                    extensions = [set(frozen_extension) for frozen_extension in frozen_extensions]
                    skep_accepted = get_accepted_formulas(extensions, 'Skep')
                    wskep_accepted = get_accepted_formulas(extensions, 'WSkep')
                    cred_accepted = get_accepted_formulas(extensions, 'Cred')
                    for ext in extensions:
                        if argument in ext:
                            arg_ext.append(ext)
                    if formula in skep_accepted:
                        skep_accept = True
                    if formula in wskep_accepted:
                        wskep_accept = True
                    if formula in cred_accepted:
                        cred_accept = True
                elif semantics == 'Grd':
                    extensions = frozen_extensions
                    if argument in extensions:
                        arg_ext.append(extensions)
                        skep_accepted = extensions
                        cred_accepted = extensions
                        skep_accept = True
                        wskep_accept = True
                        cred_accept = True
                if skep_accept:
                    output_accept += str(formula) + ' is (weakly) skeptically and credulously accepted.'
                    if function is not None and expltype == 'Acc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div([html.H4(
                            'The skeptical acceptance explanation for {}:'.format(str(formula)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}'))), html.H4(
                                'The credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no non-acceptance explanation for formula {}, since it is '
                                                'skeptically accepted.'.format(
                                                    formula)])
                elif wskep_accept:
                    output_accept += str(
                        formula) + ' is weakly skeptically and credulously accepted, but not skeptically accepted.'
                    if function is not None and expltype == 'Acc':
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}')))])
                elif cred_accept:
                    output_accept += str(formula) + ' is credulously but not (weakly) skeptically accepted.'
                    if function is not None and expltype == 'Acc':
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div(
                            [html.H4('The credulous acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(cred_expla.get(str(formula))).replace('set()','{}')))])
                    elif function is not None and expltype == 'NonAcc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        expl_output = html.Div(
                            [html.H4('The not skeptical acceptance explanation for {}:'.format(str(formula)),
                                     style={'color': '#152A47'}),
                             html.H6('\n {}'.format(str(skep_expla.get(str(formula))).replace('set()','{}')))])
                elif skep_accept == False and cred_accept == False:
                    output_accept += str(argument) + ' is neither credulously nor (weakly) skeptically accepted.'
                    if function is not None and expltype == 'NonAcc':
                        skep_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, skep_accepted,
                                                          function, expltype, 'Skep', form)
                        cred_expla = get_str_explanations(arg_theory, semantics, ordering, extensions, cred_accepted,
                                                          function, expltype, 'Cred', form)
                        expl_output = html.Div([html.H4(
                            'The not skeptical acceptance explanation for {}:'.format(str(argument)),
                            style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(skep_expla.get(str(argument))).replace('set()','{}'))), html.H4(
                                'The not credulous acceptance explanation for {}:'.format(str(argument)),
                                style={'color': '#152A47'}),
                            html.H6('\n {}'.format(str(cred_expla.get(str(argument))).replace('set()','{}')))])
                    elif function is not None and expltype == 'Acc':
                        expl_output = html.Div([html.H4('Error', style={'color': 'red'}),
                                                'There is no acceptance explanation for formula {}, since it is not '
                                                'credulously accepted.'.format(
                                                    formula)])
            output_evaluation = html.Div(
                [html.H4('The extensions with argument {}:'.format(str(argument)), style={'color': '#152A47'}),
                 html.H6('{}'.format(arg_ext)), html.H6('{}'.format(output_accept))])
        return output_arg, output_evaluation, expl_output
    raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port=8050)
