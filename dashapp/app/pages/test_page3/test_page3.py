

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State


dash.register_page(__name__,"/testpage3")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(
    children=[
        html.Div(
            id="accordion",
            className="accordion",
            children=[
                html.Div(
                    className="accordion-item",
                    children=[
                        html.Div(
                            className="accordion-title",
                            children=[
                                html.H2("Accordion Title"),
                                html.Div(
                                    className="accordion-icon",
                                    children=[
                                        # html.Button('Button',
                                        #     id='accordion-id',
                                        #     n_clicks=0,
                                        # )
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            id="accordion-content",
                            className="accordion-content",
                            children=[
                                html.P("Accordion Content, very much content to show up when active")
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)




@dash.callback(
    Output("accordion-content", "style"),
    Input("accordion", "n_clicks"),
    State("accordion-content", "style")
)
def toggle_accordion(n, style):
    print(f"toggle_accordion: {n}")
    print(f"toggle_accordion: {style}")
    if n:
        if style["display"] == "block":
            return {"display": "none"}
        else:
            return  {"display": "block"}
    return {"display": "none"}







# @dash.callback(
#     Output("accordion-content", "className"),
#     Input("accordion-id", "n_clicks"),
#     State("accordion-content", "className")
# )
# def toggle_accordion(n, className):
#     print(f"toggle_accordion: {n}")
#     if n:
#         if className == "accordion-content":
#             return "accordion-content active"
#         else:
#             return "accordion-content"
#     return "accordion-content"




# @dash.callback(
#     Output("accordion-id", "children"),
#     Input("accordion-id", "n_clicks"),
# )
# def toggle_accordion(n):
#     print(f"toggle_accordion 2: {n}")
#     if n:
#         return "Button Clicked"
#     return "Button"


