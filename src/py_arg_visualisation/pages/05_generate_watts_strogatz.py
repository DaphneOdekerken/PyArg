import json
from typing import List

import dash
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State, MATCH, dcc

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.generators.watts_strogatz_generator \
    import WattsStrogatz
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_aspartix_format_writer import \
    ArgumentationFrameworkToASPARTIXFormatWriter
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_iccma23_format_writer import \
    ArgumentationFrameworkToICCMA23FormatWriter
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_json_writer import \
    ArgumentationFrameworkToJSONWriter
from py_arg.abstract_argumentation.import_export. \
    argumentation_framework_to_trivial_graph_format_writer import \
    ArgumentationFrameworkToTrivialGraphFormatWriter

dash.register_page(__name__, name='GenerateWattsStrogatz',
                   title='Generate Watts-Strogatz AF')

left_column = dbc.Col([
    html.H2('Input'),
    html.Br(),
    dbc.Row([dbc.Col(html.B('Number of arguments')),
             dbc.Col(dbc.Input(
                 type='number', min=0, max=50, step=1, value=8,
                 id='05-generate-watts-strogatz-nr-arguments-input'))]),
    dbc.Row([dbc.Col(html.B('Number of neighbours to join')),
             dbc.Col(dbc.Input(
                 type='number', min=0, max=50, step=1, value=8,
                 id='05-generate-watts-strogatz-nr-join-neighbours-input'))]),
    dbc.Row([dbc.Col(html.B('Use Seed')),
             dbc.Col(dbc.Select(
                 options=[{'label': answer, 'value': answer} for answer in
                          ['Yes', 'No']],
                 value='No',
                 id='05-generate-watts-strogatz-use-seed-input'))]),
    dbc.Row([dbc.Col(html.B('Seed')),
             dbc.Col(dbc.Input(type='number', min=0, max=128, step=1, value=42,
                               id='05-generate-watts-strogatz-seed-input'))]),
    dbc.Row([dbc.Col(html.B('Probability of defeat rewiring')),
             dbc.Col(dcc.Slider(
                 min=0.1, max=1, step=0.1, value=0.5, marks=None,
                 tooltip={"placement": "bottom",
                          "always_visible": True},
                 id='05-generate-watts-strogatz-prob-defeat-rewiring-input'))
             ]),
    dbc.Row([dbc.Col(html.B('Probability of argument in cycle')),
             dbc.Col(dcc.Slider(
                 min=0.1, max=1, step=0.1, value=0.5, marks=None,
                 tooltip={"placement": "bottom",
                          "always_visible": True},
                 id='05-generate-watts-strogatz-prob-cycle-input'))]),
    html.Br(),
    dbc.Row([dbc.Button('Generate', id='05-generate-watts-strogatz-button',
                        className='w-50 mx-auto')])
])
right_column = dbc.Col([], id='05-generate-watts-strogatz-output')
layout_generate_abstract = dbc.Row([left_column, right_column])

layout = html.Div([
    html.H1('Generate Random Watts-Strogatz Abstract Argumentation Framework'),
    html.Div(layout_generate_abstract)
])


@callback(Output('05-generate-watts-strogatz-output', 'children'),
          Input('05-generate-watts-strogatz-button', 'n_clicks'),
          State('05-generate-watts-strogatz-nr-arguments-input', 'value'),
          State('05-generate-watts-strogatz-nr-join-neighbours-input',
                'value'),
          State('05-generate-watts-strogatz-seed-input', 'value'),
          State('05-generate-watts-strogatz-use-seed-input', 'value'),
          State('05-generate-watts-strogatz-prob-defeat-rewiring-input',
                'value'),
          State('05-generate-watts-strogatz-prob-cycle-input', 'value'))
def generate_abstract_argumentation_framework(
        nr_clicks: int, nr_arguments: str, nr_join_neighbours: str, seed: str,
        use_seed: str, prob_rewiring: str, prob_cycle: str):
    if not nr_clicks:
        return 'Press the button to generate an argumentation framework.'

    try:
        nr_arguments_int = int(nr_arguments)
    except TypeError:
        return 'The number of arguments is not an integer.'
    if nr_arguments_int < 1:
        return 'The number of arguments should be at least one.'

    try:
        seed_int = int(seed)
    except TypeError:
        return 'The seed value is not an integer.'

    prob_rewiring_float = float(prob_rewiring)
    prob_cycle_float = float(prob_cycle)
    nr_join_neighbours_int = int(nr_join_neighbours)

    if use_seed == 'No':
        seed_int = None

    generator = WattsStrogatz(nr_of_arguments=nr_arguments_int,
                              nr_join_neighbours=nr_join_neighbours_int,
                              prob_edge_rewiring=prob_rewiring_float,
                              prob_cycle=prob_cycle_float, seed=seed_int)
    argumentation_framework = generator.generate()

    output_children = \
        [html.H2('Output'),
         dbc.Row([
             dbc.Col([html.B('Arguments'), dbc.Textarea(
                 value='\n'.join(
                     str(arg) for arg in argumentation_framework.arguments),
                 style={'height': '300px'},
                 id={'type': '05-generate-watts-strogatz-arguments-text',
                     'index': nr_clicks})]),
             dbc.Col([html.B('Defeats'), dbc.Textarea(
                 value='\n'.join(
                     (f'({str(defeat.from_argument)},'
                      f'{str(defeat.to_argument)})'
                      for defeat in argumentation_framework.defeats)),
                 style={'height': '300px'},
                 id={'type': '05-generate-watts-strogatz-defeats-text',
                     'index': nr_clicks})])
         ]),
         html.Br(),
         dbc.Row([
             dbc.InputGroup([
                 dbc.InputGroupText('Filename'),
                 dbc.Input(value='generated_ws_af',
                           id={'type': '05-generate-watts-strogatz-filename',
                               'index': nr_clicks}),
                 dbc.InputGroupText('.'),
                 dbc.Select(options=[{'label': extension, 'value': extension}
                                     for extension in
                                     ['JSON', 'TGF', 'APX', 'ICCMA23']],
                            value='JSON',
                            id={'type': '05-generate-watts-strogatz-extension',
                                'index': nr_clicks}),
                 dbc.Button('Download', id={
                     'type': '05-generate-watts-strogatz-download-button',
                     'index': nr_clicks}),
             ]),
             dcc.Download(id={'type': '05-generate-watts-strogatz-downloader',
                              'index': nr_clicks})
         ])
         ]

    return output_children


def read_defeats(defeat_text: str) -> List[Defeat]:
    defeat_text_lines = defeat_text.split('\n')
    result = []
    for defeat_text_line in defeat_text_lines:
        defeat_text_line = defeat_text_line.replace('(', '')
        defeat_text_line = defeat_text_line.replace(')', '')
        from_str, to_str = defeat_text_line.split(',')
        from_arg = Argument(from_str.strip())
        to_arg = Argument(to_str.strip())
        result.append(Defeat(from_arg, to_arg))
    return result


@callback(
    Output({'type': '05-generate-watts-strogatz-downloader', 'index': MATCH},
           'data'),
    Input(
        {'type': '05-generate-watts-strogatz-download-button', 'index': MATCH},
        'n_clicks'),
    State({'type': '05-generate-watts-strogatz-arguments-text',
           'index': MATCH}, 'value'),
    State({'type': '05-generate-watts-strogatz-defeats-text', 'index': MATCH},
          'value'),
    State({'type': '05-generate-watts-strogatz-filename', 'index': MATCH},
          'value'),
    State({'type': '05-generate-watts-strogatz-extension', 'index': MATCH},
          'value'),
    prevent_initial_call=True,
)
def download_generated_abstract_argumentation_framework(
        _nr_clicks: int, arguments_text: str, defeats_text: str, filename: str,
        extension: str):
    argumentation_framework = AbstractArgumentationFramework(
        name='generated',
        arguments=[Argument(arg_str.strip()) for arg_str in
                   arguments_text.split('\n')],
        defeats=read_defeats(defeats_text)
    )

    if extension == 'JSON':
        argumentation_framework_json = \
            ArgumentationFrameworkToJSONWriter().to_dict(
                argumentation_framework)
        argumentation_framework_str = json.dumps(argumentation_framework_json)
    elif extension == 'TGF':
        argumentation_framework_str = \
            ArgumentationFrameworkToTrivialGraphFormatWriter.write_to_str(
                argumentation_framework)
    elif extension == 'APX':
        argumentation_framework_str = \
            ArgumentationFrameworkToASPARTIXFormatWriter.write_to_str(
                argumentation_framework)
    elif extension == 'ICCMA23':
        argumentation_framework_str = \
            ArgumentationFrameworkToICCMA23FormatWriter.write_to_str(
                argumentation_framework)
    else:
        raise NotImplementedError

    return {'content': argumentation_framework_str,
            'filename': filename + '.' + extension}
