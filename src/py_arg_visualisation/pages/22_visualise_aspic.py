import base64
import json
from typing import List, Dict

import dash
import dash_bootstrap_components as dbc
import visdcc
from dash import ctx, html, callback, Input, Output, State, ALL, dcc
from dash.exceptions import PreventUpdate

from py_arg.aspic.classes.argumentation_system import ArgumentationSystem
from py_arg.aspic.classes.argumentation_theory import ArgumentationTheory
from py_arg.aspic.classes.instantiated_argument import InstantiatedArgument
from py_arg.aspic.generators.argumentation_system_generators. \
    layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.aspic.generators.argumentation_theory_generators. \
    argumentation_theory_generator import \
    ArgumentationTheoryGenerator
from py_arg.aspic.import_export.argumentation_theory_from_json_reader import \
    ArgumentationTheoryFromJsonReader
from py_arg.aspic.import_export.argumentation_theory_to_json_writer import \
    ArgumentationTheoryToJSONWriter
from py_arg_visualisation.functions.explanations_functions. \
    explanation_function_options import \
    EXPLANATION_FUNCTION_OPTIONS
from py_arg_visualisation.functions.explanations_functions. \
    get_at_explanations import get_str_explanations
from py_arg.aspic.semantics.get_accepted_formulas import get_accepted_formulas
from py_arg.abstract_argumentation.semantics. \
    get_argumentation_framework_extensions import \
    get_argumentation_framework_extensions
from py_arg_visualisation.functions.extensions_functions. \
    get_acceptance_strategy import get_acceptance_strategy
from py_arg_visualisation.functions.graph_data_functions.get_aspic_graph_data \
    import get_argumentation_theory_aspic_graph_data
from py_arg_visualisation.functions.graph_data_functions. \
    get_at_graph_data import get_argumentation_theory_af_graph_data
from py_arg_visualisation.functions.import_functions. \
    read_argumentation_theory_functions import \
    read_argumentation_theory
from py_arg_visualisation.functions.ordering_functions. \
    get_ordering_by_specification import \
    get_ordering_by_specification

dash.register_page(__name__, name='Visualise ASPIC+ AT',
                   title='Visualise ASPIC+ AT')


def get_aspic_layout(aspic_setting, structured_evaluation,
                     structured_explanation):
    left_column = dbc.Col(
        dbc.Accordion([
            dbc.AccordionItem(aspic_setting,
                              title='ASPIC+ Argumentation Theory'),
            dbc.AccordionItem(structured_evaluation,
                              title='Evaluation', item_id='Evaluation'),
            dbc.AccordionItem(structured_explanation,
                              title='Explanation', item_id='Explanation')
        ], id='structured-evaluation-accordion')
    )

    aspic_options = {
        'physics': {'enabled': True},
        'solver': 'hierarchicalRepulsion',
        'layout': {'hierarchical': {'enabled': True, 'direction': 'DU',
                                    'sortMethod': 'directed'}},
        'wind': {'x': 50, 'y': 50},
        'improvedLayout': True,
        'height': '500px',
        'edges': {'color': {
            'inherit': False,
        }},
        'interaction': {'hover': True},
    }
    af_options = {'height': '500px'}

    right_column = dbc.Col([
        dbc.Row([
            dbc.Card(
                dcc.Tabs([
                    dcc.Tab(label='AF visualisation', children=[
                        visdcc.Network(data={'nodes': [], 'edges': []},
                                       id='22-af-graph',
                                       options=af_options)]),
                    dcc.Tab(label='Structured visualisation', children=[
                        visdcc.Network(data={'nodes': [], 'edges': []},
                                       id='22-aspic-graph',
                                       options=aspic_options),
                        dbc.Checklist(
                            options=[{'label': 'Show contradictories',
                                      'value': 'show_contra'}],
                            value=['show_contra'],
                            inline=True, switch=True,
                            id='22-aspic-graph-show-contradictories'
                        ),
                    ]),
                ]))])])
    return dbc.Row([left_column, right_column])


def get_aspic_setting_specification_div():
    return html.Div(children=[
        dcc.Store(id='selected-argument-store-structured'),
        dbc.Col([
            dbc.Row([dbc.Col(dbc.Button(
                'Generate random', id='generate-random-arg-theory-button',
                n_clicks=0, className='w-100')),
                     dbc.Col(dcc.Upload(dbc.Button(
                         'Open existing AT', n_clicks=0, className='w-100'),
                         id='22-open-existing-aspic-at'
                     ))],
                    className='mt-2'),
            dbc.Row([
                dbc.Col([html.B('Axioms')]),
                dbc.Col([html.B('Ordinary premises')]),
                dbc.Col([html.B('Ordinary premise preferences')]),
            ]),
            dbc.Row([
                dbc.Col([dbc.Textarea(
                    id='aspic-axioms',
                    placeholder='Add one axiom per line. '
                                'For example:\n p \n -q \n ~r',
                    value='', style={'height': '200px'})]),
                dbc.Col([dbc.Textarea(
                    id='aspic-ordinary-premises',
                    placeholder='Add one ordinary premise per line. '
                                'For example:\n p \n -q \n ~r',
                    value='', style={'height': '200px'}), ]),
                dbc.Col([dbc.Textarea(
                    id='ordinary-prem-preferences',
                    placeholder='Add one preference between two premises per '
                                'line. '
                                'For example:\n p < -q \n -q > ~r',
                    value='', style={'height': '200px'}), ]),
            ]),
            dbc.Row([
                dbc.Col([html.B('Strict rules')]),
                dbc.Col([html.B('Defeasible rules')]),
                dbc.Col([html.B('Defeasible rule preferences')]),
            ]),
            dbc.Row([
                dbc.Col([dbc.Textarea(
                    id='aspic-strict-rules',
                    placeholder='Add one strict rule per line. '
                                'For example:\n p->q \n -q -> -r',
                    value='', style={'height': '200px'})]),
                dbc.Col([dbc.Textarea(
                    id='aspic-defeasible-rules',
                    placeholder='Add one defeasible rule per line, '
                                'including the rule name. '
                                'For example:\n d1: p=>q \n d2: -q => -r',
                    value='', style={'height': '200px'}), ]),
                dbc.Col([dbc.Textarea(
                    id='defeasible-rule-preferences',
                    placeholder='Add one preference between two rules per '
                                'line. '
                                'For example:\n d1 < d2',
                    value='', style={'height': '200px'}), ]),
            ]),
            dbc.Row([html.B('Ordering')]),
            dbc.Row([
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Democratic', 'value': 'democratic'},
                        {'label': 'Elitist', 'value': 'elitist'}
                    ], value='democratic', id='ordering-choice')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Last link', 'value': 'last_link'},
                        {'label': 'Weakest link', 'value': 'weakest_link'}
                    ],
                    value='last_link', id='ordering-link')),
            ]),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText('Filename'),
                    dbc.Input(value='edited_aspic_theory',
                              id='22-aspic-theory-filename'),
                    dbc.InputGroupText('.'),
                    dbc.Select(
                        options=[{'label': extension, 'value': extension}
                                 for extension in ['JSON']],
                        value='JSON', id='22-aspic-theory-extension'),
                    dbc.Button('Download',
                               id='22-aspic-theory-download-button'),
                ], className='mt-2'),
                dcc.Download(id='22-aspic-theory-download')
            ])
        ])
    ])


def get_structured_evaluation_specification_div():
    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.B('Semantics')),
                dbc.Col(dbc.Select(options=[
                    {'label': 'Admissible', 'value': 'Admissible'},
                    {'label': 'Complete', 'value': 'Complete'},
                    {'label': 'Grounded', 'value': 'Grounded'},
                    {'label': 'Preferred', 'value': 'Preferred'},
                    {'label': 'Ideal', 'value': 'Ideal'},
                    {'label': 'Stable', 'value': 'Stable'},
                    {'label': 'Semi-stable', 'value': 'SemiStable'},
                    {'label': 'Eager', 'value': 'Eager'},
                ], value='Complete', id='structured-evaluation-semantics')),
            ]),
            dbc.Row(id='22-aspic-evaluation-semantics'),
            dbc.Row([
                dbc.Col(html.B('Evaluation strategy')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Weakly Skeptical',
                         'value': 'WeaklySkeptical'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ],
                    value='Credulous', id='structured-evaluation-strategy')),
            ]),
            dbc.Row(id='22-aspic-evaluation-accepted')
        ]),
    ])


def get_structured_explanation_specification_div():
    return html.Div([
        dbc.Row([
            dbc.Col(html.B('Type')),
            dbc.Col(dbc.Select(options=[{'label': 'Acceptance',
                                         'value': 'Acceptance'},
                                        {'label': 'Non-Acceptance',
                                         'value': 'NonAcceptance'}],
                               value='Acceptance',
                               id='structured-explanation-type'))]),
        dbc.Row([
            dbc.Col(html.B('Explanation function')),
            dbc.Col(dbc.Select(id='structured-explanation-function'))
        ]),
        dbc.Row([
            dbc.Col(html.B('Explanation form')),
            dbc.Col(dbc.Select(options=[{'label': 'Argument', 'value': 'Arg'},
                                        {'label': 'Premises', 'value': 'Prem'},
                                        {'label': 'Rules', 'value': 'Rule'},
                                        {'label': 'Sub-arguments',
                                         'value': 'SubArg'}],
                               value='Arg', id='structured-explanation-form'))
        ]),
        dbc.Row(id='structured-explanation')
    ])


layout = html.Div(
    children=[
        html.H1('Visualisation of ASPIC+ argumentation theories'),
        get_aspic_layout(get_aspic_setting_specification_div(),
                         get_structured_evaluation_specification_div(),
                         get_structured_explanation_specification_div())
    ]
)


@callback(
    Output('22-aspic-theory-download', 'data'),
    Input('22-aspic-theory-download-button', 'n_clicks'),
    State('aspic-axioms', 'value'),
    State('aspic-ordinary-premises', 'value'),
    State('aspic-strict-rules', 'value'),
    State('aspic-defeasible-rules', 'value'),
    State('ordinary-prem-preferences', 'value'),
    State('defeasible-rule-preferences', 'value'),
    State('22-aspic-theory-filename', 'value'),
    State('22-aspic-theory-extension', 'value'),
    prevent_initial_call=True,
)
def download_generated_abstract_argumentation_framework(
        _nr_clicks: int,
        axioms_str: str, ordinary_premises_str: str, strict_rules_str: str,
        defeasible_rules_str: str, ordinary_premise_preferences_str: str,
        defeasible_rule_preferences_str: str,
        filename: str,
        extension: str):
    arg_theory = read_argumentation_theory(
        axioms_str, ordinary_premises_str, strict_rules_str,
        defeasible_rules_str, ordinary_premise_preferences_str,
        defeasible_rule_preferences_str)

    if extension == 'JSON':
        argumentation_theory_json = \
            ArgumentationTheoryToJSONWriter().to_dict(arg_theory)
        argumentation_theory_str = json.dumps(argumentation_theory_json)
    else:
        raise NotImplementedError

    return {'content': argumentation_theory_str,
            'filename': filename + '.' + extension}


@callback(
    Output('structured-explanation-function', 'options'),
    Output('structured-explanation-function', 'value'),
    [Input('structured-explanation-type', 'value')]
)
def setting_choice(choice: str):
    return EXPLANATION_FUNCTION_OPTIONS[choice], \
        EXPLANATION_FUNCTION_OPTIONS[choice][0]['value']


@callback(
    Output('aspic-axioms', 'value'),
    Output('aspic-ordinary-premises', 'value'),
    Output('aspic-strict-rules', 'value'),
    Output('aspic-defeasible-rules', 'value'),
    Output('ordinary-prem-preferences', 'value'),
    Output('defeasible-rule-preferences', 'value'),
    Input('generate-random-arg-theory-button', 'n_clicks'),
    Input('22-open-existing-aspic-at', 'contents'),
    State('22-open-existing-aspic-at', 'filename')
)
def generate_random_argumentation_theory(
        nr_of_clicks_random_button: int,
        load_arg_theory_content, load_arg_theory_filename):
    if ctx.triggered_id == 'generate-random-arg-theory-button' and \
            nr_of_clicks_random_button > 0:
        argumentation_system_generator = LayeredArgumentationSystemGenerator(
            nr_of_literals=10, nr_of_rules=5,
            rule_antecedent_distribution={1: 4, 2: 1},
            literal_layer_distribution={0: 5, 1: 3, 2: 2},
            strict_rule_ratio=0.3
        )
        argumentation_system = argumentation_system_generator.generate()
        argumentation_theory_generator = ArgumentationTheoryGenerator(
            argumentation_system, knowledge_literal_ratio=0.4,
            axiom_knowledge_ratio=0.5)
        argumentation_theory = argumentation_theory_generator.generate()
    elif ctx.triggered_id == '22-open-existing-aspic-at':
        content_type, content_str = load_arg_theory_content.split(',')
        decoded = base64.b64decode(content_str)

        # name = load_arg_theory_filename.split('.')[0]
        if load_arg_theory_filename.upper().endswith('.JSON'):
            argumentation_theory = \
                ArgumentationTheoryFromJsonReader().from_json(json.loads(
                    decoded))
            argumentation_system = argumentation_theory.argumentation_system
        else:
            raise NotImplementedError('This extension has no reader yet.')
    else:
        return '', '', '', '', '', ''

    aspic_axioms_value = \
        '\n'.join(str(axiom)
                  for axiom in argumentation_theory.knowledge_base_axioms)
    aspic_ordinary_premises_value = \
        '\n'.join(str(premise)
                  for premise in argumentation_theory.
                  knowledge_base_ordinary_premises)
    aspic_strict_rule = \
        '\n'.join(str(strict_rule)
                  for strict_rule in argumentation_system.strict_rules)
    aspic_defeasible_rule = \
        '\n'.join(f'{defeasible_rule.id}: {str(defeasible_rule)}'
                  for defeasible_rule in argumentation_system.
                  defeasible_rules)
    aspic_ordinary_premise_preference_value = \
        '\n'.join(f'{str(preference[0])} < {str(preference[1])}'
                  for preference in argumentation_theory.
                  ordinary_premise_preferences.preference_tuples)
    aspic_defeasible_rule_preference_vale = \
        '\n'.join(f'{preference[0].id} < {preference[1].id}'
                  for preference in argumentation_system.rule_preferences.
                  preference_tuples)
    return aspic_axioms_value, aspic_ordinary_premises_value, \
        aspic_strict_rule, aspic_defeasible_rule, \
        aspic_ordinary_premise_preference_value, \
        aspic_defeasible_rule_preference_vale


@callback(
    Output('22-af-graph', 'data'),
    Output('22-aspic-graph', 'data'),
    Input('aspic-axioms', 'value'),
    Input('aspic-ordinary-premises', 'value'),
    Input('aspic-strict-rules', 'value'),
    Input('aspic-defeasible-rules', 'value'),
    Input('ordinary-prem-preferences', 'value'),
    Input('defeasible-rule-preferences', 'value'),
    Input('ordering-choice', 'value'),
    Input('ordering-link', 'value'),
    Input('selected-argument-store-structured', 'data'),
    Input('color-blind-mode', 'on'),
    Input('22-aspic-graph-show-contradictories', 'value'),
    prevent_initial_call=True
)
def create_argumentation_theory(
        axioms_str: str, ordinary_premises_str: str, strict_rules_str: str,
        defeasible_rules_str: str, ordinary_premise_preferences_str: str,
        defeasible_rule_preferences_str: str, ordering_choice_value: str,
        ordering_link_value: str, selected_arguments: Dict[str, List[str]],
        color_blind_mode: bool, show_contradictories: bool):
    # Read the ordering
    ordering_specification = ordering_choice_value + '_' + ordering_link_value

    # Read the argumentation theory
    try:
        arg_theory = read_argumentation_theory(
            axioms_str, ordinary_premises_str, strict_rules_str,
            defeasible_rules_str, ordinary_premise_preferences_str,
            defeasible_rule_preferences_str)
    except ValueError:
        arg_theory = ArgumentationTheory(ArgumentationSystem(
            {}, {}, [], []), [], [])

    # Generate the graph data for this argumentation theory
    af_graph_data = get_argumentation_theory_af_graph_data(
        arg_theory, ordering_specification, selected_arguments,
        color_blind_mode)

    show_contra_bool = 'show_contra' in show_contradictories
    aspic_graph_data = get_argumentation_theory_aspic_graph_data(
        arg_theory, selected_arguments,
        color_blind_mode, show_contra_bool)
    return af_graph_data, aspic_graph_data


@callback(
    Output('22-aspic-evaluation-semantics', 'children'),
    Output('22-aspic-evaluation-accepted', 'children'),
    State('aspic-axioms', 'value'),
    State('aspic-ordinary-premises', 'value'),
    State('aspic-strict-rules', 'value'),
    State('aspic-defeasible-rules', 'value'),
    State('ordinary-prem-preferences', 'value'),
    State('defeasible-rule-preferences', 'value'),
    State('ordering-choice', 'value'),
    State('ordering-link', 'value'),
    Input('structured-evaluation-accordion', 'active_item'),
    Input('structured-evaluation-semantics', 'value'),
    Input('structured-evaluation-strategy', 'value'),
    prevent_initial_call=True
)
def evaluate_structured_argumentation_framework(
        axioms_str: str, ordinary_premises_str: str, strict_rules_str: str,
        defeasible_rules_str: str, ordinary_premise_preferences_str: str,
        defeasible_rule_preferences_str: str, ordering_choice_value: str,
        ordering_link_value: str, active_item: str,
        semantics_specification: str, acceptance_strategy_specification: str):
    if active_item != 'Evaluation':
        raise PreventUpdate

    # Read the ordering
    ordering_specification = ordering_choice_value + '_' + ordering_link_value

    # Read the argumentation theory
    try:
        arg_theory = read_argumentation_theory(
            axioms_str, ordinary_premises_str, strict_rules_str,
            defeasible_rules_str, ordinary_premise_preferences_str,
            defeasible_rule_preferences_str)
    except ValueError:
        arg_theory = ArgumentationTheory(
            ArgumentationSystem({}, {}, [], []), [], [])

    ordering = get_ordering_by_specification(arg_theory,
                                             ordering_specification)
    arg_framework = arg_theory.create_abstract_argumentation_framework(
        'af', ordering)
    frozen_extensions = get_argumentation_framework_extensions(
        arg_framework, semantics_specification)

    extensions = [set(frozen_extension)
                  for frozen_extension in frozen_extensions]
    acceptance_strategy = get_acceptance_strategy(
        acceptance_strategy_specification)
    accepted_formulas = get_accepted_formulas(arg_theory, extensions,
                                              acceptance_strategy)

    extension_buttons = []
    formula_arguments = {
        formula: []
        for formula in arg_theory.argumentation_system.language.keys()}
    for extension in extensions:
        for argument in extension:
            assert isinstance(argument, InstantiatedArgument)
            accepted_formula = argument.conclusion
            formula_arguments[accepted_formula.s1].append(argument.name)

        out_arguments = {attacked for attacked in arg_framework.arguments
                         if any(argument in arg_framework.
                                get_incoming_defeat_arguments(attacked)
                                for argument in extension)}
        undecided_arguments = {argument for argument in arg_framework.arguments
                               if argument not in extension and
                               argument not in out_arguments}
        extension_readable_str = \
            '{' + ', '.join(argument.short_name
                            for argument in extension) + '}'

        extension_in_str = '+'.join(argument.name
                                    for argument in sorted(extension))
        extension_out_str = '+'.join(argument.name
                                     for argument in sorted(out_arguments))
        extension_undecided_str = \
            '+'.join(argument.name for argument in sorted(undecided_arguments))
        extension_long_str = '|'.join(
            [extension_in_str, extension_undecided_str, extension_out_str])
        extension_buttons.append(dbc.Button([
            extension_readable_str], color='secondary',
            id={'type': 'extension-button', 'index': extension_long_str}))

    accepted_formula_buttons = [dbc.Button(
        formula.s1, color='secondary',
        id={'type': 'formula-button-structured',
            'index': '+'.join(formula_arguments[formula.s1])})
        for formula in sorted(accepted_formulas)]

    semantics_div = html.Div([
        html.B('The extension(s):'),
        html.Br(),
        html.I('Click on the extension buttons to '
               'display the corresponding extension '
               'in the graph.'),
        html.Div(extension_buttons),
        html.Br()
    ])
    accepted_div = html.Div([
        html.B('The accepted formula(s):'),
        html.Br(),
        html.I('Click on the accepted formula buttons to '
               'display the corresponding argument '
               'in the graph.'),
        html.Div(accepted_formula_buttons),
    ])

    return semantics_div, accepted_div


@callback(
    Output('selected-argument-store-structured', 'data'),
    Input({'type': 'extension-button', 'index': ALL}, 'n_clicks'),
    Input({'type': 'formula-button-structured', 'index': ALL}, 'n_clicks'),
    State('selected-argument-store-structured', 'data'),
)
def mark_extension_in_graph(
        _nr_of_clicks_values_extension, _nr_of_clicks_values_formula,
        old_selected_data: List[str]):
    button_clicked_id = \
        dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if button_clicked_id == '':
        return old_selected_data
    button_clicked_id_content = json.loads(button_clicked_id)
    button_clicked_id_type = button_clicked_id_content['type']
    button_clicked_id_index = button_clicked_id_content['index']
    if button_clicked_id_type == 'extension-button':
        in_part, undecided_part, out_part = \
            button_clicked_id_index.split('|', 3)
        return {'green': in_part.split('+'),
                'yellow': undecided_part.split('+'),
                'red': out_part.split('+')}
    elif button_clicked_id_type == 'formula-button-structured':
        return {'blue': button_clicked_id_index.split('+')}
    return []


@callback(
    Output('structured-explanation', 'children'),
    Input('structured-evaluation-accordion', 'active_item'),
    State('aspic-axioms', 'value'),
    State('aspic-ordinary-premises', 'value'),
    State('aspic-strict-rules', 'value'),
    State('aspic-defeasible-rules', 'value'),
    State('ordinary-prem-preferences', 'value'),
    State('defeasible-rule-preferences', 'value'),
    State('ordering-choice', 'value'),
    State('ordering-link', 'value'),
    State('structured-evaluation-semantics', 'value'),
    Input('structured-explanation-function', 'value'),
    Input('structured-explanation-type', 'value'),
    State('structured-evaluation-strategy', 'value'),
    Input('structured-explanation-form', 'value'),
    prevent_initial_call=True
)
def derive_explanation_structured(
        active_item: str, axioms, ordinary, strict, defeasible,
        premise_preferences, rule_preferences, choice, link, semantics,
        function, explanation_type, strategy: str, form):
    if active_item != 'Explanation':
        raise PreventUpdate

    try:
        arg_theory = read_argumentation_theory(
            axioms, ordinary, strict, defeasible, premise_preferences,
            rule_preferences)
    except ValueError:
        arg_theory = ArgumentationTheory(ArgumentationSystem(
            {}, {}, [], []), [], [])

    ordering = get_ordering_by_specification(arg_theory, choice + '_' + link)
    arg_framework = arg_theory.create_abstract_argumentation_framework(
        'af', ordering)
    frozen_extensions = get_argumentation_framework_extensions(
        arg_framework, semantics)

    if semantics == 'Grounded':
        extension = frozen_extensions
        accepted = extension
    else:
        extension = [set(frozen_extension)
                     for frozen_extension in frozen_extensions]
        acceptance_strategy = get_acceptance_strategy(strategy)
        accepted = get_accepted_formulas(arg_theory, extension,
                                         acceptance_strategy)
    explanations = get_str_explanations(arg_theory, semantics, ordering,
                                        extension, accepted, function,
                                        explanation_type, strategy, form)

    return html.Div(
        [html.Div(html.B('Explanation(s) by formula:'))] +
        [html.Div([
            html.B(explanation_key),
            html.Ul([html.Li(str(explanation_value).replace(
                'set()', '{}'))
                for explanation_value in explanation_values])])
            for explanation_key, explanation_values in
            explanations.items()])
