import dash
from dash import html


dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.Div(children='Please click on one of the links above.'),
])
