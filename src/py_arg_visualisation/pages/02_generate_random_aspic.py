import dash
from dash import html

dash.register_page(__name__, name='GenerateRandomAspic',
                   title='Generate Random ASPIC+ AT')

layout = html.Div(
    children=[
        html.H1('Generate Random ASPIC+ Argumentation Theory'),
        html.Div([], id='generate-random-aspic-div')
    ]
)
