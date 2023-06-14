
# landing page

import base64
import datetime
import io

import pandas as pd

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table

dash.register_page(__name__,"/landing")



layout = html.Div(
    children=[
        html.H1(children='This is our template page'),
        html.Div(children='''
            This is our landing page content.
            '''),
        ])



