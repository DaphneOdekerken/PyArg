from typing import Dict, List

import dash
import visdcc
from dash import html, callback, Input, Output, State, ALL, dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_interactive_graphviz

from py_arg.incomplete_argumentation_frameworks.classes.\
    incomplete_argumentation_framework import IncompleteArgumentationFramework
from py_arg_visualisation.functions.graph_data_functions.get_iaf_graph_data \
    import get_iaf_graph_data
from py_arg_visualisation.functions.import_functions.read_iaf_functions \
    import read_incomplete_argumentation_framework

dash.register_page(__name__, name='Visualise AF', title='Visualise AF')


def get_abstract_setting_specification_div():
    return html.Div(children=[
        dcc.Store(id='24-selected-argument-store-iaf'),
        dbc.Col([
            dbc.Row([dbc.Col(dbc.Button(
                'Generate random',
                id='24-generate-random-af-button', n_clicks=0,
                className='w-100')),
                dbc.Col(dcc.Upload(dbc.Button(
                    'Open existing IAF', className='w-100'),
                    id='24-upload-iaf'))
            ], className='mt-2'),
            dbc.Row([
                dbc.Col([
                    html.B('Certain arguments'),
                    dbc.Textarea(
                        id='24-certain-arguments',
                        placeholder='Add one argument per line. '
                                    'For example:\n A\n B',
                        value='', style={'height': '150px'})
                ]),
                dbc.Col([
                    html.B('Certain attacks'),
                    dbc.Textarea(
                        id='24-certain-attacks',
                        placeholder='Add one attack per line. '
                                    'For example: \n (A,B) \n (A,C)',
                        value='', style={'height': '150px'}),
                ])
            ], className='mt-2'),
            dbc.Row([
                dbc.Col([
                    html.B('Uncertain arguments'),
                    dbc.Textarea(
                        id='24-uncertain-arguments',
                        placeholder='Add one argument per line. '
                                    'For example:\n C',
                        value='', style={'height': '150px'})
                ]),
                dbc.Col([
                    html.B('Uncertain attacks'),
                    dbc.Textarea(
                        id='24-uncertain-attacks',
                        placeholder='Add one attack per line. '
                                    'For example: \n (C,B)',
                        value='', style={'height': '150px'}),
                ])
            ], className='mt-2'),
            dbc.Row([
                dbc.InputGroup([
                    dbc.InputGroupText('Filename'),
                    dbc.Input(value='edited_iaf', id='24-iaf-filename'),
                    dbc.InputGroupText('.'),
                    dbc.Select(
                        options=[{'label': extension, 'value': extension}
                                 for extension in ['JSON', 'TGF', 'APX',
                                                   'ICCMA23']],
                        value='JSON', id='24-iaf-extension'),
                    dbc.Button('Download', id='24-iaf-download-button'),
                ], className='mt-2'),
                dcc.Download(id='24-iaf-download')
            ])
        ])
    ])


def get_abstract_evaluation_div():
    return html.Div([
        html.Div([
            dbc.Row([
                dbc.Col(html.B('Semantics')),
                dbc.Col(dbc.Select(options=[
                    {'label': 'Complete', 'value': 'Complete'},
                    {'label': 'Grounded', 'value': 'Grounded'}
                ], value='Grounded', id='24-iaf-evaluation-semantics')),
            ]),

            dbc.Row([
                dbc.Col(html.B('Evaluation strategy')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ], value='Credulous', id='24-iaf-evaluation-strategy')),
            ]),
            dbc.Row(id='24-iaf-evaluation')
        ]),
    ])


left_column = dbc.Col(
    dbc.Accordion([
        dbc.AccordionItem(get_abstract_setting_specification_div(),
                          title='Incomplete Argumentation Framework',
                          item_id='IAF'),
        dbc.AccordionItem(get_abstract_evaluation_div(),
                          title='Evaluation', item_id='Evaluation'),
    ], id='24-iaf-evaluation-accordion')
)

right_column = dbc.Col([
    dbc.Row([
        dbc.Card(
            visdcc.Network(data={'nodes': [], 'edges': []},
                           id='24-iaf-argumentation-graph',
                           options={'height': '500px'}))
    ])])

layout_iaf = dbc.Row([left_column, right_column])
layout = html.Div([html.H1(
    'Visualisation of incomplete argumentation frameworks'), layout_iaf])


@callback(
    Output('24-iaf-argumentation-graph', 'data'),
    Input('24-certain-arguments', 'value'),
    Input('24-certain-attacks', 'value'),
    Input('24-uncertain-arguments', 'value'),
    Input('24-uncertain-attacks', 'value'),
    Input('24-selected-argument-store-iaf', 'data'),
    Input('color-blind-mode', 'on'),
    Input('24-iaf-evaluation-accordion', 'active_item'),
    prevent_initial_call=True
)
def create_abstract_argumentation_framework(
        certain_arguments: str, certain_attacks: str,
        uncertain_arguments: str, uncertain_attacks: str,
        selected_arguments: Dict[str, List[str]],
        color_blind_mode: bool, active_item: str):
    """
    Send the IAF data to the graph for plotting.
    """

    # Read the argumentation framework; in case of an error, display nothing.
    try:
        iaf = read_incomplete_argumentation_framework(
            certain_arguments, certain_attacks,
            uncertain_arguments, uncertain_attacks)
    except ValueError:
        iaf = IncompleteArgumentationFramework()

    # Do not display colors if the IAF tab is open.
    if active_item == 'IAF':
        selected_arguments = None

    data = get_iaf_graph_data(iaf, selected_arguments, color_blind_mode)

    return data
