import json
from typing import List

import dash
from dash import html, callback, Input, Output, State, MATCH, dcc
import dash_bootstrap_components as dbc

from py_arg.abstract_argumentation.classes.abstract_argumentation_framework \
    import AbstractArgumentationFramework
from py_arg.abstract_argumentation.classes.argument import Argument
from py_arg.abstract_argumentation.classes.defeat import Defeat
from py_arg.abstract_argumentation.generators.\
    abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator
from py_arg.abstract_argumentation.import_export.\
    argumentation_framework_to_aspartix_format_writer import \
    ArgumentationFrameworkToASPARTIXFormatWriter
from py_arg.abstract_argumentation.import_export.\
    argumentation_framework_to_iccma23_format_writer import \
    ArgumentationFrameworkToICCMA23FormatWriter
from py_arg.abstract_argumentation.import_export.\
    argumentation_framework_to_json_writer import \
    ArgumentationFrameworkToJSONWriter
from py_arg.abstract_argumentation.import_export.\
    argumentation_framework_to_trivial_graph_format_writer import \
    ArgumentationFrameworkToTrivialGraphFormatWriter

dash.register_page(__name__, name='GenerateAbstract',
                   title='Generate Abstract AF')

left_column = dbc.Col([
    html.H2('Input'),
    html.Br(),
    dbc.Row([dbc.Col(html.B('Number of arguments')),
             dbc.Col(dbc.Input(
                 type='number', min=0, max=50, step=1, value=8,
                 id='01-generate-abstract-nr-arguments-input'))]),
    dbc.Row([dbc.Col(html.B('Number of defeats')),
             dbc.Col(dbc.Input(
                 type='number', min=0, max=50, step=1, value=8,
                 id='01-generate-abstract-nr-defeats-input'))]),
    dbc.Row([dbc.Col(html.B('Allow self-defeats')),
             dbc.Col(dbc.Select(
                 options=[{'label': answer, 'value': answer}
                          for answer in ['Yes', 'No']],
                 value='Yes',
                 id='01-generate-abstract-allow-self-defeats-input'))
             ]),
    html.Br(),
    dbc.Row([dbc.Button('Generate', id='01-generate-abstract-button',
                        className='w-50 mx-auto')])
])
right_column = dbc.Col([], id='01-generate-abstract-output')
layout_generate_abstract = dbc.Row([left_column, right_column])

layout = html.Div([
    html.H1('Generate Random Abstract Argumentation Framework'),
    html.Div(layout_generate_abstract)
])


@callback(Output('01-generate-abstract-output', 'children'),
          Input('01-generate-abstract-button', 'n_clicks'),
          State('01-generate-abstract-nr-arguments-input', 'value'),
          State('01-generate-abstract-nr-defeats-input', 'value'),
          State('01-generate-abstract-allow-self-defeats-input', 'value'))
def generate_abstract_argumentation_framework(
        nr_clicks: int, nr_arguments: str, nr_defeats: str,
        allow_self_defeats: str):
    if not nr_clicks:
        return 'Press the button to generate an argumentation framework.'

    try:
        nr_arguments_int = int(nr_arguments)
    except TypeError:
        return 'The number of arguments is not an integer.'
    if nr_arguments_int < 1:
        return 'The number of arguments should be at least one.'

    try:
        nr_defeats_int = int(nr_defeats)
    except TypeError:
        return 'The number of defeats is not an integer.'
    if nr_defeats_int < 0:
        return 'The number of defeats cannot be negative.'

    allow_self_defeats_bool = allow_self_defeats == 'Yes'

    generator = AbstractArgumentationFrameworkGenerator(
        nr_of_arguments=nr_arguments_int,
        nr_of_defeats=nr_defeats_int,
        allow_self_defeats=allow_self_defeats_bool
    )
    argumentation_framework = generator.generate()

    output_children = \
        [html.H2('Output'),
         dbc.Row([
             dbc.Col([html.B('Arguments'), dbc.Textarea(
                 value='\n'.join(str(arg)
                                 for arg in argumentation_framework.arguments),
                 style={'height': '300px'},
                 id={'type': '01-generate-abstract-arguments-text',
                     'index': nr_clicks})]),
             dbc.Col([html.B('Defeats'), dbc.Textarea(
                 value='\n'.join(
                     (f'({str(defeat.from_argument)},'
                      f'{str(defeat.to_argument)})'
                      for defeat in argumentation_framework.defeats)),
                 style={'height': '300px'},
                 id={'type': '01-generate-abstract-defeats-text',
                     'index': nr_clicks})])
         ]),
         html.Br(),
         dbc.Row([
             dbc.InputGroup([
                 dbc.InputGroupText('Filename'),
                 dbc.Input(value='generated_af',
                           id={'type': '01-generate-abstract-filename',
                               'index': nr_clicks}),
                 dbc.InputGroupText('.'),
                 dbc.Select(options=[{'label': extension, 'value': extension}
                                     for extension in ['JSON', 'TGF', 'APX',
                                                       'ICCMA23']],
                            value='JSON',
                            id={'type': '01-generate-abstract-extension',
                                'index': nr_clicks}),
                 dbc.Button('Download',
                            id={'type': '01-generate-abstract-download-button',
                                'index': nr_clicks}),
             ]),
             dcc.Download(id={'type': '01-generate-abstract-downloader',
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
    Output({'type': '01-generate-abstract-downloader', 'index': MATCH},
           'data'),
    Input({'type': '01-generate-abstract-download-button', 'index': MATCH},
          'n_clicks'),
    State({'type': '01-generate-abstract-arguments-text', 'index': MATCH},
          'value'),
    State({'type': '01-generate-abstract-defeats-text', 'index': MATCH},
          'value'),
    State({'type': '01-generate-abstract-filename', 'index': MATCH}, 'value'),
    State({'type': '01-generate-abstract-extension', 'index': MATCH}, 'value'),
    prevent_initial_call=True,
)
def download_generated_abstract_argumentation_framework(
        _nr_clicks: int, arguments_text: str, defeats_text: str, filename: str,
        extension: str):
    argumentation_framework = AbstractArgumentationFramework(
        name='generated',
        arguments=[Argument(arg_str.strip())
                   for arg_str in arguments_text.split('\n')],
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
