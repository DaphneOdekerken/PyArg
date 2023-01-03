import dash_bootstrap_components as dbc
import visdcc
from dash import html, dcc


def get_aspic_layout(ASPIC_setting, structured_evaluation, structured_explanation):
    layout_ASPIC = html.Div([
        html.Div([
            html.Div([
                dbc.CardHeader(dbc.Button('ASPIC Argumentation Setting', className='pyarg-button',
                                          id='structured-arg-setting-button')),
                dbc.Collapse(dbc.CardBody(ASPIC_setting), id='structured-arg-setting-collapse', is_open=False),

                dbc.CardHeader(dbc.Button('Evaluation', className='pyarg-button', id='structured-evaluation-button')),
                dbc.Collapse(dbc.CardBody(structured_evaluation), id='structured-evaluation-collapse', is_open=False),

                dbc.CardHeader(dbc.Button('Explanation', className='pyarg-button', id='structured-explanation-button')),
                dbc.Collapse(dbc.CardBody(structured_explanation), id='structured-explanation-collapse', is_open=False),
            ], className='padded-item'),

            html.Div([
                visdcc.Network(data={'nodes': [], 'edges': []},
                               id='structured-argumentation-graph',
                               options=dict(height='600px'),
                               style={'border-radius': '8px',
                                      'border': '2px solid #152A47',
                                      'margin-right': '25px'}),
                html.Div([
                    html.Div([
                        html.Div(id='structured-output', className='output'),
                        html.Div(id='structured-evaluation', className='output'),
                        html.Div(id='structured-explanation', className='output')
                    ], className='row-container'),
                    html.Div([
                        html.Div(id='structured-argumentation-graph-output', className='output'),
                        html.Div(id='structured-argumentation-graph-evaluation', className='output'),
                        html.Div(id='structured-argumentation-graph-explanation', className='output')
                    ], className='row-container')
                ])
            ], className='padded-item'),
        ], className='row-container')
    ])
    return layout_ASPIC


def get_structured_explanation():
    structured_explanation = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.B('Type'),
                    dcc.RadioItems(
                        options=[{'label': 'Acceptance', 'value': 'Acceptance'},
                                 {'label': 'Non-Acceptance', 'value': 'NonAcceptance'}],
                        value='', id='structured-explanation-type'
                    ),
                ]),

                html.Div([
                    html.B('Strategy'),
                    dcc.RadioItems(
                        options=[
                            {'label': 'Credulous', 'value': 'Credulous'},
                            {'label': 'Skeptical', 'value': 'Skeptical'}
                        ],
                        value='', id='structured-explanation-strategy'
                    ),
                ], style={'margin-top': '20px'}),
            ], className='padded-item'),

            html.Div([
                html.Div([
                    html.B('Explanation function'),
                    dcc.RadioItems(
                        id='structured-explanation-function'
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
                            {'label': 'Sub-argument conclusions', 'value': 'SubArgConclusions'}
                        ],
                        id='structured-explanation-form'
                    ),
                ], style={'margin-top': '20px'}),
            ], className='padded-item')

        ], className='row-container'),

        html.Div(
            [html.Button('Derive Explanations', id='structured-explanation-button', n_clicks=0,
                         className='pyarg-button')], className='button-container'),

        html.Div(style={'whiteSpace': 'pre-line'}),
    ])
    return structured_explanation


def get_structured_evaluation():
    structured_evaluation = html.Div([
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
                    value='', id='structured-evaluation-semantics'
                ),
            ], className='padded-item'),

            html.Div([
                html.B('Evaluation strategy'),
                dcc.RadioItems(
                    options=[
                        {'label': 'Credulous', 'value': 'Credulous'},
                        {'label': 'Weakly Skeptical', 'value': 'WeaklySkeptical'},
                        {'label': 'Skeptical', 'value': 'Skeptical'}
                    ],
                    value='', id='structured-evaluation-strategy'
                ),
            ], className='padded-item'),
        ], className='row-container'),

        html.Div(
            [html.Button('Evaluate AF', id='evaluate-structured-argumentation-theory-button',
                         n_clicks=0, className='small-pyarg-button')], className='button-container'),
        html.Div(style={'whiteSpace': 'pre-line'}),
    ])
    return structured_evaluation


def get_aspic_setting():
    ASPIC_setting = html.Div(children=[
        html.Div([html.Button('Generate random', id='generate-random-arg-theory-button', n_clicks=0,
                              className='small-pyarg-button')], className='padded-item'),
        # html.Div([html.Button('Generate layered', id='generate-layered-arg-theory-button', n_clicks=0,
        #                       className='small-pyarg-button')], className='padded-item'),
        html.Div([
            html.Div([
                html.B('Axioms'),
                html.Br(),
                dcc.Textarea(id='aspic-axioms', placeholder='Add one axiom per line. For example:\n p \n -q \n ~r',
                             value='', className='aspic-input'),
            ], className='padded-item'),

            html.Div([
                html.B('Ordinary premises'),
                html.Br(),
                dcc.Textarea(id='aspic-ordinary-premises',
                             placeholder='Add one ordinary premise per line. For example:\n p \n -q \n ~r',
                             value='', className='aspic-input'),
            ], className='padded-item'),

            html.Div([
                html.B('Ordinary premise preferences', style={'margin-left': '10px'}),
                html.Br(),
                dcc.Textarea(id='ordinary-prem-preferences',
                             placeholder='Add one preference between two premises per line. '
                                         'For example:\n p < -q \n -q > ~r',
                             value='', className='aspic-input'),
            ], className='padded-item'),
        ], className='row-container'),

        html.Div([
            html.Div([
                html.B('Strict rules', style={'margin-left': '10px'}),
                html.Br(),
                dcc.Textarea(
                    id='aspic-strict-rules',
                    placeholder='Add one strict rule per line. For example:\n p->q \n -q -> -r',
                    value='', className='aspic-input',
                ),
            ], className='padded-item'),

            html.Div([
                html.B('Defeasible rules'),
                html.Br(),
                dcc.Textarea(
                    id='aspic-defeasible-rules',
                    placeholder='Add one defeasible rule per line, including the rule name. '
                                'For example:\n d1: p=>q \n d2: -q => -r',
                    value='', className='aspic-input'),
            ], className='padded-item'),

            html.Div([
                html.B('Defeasible rule preferences', style={'margin-left': '10px'}),
                html.Br(),
                dcc.Textarea(
                    id='defeasible-rule-preferences',
                    placeholder='Add one preference between two rules per line. For example:\n d1 < d2',
                    value='', className='aspic-input',
                ),
            ], className='padded-item'),
        ], className='row-container'),

        html.Div([
            html.B('Ordering', style={'margin-left': '10px'}),
            html.Br(),
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': 'Democratic', 'value': 'democratic'},
                            {'label': 'Elitist', 'value': 'elitist'}
                        ],
                        value='democratic', id='ordering-choice'
                    ),
                ], style={'padding': 5, 'flex': 1}),

                html.Div([
                    dcc.RadioItems(
                        options=[
                            {'label': 'Last link', 'value': 'last_link'},
                            {'label': 'Weakest link', 'value': 'weakest_link'}
                        ],
                        value='last_link', id='ordering-link'
                    ),
                ], style={'padding': 5, 'flex': 1}),
            ], className='row-container'),
        ]),

        html.Div(
            [html.Button('Create AF', id='create-argumentation-theory-button', n_clicks=0,
                         className='small-pyarg-button')], className='button-container'),

        html.Div(id='ASPIC-argumentation', style={'whiteSpace': 'pre-line'})
    ])
    return ASPIC_setting
