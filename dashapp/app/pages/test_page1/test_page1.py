import dash
from dash import html, dcc


dash.register_page(__name__,"/testpage1")

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
        html.Div(
            children=[
                html.Div(
                    className="myCard",
                    # myCard
                    children=[
                        html.Div(
                            className="myCard_inner",
                            # innerCard
                            children=[
                                html.Div(
                                    className="myCard_front",
                                    # front
                                    children=[
                                        html.P(className="myCard_front_title", children=["Title"]),
                                        html.P("Hover Me")
                                    ]
                                ),
                                html.Div(
                                    className="myCard_back",
                                    # back
                                    children=[
                                        html.P(className="myCard_back_title", children=["Title"]),
                                        html.P("Leave Me")
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
