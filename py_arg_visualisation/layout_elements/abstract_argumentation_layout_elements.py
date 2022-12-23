import dash_bootstrap_components as dbc
import visdcc
from dash import html, dcc


def get_abstract_layout(abstract_evaluation, abstract_explanation, abstract_setting):
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
                    dbc.CardBody(abstract_evaluation),
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
                    dbc.CardBody(abstract_explanation),
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
    return layout_abstract


def get_abstract_explanation():
    abstract_explanation = html.Div([
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
    return abstract_explanation


def get_abstract_evaluation():
    abstract_evaluation = html.Div([
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
            [html.Button('Evaluate AF', id='abstrAF-Eval', n_clicks=0)],
            style={'text-align': 'left', 'margin-left': '10px'}
        ),

        html.Div(id='abstrAF-evaluation', style={'whiteSpace': 'pre-line'}),
    ])
    return abstract_evaluation


def get_abstract_setting():
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
            [html.Button('Create AF', id='abstrAF-Calc', n_clicks=0)],
            style={'text-align': 'left', 'margin-left': '10px'}
        ),

        html.Div(id='abstract-argumentation', style={'whiteSpace': 'pre-line'})
    ])
    return abstract_setting
