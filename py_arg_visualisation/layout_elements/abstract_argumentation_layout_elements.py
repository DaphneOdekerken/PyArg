import dash_bootstrap_components as dbc
import visdcc
from dash import html, dcc


def get_abstract_layout(abstract_evaluation, abstract_explanation, abstract_setting):
    left_column = dbc.Col(
        dbc.Accordion([
            dbc.AccordionItem(abstract_setting, title='Abstract Argumentation Setting'),
            dbc.AccordionItem(abstract_evaluation, title='Evaluation', item_id='Evaluation'),
            dbc.AccordionItem(abstract_explanation, title='Explanation')
        ], id='abstract-evaluation-accordion')
    )
    right_column = dbc.Col([
        dbc.Row([
            dbc.Card(visdcc.Network(data={'nodes': [], 'edges': []}, id='abstract-argumentation-graph',
                                    options={'height': '500px'}), body=True),
            html.Div([
                html.Div([
                    html.Div(id='abstract-argumentation-graph-evaluation'),
                    html.Div(id='abstract-argumentation-graph-explanation')
                ], className='row-container')
            ])
        ])
    ])
    layout_abstract = dbc.Row([left_column, right_column])
    return html.Div([html.H1('Visualisation of abstract argumentation frameworks'), layout_abstract])


def get_abstract_explanation_div():
    abstract_explanation = html.Div([
        dbc.Row([
            html.B('Type'),
            dbc.Select(options=[{'label': 'Acceptance', 'value': 'Acceptance'},
                                {'label': 'Non-Acceptance', 'value': 'NonAcceptance'}],
                       value='Acceptance', id='abstract-explanation-type'),
            html.B('Strategy'),
            dbc.Select(options=[{'label': 'Credulous', 'value': 'Credulous'},
                                {'label': 'Skeptical', 'value': 'Skeptical'}],
                       value='Credulous', id='abstract-explanation-strategy'),
            html.B('Explanation function'),
            dbc.Select(id='abstract-explanation-function')
            ]),
        dbc.Row([dbc.Button('Derive Explanations', id='abstract-explanation-button', n_clicks=0)]),
        dbc.Row(id='abstract-explanation')
    ])
    return abstract_explanation


def get_abstract_evaluation_div():
    abstract_evaluation = html.Div([
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
                ], value='Complete', id='abstract-evaluation-semantics')),
            ]),

            dbc.Row([
                dbc.Col(html.B('Evaluation strategy')),
                dbc.Col(dbc.Select(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ], value='Credulous', id='abstract-evaluation-strategy')),
            ]),
            dbc.Row(id='abstract-evaluation')
        ]),
    ])
    return abstract_evaluation


def get_abstract_setting_specification_div():
    abstract_setting = html.Div(children=[
        dcc.Store(id='selected-argument-store-abstract'),
        dbc.Col([
            dbc.Row(dbc.Button('Generate random', id='generate-random-af-button', n_clicks=0)),
            dbc.Row([
                dbc.Col([
                    html.B('Arguments'),
                    dbc.Textarea(id='abstract-arguments',
                                 placeholder='Add one argument per line. For example:\n A\n B\n C',
                                 value='', style={'height': '300px'})
                ]),
                dbc.Col([
                    html.B('Attacks'),
                    dbc.Textarea(id='abstract-attacks',
                                 placeholder='Add one attack per line. For example: \n (A,B) \n (A,C) \n (C,B)',
                                 value='', style={'height': '300px'}),
                ])
            ])
        ])
    ])
    return abstract_setting
