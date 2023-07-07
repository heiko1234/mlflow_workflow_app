
# landing page

import base64
import datetime
import io

import pandas as pd

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table

from app.utilities.cards import (
    standard_card,
    form_card
)


dash.register_page(__name__,"/landing")



layout = html.Div(
    id="landing_page_content",
    className="landing_page_content",
    children=[
        html.H1(children='Start your Project'),
        # html.Div(children='''
        #     This is our landing page content.
        #     '''),
        standard_card(id="collectcard", header_text="Project Infos", content=[html.Div(children=[
            html.Div(
                children=[
                    standard_card(id="namecard", header_text="Name", content=[dcc.Input(type="text", id="i_name")], height="100px", width="250px"),
                    # standard_card(id="projectcard", header_text="Projectname", content=[dcc.Input(type="text", id="i_projectname")], height="100px", width="250px"),
                    form_card(id="projectcard", header_text="Projectname", height="100px", width="450px")
                    ], style={"display": "flex"}
                ),
            html.Div(
                children=[
                    standard_card(id="organizationcard", header_text="Organization", content=[dcc.Input(type="text", id="i_organization")], height="100px", width="250px"),
                    standard_card(id="testcard", header_text="Dummyname", content=[dcc.Input(type="text", id="i_dummy")], height="100px", width="250px")
                    ], style={"display": "flex"}
                ),
            ],)],
            height="600px",
            width="600px"
        )
    ])



