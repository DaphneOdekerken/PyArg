import json

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State, MATCH

from py_arg.aspic.generators.argumentation_system_generators. \
    layered_argumentation_system_generator import \
    LayeredArgumentationSystemGenerator
from py_arg.aspic.import_export.argumentation_system_to_json_writer import \
    ArgumentationSystemToJSONWriter

dash.register_page(__name__, name='GenerateLayeredAspic',
                   title='Generate Layered ASPIC+ AS')

left_column = dbc.Col([
    html.H2('Input'),
    html.Br(),
    dbc.Row([dbc.Col(html.B('Number of literals')),
             dbc.Col([dbc.Input(
                 type='number', min=0, max=500, step=2, value=6,
                 id='03-generate-layered-aspic-nr-literals-input'),
                 dbc.Tooltip(
                     'The desired number of literals in the argumentation '
                     'system. Note that this number should be even.',
                     target='03-generate-layered-aspic-nr-literals-input'
                 )])]),
    dbc.Row([
        dbc.Col(html.B('Number of  rules')),
        dbc.Col([dbc.Input(type='number', min=0, max=500, step=1, value=3,
                           id='03-generate-layered-aspic-nr-rules-input'),
                 dbc.Tooltip(
                     'The desired number of rules (strict or defeasible).',
                     target='03-generate-layered-aspic-nr-rules-input')])]),
    dbc.Row([
        dbc.Col(html.B('Rule antecedent distribution')),
        dbc.Col([dbc.Input(
             id='03-generate-layered-aspic-rule-antecedent-distribution-input',
             value='2: 1, 1: 2'),
                  dbc.Tooltip(
                      'Number of rules with a specific number of '
                      'antecedents. '
                      'These should be put in the format '
                      '[nr_ants_1]: [nr_rules_1], '
                      '[nr_ants_2]: [nr_rules_2], ...',
                      target='03-generate-layered-aspic-rule-antecedent-'
                             'distribution-input')])]),
    dbc.Row([dbc.Col(html.B('Literal layer distribution')),
             dbc.Col([dbc.Input(
                 id='03-generate-layered-aspic-literal-layer-'
                    'distribution-input',
                 value='0: 3, 1: 2, 2: 1'),
                      dbc.Tooltip(
                          'Number of literals on a specific "layer" '
                          '(which is something '
                          'like the height in the support graph). '
                          'These should be put in the format '
                          '[layer_nr_1]: [nr_literals_1], '
                          '[layer_nr_2]: [nr_literals_2], ...',
                          target='03-generate-layered-aspic-literal-layer-'
                                 'distribution-input'
                          )])]),
    dbc.Row([dbc.Col(html.B('Strict rule ratio')),
             dbc.Col([dbc.Input(type='number', min=0, max=1, value=0,
                                id='03-generate-layered-aspic-strict-rule-'
                                   'ratio-input'),
                      dbc.Tooltip(
                          'Ration of strict rules over all rules, e.g. '
                          'if this number is 0.8, '
                          'then around 80% of the generated rules are '
                          'expected to be strict.',
                          target='03-generate-layered-aspic-strict-rule-'
                                 'ratio-input')])]),
    html.Br(),
    dbc.Row([dbc.Button('Generate', id='03-generate-layered-aspic-button',
                        className='w-50 mx-auto')])
])
right_column = dbc.Col([], id='03-generate-layered-aspic-output')
layout_generate_layered_aspic = dbc.Row([left_column, right_column])

layout = html.Div([
    html.H1('Generate Random Layered ASPIC+ Argumentation System'),
    html.P('This generator assumes that negation is used for contradiction. '
           'In addition, it does not generate any preference ordering '
           'between defeasible rules.'),
    html.Div(layout_generate_layered_aspic)
])


@callback(Output('03-generate-layered-aspic-output', 'children'),
          Input('03-generate-layered-aspic-button', 'n_clicks'),
          State('03-generate-layered-aspic-nr-literals-input', 'value'),
          State('03-generate-layered-aspic-nr-rules-input', 'value'),
          State('03-generate-layered-aspic-rule-antecedent-distribution-input',
                'value'),
          State('03-generate-layered-aspic-literal-layer-distribution-input',
                'value'),
          State('03-generate-layered-aspic-strict-rule-ratio-input', 'value'))
def generate_layered_aspic_argumentation_system(
        nr_clicks: int, nr_literals: str, nr_rules: str,
        rule_antecedent_distribution: str, literal_layer_distribution: str,
        strict_rule_ratio: str):
    if not nr_clicks:
        return 'Press the button to generate an argumentation framework.'

    try:
        nr_literals_int = int(nr_literals)
    except TypeError:
        return 'The number of literals is not an integer.'
    if nr_literals_int < 1:
        return 'The number of literals should be at least one.'

    try:
        nr_rules_int = int(nr_rules)
    except TypeError:
        return 'The number of rules is not an integer.'
    if nr_rules_int < 0:
        return 'The number of rules cannot be negative.'

    try:
        strict_rule_ratio_float = float(strict_rule_ratio)
    except TypeError:
        return 'The strict rule ratio is not a float.'
    if strict_rule_ratio_float < 0 or strict_rule_ratio_float > 1:
        return 'The strict rule ratio should be between 0 and 1.'

    try:
        rule_ant_distribution = {}
        rule_antecedent_parts = rule_antecedent_distribution.split(',')
        for rule_antecedent_part in rule_antecedent_parts:
            nr_ants, nr_rules_per_ant = rule_antecedent_part.split(':', 2)
            nr_ants_int = int(nr_ants)
            nr_rules_per_ant_int = int(nr_rules_per_ant)
            rule_ant_distribution[nr_ants_int] = nr_rules_per_ant_int
    except ValueError:
        return 'I could not read this rule antecedent distribution.'

    try:
        lit_layer_distribution = {}
        lit_layer_parts = literal_layer_distribution.split(',')
        for lit_layer_part in lit_layer_parts:
            nr_layer, nr_lits_per_layer = lit_layer_part.split(':', 2)
            nr_layer_int = int(nr_layer)
            nr_lits_per_layer_int = int(nr_lits_per_layer)
            lit_layer_distribution[nr_layer_int] = nr_lits_per_layer_int
    except ValueError:
        return 'I could not read this literal layer distribution.'

    generator = LayeredArgumentationSystemGenerator(
        nr_of_literals=nr_literals_int,
        nr_of_rules=nr_rules_int,
        rule_antecedent_distribution=rule_ant_distribution,
        literal_layer_distribution=lit_layer_distribution,
        strict_rule_ratio=strict_rule_ratio_float
    )
    argumentation_system = generator.generate()
    argumentation_system_json = json.dumps(
        ArgumentationSystemToJSONWriter().to_dict(argumentation_system))

    output_children = \
        [html.H2('Output'),
         dbc.Row([
             dbc.Col([html.B('Literals'), dbc.Textarea(
                 value='\n'.join(sorted(argumentation_system.language.keys())),
                 style={'height': '300px'})]),
             dbc.Col([html.B('Rules'), dbc.Textarea(
                 value='\n'.join(
                     (str(rule) for rule in argumentation_system.rules)),
                 style={'height': '300px'})])
         ]),
         dcc.Store(data=argumentation_system_json,
                   id={'type': '03-generate-layered-aspic-download-content',
                       'index': nr_clicks}),
         html.Br(),
         dbc.Row([
             dbc.InputGroup([
                 dbc.InputGroupText('Filename'),
                 dbc.Input(value='generated_as',
                           id={'type': '03-generate-layered-aspic-filename',
                               'index': nr_clicks}),
                 dbc.InputGroupText('.'),
                 dbc.Select(options=[{'label': extension, 'value': extension}
                                     for extension in ['JSON']],
                            value='JSON',
                            id={'type': '03-generate-layered-aspic-extension',
                                'index': nr_clicks}),
                 dbc.Button('Download', id={
                     'type': '03-generate-layered-aspic-download-button',
                     'index': nr_clicks}),
             ]),
             dcc.Download(id={'type': '03-generate-layered-aspic-downloader',
                              'index': nr_clicks})
         ])
         ]

    return output_children


@callback(
    Output({'type': '03-generate-layered-aspic-downloader', 'index': MATCH},
           'data'),
    Input({'type': '03-generate-layered-aspic-download-button',
           'index': MATCH},
          'n_clicks'),
    State(
        {'type': '03-generate-layered-aspic-download-content', 'index': MATCH},
        'data'),
    State({'type': '03-generate-layered-aspic-filename', 'index': MATCH},
          'value'),
    State({'type': '03-generate-layered-aspic-extension', 'index': MATCH},
          'value'),
    prevent_initial_call=True,
)
def download_generated_argumentation_system(
        _nr_clicks: int, argumentation_system_data, filename: str,
        extension: str):
    if extension == 'JSON':
        return {'content': argumentation_system_data,
                'filename': filename + '.' + extension}
    return NotImplementedError
