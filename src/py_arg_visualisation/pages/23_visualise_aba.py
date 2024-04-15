from typing import List, Dict

import dash
import dash_bootstrap_components as dbc
import visdcc
from dash import html, callback, Input, Output, State, dcc
from dash.exceptions import PreventUpdate

from py_arg.assumption_based_argumentation.classes.rule import Rule
from py_arg.assumption_based_argumentation.classes.aba_framework \
    import AssumptionBasedArgumentationFramework
from py_arg_visualisation.functions.extensions_functions import \
    get_abaf_extensions
from py_arg_visualisation.functions.extensions_functions import \
    get_accepted_assumptions
from py_arg_visualisation.functions.graph_data_functions import \
    get_aba_graph_data

dash.register_page(__name__, name='Visualise ABA Framework',
                   title='Visualise ABA Framework')


def get_aba_layout(abaf, aba_evaluation):
    left_column = dbc.Col(
        dbc.Accordion([
            dbc.AccordionItem(abaf, title='ABA Framework'),
            dbc.AccordionItem(aba_evaluation, title='Evaluation',
                              item_id='23-ABA-Evaluation'),
        ], id='23-ABA-evaluation-accordion')
    )
    right_column = dbc.Col([
        dbc.Row([
            dbc.Card(visdcc.Network(data={'nodes': [], 'edges': []},
                                    id='23-ABA-instantiated-graph',
                                    options={'height': '500px'}), body=True),
        ])
    ])
    return dbc.Row([left_column, right_column])


def get_aba_setting_specification_div():
    return html.Div(children=[
        dcc.Store(id='23-selected-argument-store-structured'),
        dbc.Col([
            dbc.Row([
                dbc.Col([html.B('Choose a predefined ABA framework '
                                '(optional)')]),
                dbc.Col([dbc.Select(id='23-ABA-choose-predefined',
                                    options=[
                                       {'label': '-', 'value': 'none'},
                                       {'label': 'ABA tutorial example 3.1',
                                        'value': 'lasagna'},
                                       {'label': 'ABA tutorial example 5.1',
                                        'value': 'semantics_test'},
                                       {'label': 'ABA tutorial example 5.2',
                                        'value': 'semantics_test_2'},
                                       {'label': 'ABA tutorial example 5.3',
                                        'value': 'semantics_test_3'},
                                       {'label': 'ABA tutorial example 5.4',
                                        'value': 'semantics_test_4'},
                                       {'label': 'ABA tutorial Tweety example',
                                        'value': 'tweety'},
                                       {'label': 'Difference Asms vs. Arg '
                                                 'Semantics Semi-Stable',
                                        'value': 'semantics_exm_ss'},
                                    ], value='none')])]),
            dbc.Row([
                dbc.Col([html.B('Atoms')]),
                dbc.Col([html.B('Rules')]),
            ]),
            dbc.Row([
                dbc.Col([dbc.Textarea(
                    id='23-ABA-L',
                    placeholder='Add ordinary atom per line. '
                                'For example:\n a \n b \n p \n q',
                    value='', style={'height': '200px'})]),
                dbc.Col([dbc.Textarea(
                    id='23-ABA-R',
                    placeholder='Add one rule per line. '
                                'For example:\n p <- a, b \n q <- p',
                    value='', style={'height': '200px'}), ]),
            ]),
            dbc.Row([
                dbc.Col([html.B('Assumptions')]),
                dbc.Col([html.B('Contraries')]),
            ]),
            dbc.Row([
                dbc.Col([dbc.Textarea(
                    id='23-ABA-A',
                    placeholder='Add one assumption per line. '
                                'For example:\n a \n b',
                    value='', style={'height': '200px'})]),
                dbc.Col([dbc.Textarea(
                    id='23-ABA-C',
                    placeholder='Add one assignment of a contrary per line. '
                                'For example:\n (a,p) \n (b,q) \n'
                                'This means that the contrary of a is p and '
                                'the contrary of b is q.',
                    value='', style={'height': '200px'}), ]),
            ]),
            dbc.Row([
                dbc.Col([dbc.Alert(id='23-ABA-error-explanation',
                                   color='warning', is_open=False)])
            ])
        ])
    ])


def get_aba_evaluation_specification_div():
    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.B('Semantics')),
                dbc.Col(dbc.Select(options=[
                    {'label': 'Stable', 'value': 'Stable'},
                    {'label': 'Semi-Stable', 'value': 'SemiStable'},
                    {'label': 'Preferred', 'value': 'Preferred'},
                    {'label': 'Conflict-Free', 'value': 'Conflict-Free'},
                    {'label': 'Naive', 'value': 'Naive'},
                    {'label': 'Grounded', 'value': 'Grounded'},
                    {'label': 'Admissible', 'value': 'Admissible'},
                    {'label': 'Complete', 'value': 'Complete'},
                ],
                    value='Complete', id='23-ABA-evaluation-semantics')),
            ]),

            dbc.Row([
                dbc.Col(html.B('Evaluation Strategy')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ],
                    value='Credulous', id='23-ABA-evaluation-strategy')),
            ]),
            dbc.Row(id='23-ABA-evaluation')
        ]),
    ])


layout = html.Div(
    children=[
        html.H1('Visualisation of ABA Frameworks'),
        get_aba_layout(get_aba_setting_specification_div(),
                       get_aba_evaluation_specification_div())
    ]
)


def read_aba(aba_l_str: str, aba_r_str: str, aba_a_str: str, aba_c_str: str):
    """
    Read the ABA framework from the str (in the four text fields).
    """
    # Read atoms (language)
    atoms = {
        atom
        for atom in aba_l_str.replace(' ', '').replace('.', '').split('\n')
        if atom}

    # Read rules
    cleaned_rule_str = aba_r_str.replace(' ', '').replace('.', '')
    rules = set()
    for rule_str in cleaned_rule_str.split('\n'):
        if '<-' in rule_str:
            before_rule, after_rule = rule_str.split('<-', 2)
            if before_rule:
                if after_rule:
                    antecedents = set(after_rule.split(','))
                else:
                    antecedents = set()
                rules.add(Rule(rule_str, antecedents, before_rule))
        if ':-' in rule_str:
            before_rule, after_rule = rule_str.split(':-', 2)
            if before_rule:
                if after_rule:
                    antecedents = set(after_rule.split(','))
                else:
                    antecedents = set()
                rules.add(Rule(rule_str, antecedents, before_rule))

    # Read assumptions
    assumptions = {
        atom
        for atom in aba_a_str.replace(' ', '').replace('.', '').split('\n')
        if atom}

    # Read contraries
    cleaned_contrary_str = \
        aba_c_str.replace(' ', '').replace('.', '').replace('(', '').\
        replace(')', '')
    contraries = {}
    for contrary_str in cleaned_contrary_str.split('\n'):
        if ',' in contrary_str:
            before_comma, after_comma = contrary_str.split(',', 2)
            if before_comma and after_comma:
                contraries[before_comma] = after_comma

    return AssumptionBasedArgumentationFramework(assumptions, rules,
                                                 atoms, contraries)


@callback(
    Output('23-ABA-L', 'value'),
    Output('23-ABA-R', 'value'),
    Output('23-ABA-A', 'value'),
    Output('23-ABA-C', 'value'),
    Input('23-ABA-choose-predefined', 'value'),
)
def prefill_predefined(predefined_value):
    if predefined_value == 'none':
        return '', '', '', ''
    if predefined_value == 'lasagna':
        language = 'happy \neating \ngood_food \nnot_eating \nno_fork \n' \
                   'dirty_hands \nfork \nclean_hands'
        rules = 'happy <- good_food, eating \ngood_food <- \n' \
                'not_eating <- no_fork, dirty_hands'
        assumptions = 'eating \nno_fork \ndirty_hands'
        contraries = '(eating, not_eating) \n(no_fork, fork) \n' \
                     '(dirty_hands, clean_hands)'
        return language, rules, assumptions, contraries
    if predefined_value == 'semantics_test':
        language = 'a\nb\nca\ncb'
        rules = 'ca <- a\nca <- b\ncb <- a'
        assumptions = 'a\nb'
        contraries = '(a, ca)\n(b, cb)'
        return language, rules, assumptions, contraries
    if predefined_value == 'semantics_test_2':
        language = 'a\nb\nc\nd\ne\nf\nca\ncb\ncc\ncd\nce\ncf'
        rules = 'ca <- a\nca <- b\ncb <- a\ncc <- d\ncd <- c\nce <- c\n' \
                'ce <- d\ncf <- e'
        assumptions = 'a\nb\nc\nd\ne\nf'
        contraries = '(a, ca)\n(b, cb)\n(c, cc)\n(d, cd)\n(e, ce)\n(f, cf)'
        return language, rules, assumptions, contraries
    if predefined_value == 'semantics_test_3':
        language = 'a\nb\nc\nca\ncb\ncc'
        rules = 'ca <- b\ncb <- a\ncc <- b\ncc<- c'
        assumptions = 'a\nb\nc'
        contraries = '(a, ca)\n(b, cb)\n(c, cc)'
        return language, rules, assumptions, contraries
    if predefined_value == 'semantics_test_4':
        language = 'a\nb\nc\nd\np\nq\nr\ns\nt'
        rules = 'p <- q, a\nq<- \nr<- b, c'
        assumptions = 'a\nb\nc\nd'
        contraries = '(a, r)\n(b, s)\n(c, t)\n(d, p)'
        return language, rules, assumptions, contraries
    if predefined_value == 'tweety':
        language = 'normal[tweety]\n' \
                   'normal[joe]\n' \
                   'fly[tweety]\n' \
                   'fly[joe]\n' \
                   'bird[tweety]\n' \
                   'bird[joe]\n' \
                   'not_fly[tweety]\n' \
                   'not_fly[joe]\n' \
                   'penguin[tweety]\n' \
                   'penguin[joe]'
        rules = 'fly[tweety] <- bird[tweety], normal[tweety]\n' \
                'fly[joe] <- bird[joe], normal[joe]\n' \
                'not_fly[tweety] <- penguin[tweety]\n' \
                'not_fly[joe] <- penguin[joe]\n' \
                'bird[tweety] <- penguin[tweety]\n' \
                'bird[joe] <- penguin[joe]\n' \
                'penguin[tweety] <- \n' \
                'bird[joe] <-'
        assumptions = 'normal[tweety]\n' \
                      'normal[joe]'
        contraries = '(normal[tweety], not_fly[tweety])\n' \
                     '(normal[joe], not_fly[joe])'
        return language, rules, assumptions, contraries
    if predefined_value == 'semantics_exm_ss':
        language = 'a\nb\nc\nd\nca\ncb\ncc\ncd'
        rules = 'cc <- c\nca <- b\ncb <- a\ncc <- c, a\ncd <- d, b'
        assumptions = 'a\nb\nc\nd'
        contraries = '(a, ca)\n(b, cb)\n(c, cc)\n(d, cd)'
        return language, rules, assumptions, contraries
    return NotImplementedError


@callback(
    Output('23-ABA-instantiated-graph', 'data'),
    Output('23-ABA-error-explanation', 'children'),
    Output('23-ABA-error-explanation', 'is_open'),
    Input('23-ABA-L', 'value'),
    Input('23-ABA-R', 'value'),
    Input('23-ABA-A', 'value'),
    Input('23-ABA-C', 'value'),
    Input('23-selected-argument-store-structured', 'data'),
    State('color-blind-mode', 'on'),
    prevent_initial_call=True
)
def create_abaf(aba_l_str: str, aba_r_str: str, aba_a_str: str, aba_c_str: str,
                selected_arguments: Dict[str, List[str]],
                color_blind_mode: bool):
    try:
        # Generate the graph data for this argumentation theory
        aba_framework = read_aba(aba_l_str, aba_r_str, aba_a_str, aba_c_str)
        error_message = ''
        alert_open = False
    except ValueError as value_error:
        aba_framework = AssumptionBasedArgumentationFramework(set(), set(),
                                                              set(), {})
        error_message = str(value_error)
        alert_open = True
    graph_data = get_aba_graph_data.apply(aba_framework, selected_arguments,
                                          color_blind_mode)
    return graph_data, error_message, alert_open


@callback(
    Output('23-ABA-evaluation', 'children'),
    State('23-ABA-L', 'value'),
    State('23-ABA-R', 'value'),
    State('23-ABA-A', 'value'),
    State('23-ABA-C', 'value'),
    Input('23-ABA-evaluation-accordion', 'active_item'),
    Input('23-ABA-evaluation-semantics', 'value'),
    Input('23-ABA-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_abaf(
        aba_l_str: str, aba_r_str: str, aba_a_str: str, aba_c_str: str,
        active_item: str, semantics_specification: str,
        acceptance_strategy_specification: str):
    if active_item != '23-ABA-Evaluation':
        raise PreventUpdate

    # Read the argumentation theory
    try:
        abaf = read_aba(aba_l_str, aba_r_str, aba_a_str, aba_c_str)
    except ValueError:
        abaf = AssumptionBasedArgumentationFramework(set(), set(), set(), {})

    extensions = get_abaf_extensions.apply(abaf, semantics_specification)
    accepted_assumptions = get_accepted_assumptions.apply(
        extensions, acceptance_strategy_specification)

    extension_buttons = []
    for extension in extensions:
        extension_readable_str = \
            '{' + ', '.join(assumption for assumption in extension) + '}'

        extension_buttons.append(dbc.Button(
            extension_readable_str, color='secondary',
            id={'type': 'extension-button', 'index': extension_readable_str}))

    accepted_assumptions_buttons = [dbc.Button(
        assumption, color='secondary',
        id={'type': 'formula-button-structured',
            'index': '+'.join(assumption)})
        for assumption in sorted(accepted_assumptions)]

    return [html.B('The extension(s):'),
            html.Div(extension_buttons),
            html.B('The accepted assumption(s):'),
            html.Div(accepted_assumptions_buttons)]
