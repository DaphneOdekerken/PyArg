import dash_bootstrap_components as dbc
import visdcc
from dash import html, dcc


def get_aspic_layout(ASPIC_setting, structured_evaluation, structured_explanation):
    layout_ASPIC = html.Div([
        html.Div([
            html.Div([
                dbc.CardHeader(
                    dbc.Button(
                        "ASPIC Argumentation Setting",
                        style={'color': '#152A47',
                               'text-align': 'left',
                               'background-color': '#7BE7FF',
                               'border-color': '#7BE7FF',
                               'width': '100%'},
                        id="str-arg-setting-button",
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(ASPIC_setting),
                    id="str-arg-setting-collapse", is_open=False
                ),

                dbc.CardHeader(
                    dbc.Button(
                        "Evaluation",
                        style={'color': '#152A47',
                               'text-align': 'left',
                               'background-color': '#7BE7FF',
                               'border-color': '#7BE7FF',
                               'width': '100%'},
                        id="str-evaluation-button",
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(structured_evaluation),
                    id="str-evaluation-collapse", is_open=False
                ),

                dbc.CardHeader(
                    dbc.Button(
                        "Explanation",
                        style={'color': '#152A47',
                               'text-align': 'left',
                               'background-color': '#7BE7FF',
                               'border-color': '#7BE7FF',
                               'width': '100%'},
                        id="str-explanation-button",
                    )
                ),
                dbc.Collapse(
                    dbc.CardBody(structured_explanation),
                    id="str-explanation-collapse", is_open=False
                ),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                visdcc.Network(data={'nodes': [], 'edges': []},
                               id='strnet',
                               options=dict(height='600px'),
                               style={'border-radius': '8px',
                                      'border': '2px solid #152A47',
                                      'margin-right': '25px'}),
                html.Div([
                    html.Div([
                        html.Div(
                            id='str-output',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                        html.Div(
                            id='str-evaluation',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                        ),

                        html.Div(
                            id='str-explanation',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                        )
                    ], style={'display': 'flex', 'flex-direction': 'row'}),

                    html.Div([
                        html.Div(
                            id='strnet-output',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}),

                        html.Div(
                            id='strnet-evaluation',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                        ),

                        html.Div(
                            id='strnet-explanation',
                            style={'text-align': 'left', 'margin-left': '10px', 'padding': 10, 'flex': 1}
                        )

                    ], style={'display': 'flex', 'flex-direction': 'row'})
                ])
            ], style={'padding': 10, 'flex': 1}),
        ], style={'display': 'flex', 'flex-direction': 'row'})
    ])
    return layout_ASPIC


def get_structured_explanation():
    structured_explanation = html.Div([
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
                        id='str-explanation-type',
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
                        id='str-explanation-strategy',
                        style={'margin-top': '10px'},
                        inputStyle={'margin-right': '6px'}
                    ),
                ], style={'margin-top': '20px'}),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.Div([
                    html.B('Explanation function'),

                    dcc.RadioItems(

                        id='str-explanation-function',
                        style={'margin-top': '10px'},
                        inputStyle={'margin-right': '6px'}
                    ),
                ]),

                html.Div([
                    html.B('Explanation form'),

                    dcc.RadioItems(
                        options=[
                            {'label': 'Argument', 'value': 'Arg'},
                            {'label': 'Premises', 'value': 'Prem'},
                            {'label': 'Rules', 'value': 'Rule'},
                            {'label': 'Sub-arguments', 'value': 'SubArg'},
                            {'label': 'Sub-argument conclusions', 'value': 'SubArgConc'}
                        ],
                        id='str-explanation-form',
                        style={'margin-top': '10px'},
                        inputStyle={'margin-right': '6px'}
                    ),
                ], style={'margin-top': '20px'}),

            ], style={'padding': 10, 'flex': 1})

        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div(
            [html.Button('Derive Explanations', id='strAF-Expl', n_clicks=0)], style={'text-align': 'left',
                                                                                      'margin-left': '10px'}
        ),

        html.Div(id='strAF-explanation', style={'whiteSpace': 'pre-line'}),
    ])
    return structured_explanation


def get_structured_evaluation():
    structured_evaluation = html.Div([
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
                    id='str-evaluation-semantics',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Evaluation strategy'),

                dcc.RadioItems(
                    options=[
                        {'label': 'Credulous', 'value': 'Cred'},
                        {'label': 'Weakly Skeptical', 'value': 'WSkep'},
                        {'label': 'Skeptical', 'value': 'Skep'}
                    ],
                    value='',
                    id='str-evaluation-strategy',
                    style={'margin-top': '10px'},
                    inputStyle={'margin-right': '6px'}
                ),
            ], style={'padding': 10, 'flex': 1}),
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div(
            [html.Button('Evaluate AF', id='strAF-Eval', n_clicks=0)],
            style={'text-align': 'left', 'margin-left': '10px'}
        ),

        html.Div(id='strAF-evaluation', style={'whiteSpace': 'pre-line'}),
    ])
    return structured_evaluation


def get_aspic_setting():
    ASPIC_setting = html.Div(children=[
        html.Div([
            html.Div([
                html.B('Axioms'),
                html.Br(),
                dcc.Textarea(
                    id='aspic-axioms',
                    placeholder='Add one axiom per line. For example:\n p \n -q \n ~r',
                    value='',
                    style={'height': 150, 'margin-top': '10px'}, ),
            ], style={'padding': 10, 'flex': 1, 'margin-left': '10px'}),

            html.Div([
                html.B('Ordinary premises'),
                html.Br(),
                dcc.Textarea(
                    id='aspic-ordinary-premises',
                    placeholder='Add one ordinary premise per line. For example:\n p \n -q \n ~r',
                    value='',
                    style={'height': 150, 'margin-top': '10px'}, ),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Ordinary premise preferences', style={'margin-left': '10px'}),
                html.Br(),
                dcc.Textarea(
                    id='ordinary-prem-preferences',
                    placeholder='Add one preference between two premises per line. For example:\n p < -q \n -q > ~r',
                    value='',
                    style={'height': 150, 'margin-left': '10px', 'margin-top': '10px'},
                ),
            ], style={'padding': 10, 'flex': 1}),
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div([
            html.Div([
                html.B('Strict rules', style={'margin-left': '10px'}),
                html.Br(),
                dcc.Textarea(
                    id='aspic-strict-rules',
                    placeholder='Add one strict rule per line. For example:\n p->q \n -q -> -r',
                    value='',
                    style={'height': 150, 'margin-left': '10px', 'margin-top': '10px'},
                ),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Defeasible rules'),
                html.Br(),
                dcc.Textarea(
                    id='aspic-defeasible-rules',
                    placeholder='Add one defeasible rule per line, including the rule name. '
                                'For example:\n d1: p=>q \n d2: -q => -r',
                    value='',
                    style={'height': 150, 'margin-top': '10px'}, ),
            ], style={'padding': 10, 'flex': 1}),

            html.Div([
                html.B('Defeasible rule preferences', style={'margin-left': '10px'}),
                html.Br(),
                dcc.Textarea(
                    id='defeasible-rule-preferences',
                    placeholder='Add one preference between two rules per line. For example:\n d1 < d2',
                    value='',
                    style={'height': 150, 'margin-left': '10px', 'margin-top': '10px'},
                ),
            ], style={'padding': 10, 'flex': 1}),
        ], style={'display': 'flex', 'flex-direction': 'row'}),

        html.Div([
            html.B('Ordering', style={'margin-left': '10px'}),
            html.Br(),
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': 'None', 'value': 'nochoice'},
                            {'label': 'Democratic', 'value': 'dem'},
                            {'label': 'Elitist', 'value': 'eli'}
                        ],
                        value='nochoice',
                        id='ordering-choice',
                        inputStyle={'margin-right': '6px'}
                    ),
                ], style={'padding': 5, 'flex': 1}),

                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': 'None', 'value': 'nolink'},
                            {'label': 'Last link', 'value': 'lastl'},
                            {'label': 'Weakest link', 'value': 'weakl'}
                        ],
                        value='nolink',
                        id='ordering-link',
                        inputStyle={'margin-right': '6px'}
                    ),
                ], style={'padding': 5, 'flex': 1}),
            ], style={'display': 'flex', 'flex-direction': 'row', 'margin-left': '10px'}),
        ]),

        html.Div(
            [html.Button('Create AF', id='strAF-Calc', n_clicks=0)], style={'text-align': 'left', 'margin-left': '10px'}
        ),

        html.Div(id='ASPIC-argumentation', style={'whiteSpace': 'pre-line'})
    ])
    return ASPIC_setting