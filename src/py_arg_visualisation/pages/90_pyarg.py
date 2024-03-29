import dash
from dash import html

dash.register_page(__name__, path='/', title='PyArg', name='PyArg')

layout = html.Div(children=[
    html.H1('Welcome to PyArg!'),
    html.P('This is a Python package and web interface for solving various '
           'problems in computational argumentation.'),
    html.P(['If you have any questions, feedback or ambitions to contribute, '
            'feel free to contact ',
            html.A('Daphne Odekerken (D.Odekerken@UU.nl)',
                   href='mailto:d.odekerken@uu.nl?subject=PyArg'),
            '.']),
    html.P('Contributors:'),
    html.Ul([
        html.Li(html.A(
            'Matti Berthold',
            href='https://www.informatik.uni-leipzig.de/~berthold/',
            target='_blank')),
        html.Li(html.A('AnneMarie Borg',
                       href='https://annemarieborg.nl/',
                       target='_blank')),
        html.Li(html.A('Jonas Klein',
                       href='https://www.fernuni-hagen.de/aig/en/team/jonas'
                            '.klein.shtml',
                       target='_blank')),
        html.Li(html.A('Bertram Ludäscher',
                       href='https://cs.illinois.edu/about/people/faculty/'
                            'ludaesch',
                       target='_blank')),
        html.Li(html.A('Daphne Odekerken',
                       href='https://webspace.science.uu.nl/~3827887/',
                       target='_blank')),
        html.Li(html.A('Yilin Xia',
                       href='https://yilinxia.com/',
                       target='_blank'))
    ])
])
