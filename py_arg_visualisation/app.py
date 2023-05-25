from dash import Dash, html
import dash_bootstrap_components as dbc
import dash


# Create a Dash app using an external stylesheet.
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.YETI])

# Navigation bar.
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Random Abstract AF', href='01-generate-abstract'),
                # dbc.DropdownMenuItem('Random ASPIC+ AT', href='02-generate-random-aspic'),
                dbc.DropdownMenuItem('Layered ASPIC+ AS', href='03-generate-layered-aspic'),
            ],
            nav=True,
            in_navbar=True,
            label='Generate',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Abstract', href='11-edit-abstract'),
                dbc.DropdownMenuItem('ASPIC+', href='12-edit-aspic'),
            ],
            nav=True,
            in_navbar=True,
            label='Edit',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Abstract', href='21-visualise-abstract'),
                dbc.DropdownMenuItem('ASPIC+', href='22-visualise-aspic'),
            ],
            nav=True,
            in_navbar=True,
            label='Visualise',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Practice', href='30-learn'),
            ],
            nav=True,
            in_navbar=True,
            label='Learn',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Canonical representations', href='40-canonical')
            ],
            nav=True,
            in_navbar=True,
            label='Algorithms',
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem('Chat', href='50-chat'),
            ],
            nav=True,
            in_navbar=True,
            label='Applications',
        ),
        dbc.DropdownMenuItem('About', href='/')
    ],
    brand='PyArg',
    brand_href='/',
    color='primary',
)

# Specification of the layout, consisting of a navigation bar and the page container.
app.layout = html.Div([navbar, dbc.Col(html.Div([dash.page_container]), width={'size': 10, 'offset': 1})])

# Running the app.
if __name__ == '__main__':
    app.run_server(debug=True)
