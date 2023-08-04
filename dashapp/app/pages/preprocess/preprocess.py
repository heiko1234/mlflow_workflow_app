

import pandas as pd
import numpy as np

# from upath import UPath

import dash
from dash import ctx
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table

from app.utilities.cards import (
    standard_card,
    form_card
)

from app.utilities.plots import (
    control_chart,
    control_chart_marginal
)



dash.register_page(__name__,"/preproces")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(
    id="preprocessing_page_content",
    className="analysis_page_content",
    children=[
        html.H1(children='Data Preprocessing'),
        html.Div(
            className="analysis_page_subcontent",
            children=[
            ]
        ),
    ]
)



