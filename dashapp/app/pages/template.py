import dash
from dash import html, dcc


dash.register_page(__name__,"/template")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(
    children=[
        html.H1(children='This is our template page'),
        html.Div(children='''
            This is our template page content.
            '''),
    ],
)
