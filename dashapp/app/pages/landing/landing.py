
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
                                    dcc.Input(type="text", className="text_input", id="i_projectname")
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
                                    dcc.Input(type="text", className="text_input", id="i_organization")
                                ],
                                style={
                                    "display": "flex",
                                    "justify-content": "center",
                                    "margin": "20px",
                                    }
                            ),
                            html.Div(
                                children=[
                                    html.H3("Project Manager", style={"margin": "10px", "width": "200px"}),
                                    dcc.Input(type="text", className="text_input", id="i_project_manager_name")
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


# dash callback to bring all landing page text inputs to project_basic_session_store

@dash.callback(
    Output('project_basic_session_store', 'data'),
    Input('submit-val', 'n_clicks'),
    State('i_projectname', 'value'),
    State('i_organization', 'value'),
    State('i_project_manager_name', 'value'),
    prevent_initial_call=True
)
def update_project_basic_session_store(n_clicks, projectname, organization, project_manager_name):
    output = {"projectname": projectname, "organization": organization, "project_manager_name": project_manager_name}
    return output



# make default values for the landing page when project_basic_session_store is empty

@dash.callback(
    [
        Output('i_projectname', 'value'),
        Output('i_organization', 'value'),
        Output('i_project_manager_name', 'value'),
    ],
    Input('project_basic_session_store', 'data')
)
def make_default_values_for_all_inputs(project_basic_session_store):

    print("make_default_values_for_all_inputs got activated, landingpage")
    print(f"project_basic_session_store: {project_basic_session_store}")

    if (project_basic_session_store["projectname"] is None) and (project_basic_session_store["organization"] is None) and (project_basic_session_store["project_manager_name"] is None):
        return "projectname", "organization", "projectleader"
    else:
        return project_basic_session_store["projectname"], project_basic_session_store["organization"], project_basic_session_store["project_manager_name"]

