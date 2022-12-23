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
                        id="abstract-arg-setting-button",
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(abstract_setting),
                    id="abstract-arg-setting-collapse", is_open=False
                ),

                dbc.CardHeader(
                    dbc.Button(
                        "Evaluation",
                        style={'color': '#152A47',
                               'text-align': 'left',
                               'background-color': '#7BE7FF',
                               'border-color': '#7BE7FF',
                               'width': '100%'},
                        id="abstract-evaluation-button",
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(abstract_evaluation),
                    id="abstract-evaluation-collapse", is_open=False
                ),

                dbc.CardHeader(
                    dbc.Button(
                        "Explanation",
                        style={'color': '#152A47',
                               'text-align': 'left',
                               'background-color': '#7BE7FF',
                               'border-color': '#7BE7FF',
                               'width': '100%'},
                        id="abstract-explanation-button",
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(abstract_explanation),
                    id="abstract-explanation-collapse", is_open=False
                ),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                visdcc.Network(data={'nodes': [], 'edges': []},
                               id='abstract-argumentation-graph',
                               options=dict(height='600px'),
                               style={'border-radius': '8px',
                                      'border': '2px solid #152A47',
                                      'margin-right': '25px'}),
                html.Div([
                    html.Div([
                        html.Div(
                            id='abstract-arguments-output',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                        html.Div(
                            id='abstract-evaluation',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                        ),

                        html.Div(
                            id='abstract-explanation',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                        )
                    ], style={'display': 'flex', 'flex-direction': 'row'}),

                    html.Div([
                        html.Div(
                            id='abstract-argumentation-graph-output',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                        html.Div(
                            id='abstract-argumentation-graph-evaluation',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                        ),

                        html.Div(
                            id='abstract-argumentation-graph-explanation',
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
                            {'label': 'Acceptance', 'value': 'Acceptance'},
                            {'label': 'Non-Acceptance', 'value': 'NonAcceptance'}
                        ],
                        value='',
                        id='abstract-explanation-type',
                        style={'margin-top': '10px'},
                        inputStyle={'margin-right': '6px'}
                    ),
                ]),

                html.Div([
                    html.B('Strategy'),

                    dcc.RadioItems(
                        options=[
                            {'label': 'Credulous', 'value': 'Credulous'},
                            {'label': 'Skeptical', 'value': 'Skeptical'}
                        ],
                        value='',
                        id='abstract-explanation-strategy',
                        style={'margin-top': '10px'},
                        inputStyle={'margin-right': '6px'}
                    ),
                ], style={'margin-top': '20px'}),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Explanation function'),

                dcc.RadioItems(
                    id='abstract-explanation-function',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'padding': 10, 'flex': 1}),

        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div(
            [html.Button('Derive Explanations', id='abstract_explanation_button', n_clicks=0)],
            style={'text-align': 'left', 'margin-left': '10px'}
        ),

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
                    value='Complete',
                    id='abstract-evaluation-semantics',
                    style={'margin-top': '10px'},
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
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div(
            [html.Button('Evaluate AF', id='evaluate-argumentation-framework-button', n_clicks=0)],
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
            [html.Button('Create AF', id='create-argumentation-framework-button', n_clicks=0)],
            style={'text-align': 'left', 'margin-left': '10px'}
        ),

        html.Div(id='abstract-argumentation', style={'whiteSpace': 'pre-line'})
    ])
    return abstract_setting
