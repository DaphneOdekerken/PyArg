import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', title='PyArg', name='PyArg')

layout = html.Div(children=[
    html.H1('Welcome at PyArg!'),
    html.B('What would you like to do?'),
    dbc.ListGroup(
        [dbc.ListGroupItem(
            dbc.NavLink(html.B(page['name']), href=page['relative_path']), className='w-50')
            for page in dash.page_registry.values()]
    )
])
