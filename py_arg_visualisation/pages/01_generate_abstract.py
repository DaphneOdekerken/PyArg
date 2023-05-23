import dash
from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc

from py_arg.generators.abstract_argumentation_framework_generators.abstract_argumentation_framework_generator import \
    AbstractArgumentationFrameworkGenerator

dash.register_page(__name__, name='GenerateAbstract', title='Generate Abstract AF')

left_column = dbc.Col([
    html.H2('Input'),
    dbc.Row([dbc.Col(html.B('Number of arguments')),
             dbc.Col(dbc.Input(type='number', min=0, max=50, step=1, value=8,
                               id='01-generate-abstract-nr-arguments-input'))]),
    dbc.Row([dbc.Col(html.B('Number of defeats')),
             dbc.Col(dbc.Input(type='number', min=0, max=50, step=1, value=8,
                               id='01-generate-abstract-nr-defeats-input'))]),
    dbc.Row([dbc.Col(html.B('Allow self-defeats')),
             dbc.Col(dbc.Select(
                options=[{'label': answer, 'value': answer} for answer in ['Yes', 'No']],
                value='Yes', id='01-generate-abstract-allow-self-defeats-input'))
             ]),
    html.Br(),
    dbc.Row([dbc.Button('Generate', id='01-generate-abstract-button')])
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
def get_explanation_html(nr_clicks: int, nr_arguments: str, nr_defeats: str,
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
                value='\n'.join(str(arg) for arg in argumentation_framework.arguments),
                style={'height': '300px'})]),
            dbc.Col([html.B('Defeats'), dbc.Textarea(
                value='\n'.join((f'({str(defeat.from_argument)},{str(defeat.to_argument)})'
                                 for defeat in argumentation_framework.defeats)),
                style={'height': '300px'})])
        ])]

    return output_children
