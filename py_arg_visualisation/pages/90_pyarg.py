import dash
from dash import html

dash.register_page(__name__, path='/', title='PyArg', name='PyArg')

layout = html.Div(children=[
    html.H1('Welcome at PyArg!'),
    html.P('This is a Python package and web interface for solving various problems in'
           'computational argumentation.'),
    html.P('Contributors:'),
    html.Ul([
        html.Li('Daphne Odekerken'),
        html.Li('AnneMarie Borg'),
        html.Li('Matti Berthold')
    ])
])
