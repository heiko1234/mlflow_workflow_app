
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
        standard_card(id="collectcard", header_text="General Project Infos", content=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.H3("Projectname", style={"margin": "10px", "width": "200px"}),
                                    dcc.Input(type="text", id="i_projectname", style={"margin": "10px", "width": "200px"})
                                ],
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "margin": "20px",
                                    }
                            ),
                            html.Div(
                                children=[
                                    html.H3("Organization", style={"margin": "10px", "width": "200px"}),
                                    dcc.Input(type="text", id="i_organization", style={"margin": "10px", "width": "200px"})
                                ],
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "margin": "20px",
                                    }
                            ),
                            html.Div(
                                children=[
                                    html.H3("Name", style={"margin": "10px", "width": "200px"}),
                                    dcc.Input(type="text", id="i_name", style={"margin": "10px", "width": "200px"})
                                ],
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "margin": "20px",
                                    }
                            ),
                            # create a button to submit the form
                            html.Div(
                                children=[
                                    html.Button('Submit',
                                        className="submit_button",
                                        id='submit-val',
                                        n_clicks=0,
                                    )
                                ],
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "margin": "20px",
                                }
                            ),
                        ],
                        style={
                            "display": "block",
                            "justify-content": "center",
                        }
                )],
            )
        ],
        height="400px",
        width="600px")
    ])



