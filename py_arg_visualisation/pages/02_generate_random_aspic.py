import dash
from dash import html, dcc, callback, Input, Output


dash.register_page(__name__, name='GenerateRandomAspic', title='Generate Random ASPIC+ AT')

layout = html.Div(
    children=[
        html.H1('This is the chat page.'),
        html.Div([], id='chat-output')
    ]
)
