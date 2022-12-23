import dash_bootstrap_components as dbc
import visdcc
from dash import html, dcc


def get_abstract_layout(abstract_evaluation, abstract_explanation, abstract_setting):
    layout_abstract = html.Div([
        html.Div([
            html.Div([
                dbc.CardHeader(dbc.Button("Abstract Argumentation Setting", className='pyarg-button',
                                          id="abstract-arg-setting-button")),
                dbc.Collapse(dbc.CardBody(abstract_setting), id="abstract-arg-setting-collapse", is_open=False),

                dbc.CardHeader(dbc.Button("Evaluation", className='pyarg-button', id="abstract-evaluation-button")),
                dbc.Collapse(dbc.CardBody(abstract_evaluation), id="abstract-evaluation-collapse", is_open=False),

                dbc.CardHeader(dbc.Button("Explanation", className='pyarg-button', id="abstract-explanation-button")),
                dbc.Collapse(dbc.CardBody(abstract_explanation), id="abstract-explanation-collapse", is_open=False),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                visdcc.Network(data={'nodes': [], 'edges': []}, id='abstract-argumentation-graph',
                               options={'height': '600px'}, style={'border-radius': '8px',
                                                                   'border': '2px solid #152A47',
                                                                   'margin-right': '25px'}),
                html.Div([
                    html.Div([
                        html.Div(id='abstract-arguments-output', className='output'),
                        html.Div(id='abstract-evaluation', className='output'),
                        html.Div(id='abstract-explanation', className='output')
                    ], className='row-container'),
                    html.Div([
                        html.Div(id='abstract-argumentation-graph-output', className='output'),
                        html.Div(id='abstract-argumentation-graph-evaluation', className='output'),
                        html.Div(id='abstract-argumentation-graph-explanation', className='output')
                    ], className='row-container')
                ])
            ], style={'padding': 10, 'flex': 1}),
        ], className='row-container')
    ])
    return layout_abstract


def get_abstract_explanation():
    abstract_explanation = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.B('Type'),
                    dcc.RadioItems(options=[{'label': 'Acceptance', 'value': 'Acceptance'},
                                            {'label': 'Non-Acceptance', 'value': 'NonAcceptance'}],
                                   value='', id='abstract-explanation-type', style={'margin-top': '10px'},
                                   inputStyle={'margin-right': '6px'})
                ]),

                html.Div([
                    html.B('Strategy'),
                    dcc.RadioItems(options=[{'label': 'Credulous', 'value': 'Credulous'},
                                            {'label': 'Skeptical', 'value': 'Skeptical'}],
                                   value='', id='abstract-explanation-strategy', style={'margin-top': '10px'},
                                   inputStyle={'margin-right': '6px'})
                ], style={'margin-top': '20px'}),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Explanation function'),
                dcc.RadioItems(id='abstract-explanation-function',
                               style={'margin-top': '10px'},
                               inputStyle={'margin-right': '6px'})
            ], style={'padding': 10, 'flex': 1}),

        ], className='row-container'),

        html.Div([html.Button('Derive Explanations', id='abstract-explanation-button', n_clicks=0,
                              className='small-pyarg-button')], style={'text-align': 'left', 'margin-left': '10px'}),
        html.Div(style={'whiteSpace': 'pre-line'}),
    ])
    return abstract_explanation


def get_abstract_evaluation():
    abstract_evaluation = html.Div([
        html.Div([
            html.Div([
                html.B('Semantics'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Admissible', 'value': 'Admissible'},
                        {'label': 'Complete', 'value': 'Complete'},
                        {'label': 'Grounded', 'value': 'Grounded'},
                        {'label': 'Preferred', 'value': 'Preferred'},
                        {'label': 'Ideal', 'value': 'Ideal'},
                        {'label': 'Stable', 'value': 'Stable'},
                        {'label': 'Semi-stable', 'value': 'SemiStable'},
                        {'label': 'Eager', 'value': 'Eager'},
                    ],
                    value='Complete', id='abstract-evaluation-semantics',
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Evaluation strategy'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ],
                    value='Credulous',
                    id='abstract-evaluation-strategy',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'padding': 10, 'flex': 1}),
        ], className='row-container'),

        html.Div(
            [html.Button('Evaluate AF', id='evaluate-argumentation-framework-button', n_clicks=0,
                         className='small-pyarg-button')],
            style={'text-align': 'left', 'margin-left': '10px'}
        ),

        html.Div(style={'whiteSpace': 'pre-line'}),
    ])
    return abstract_evaluation


def get_abstract_setting():
    abstract_setting = html.Div(children=[
        html.Div([
            html.Div([
                html.B('Arguments'),
                html.Br(),
                dcc.Textarea(id='abstract-arguments', placeholder='Add one argument per line. For example:\n A\n B\n C',
                             value='', className='abstract-input'),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Attacks'),
                html.Br(),
                dcc.Textarea(id='abstract-attacks',
                             placeholder='Add one attack per line. For example: \n (A,B) \n (A,C) \n (C,B)',
                             value='', className='abstract-input'),
            ], style={'padding': 10, 'flex': 1}),
        ], className='row-container'),

        html.Div(
            [html.Button('Create AF', id='create-argumentation-framework-button', n_clicks=0,
                         className='small-pyarg-button')],
            style={'text-align': 'left', 'margin-left': '10px'}
        ),

        html.Div(style={'whiteSpace': 'pre-line'})
    ])
    return abstract_setting
