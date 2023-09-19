



import base64
import datetime
import io

import os
import pandas as pd
import numpy as np

# from upath import UPath

import dash
from dash import ctx
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash_daq as daq

from app.utilities.cards import (
    standard_card,
    form_card
)

from app.utilities.plots import (
    control_chart,
    control_chart_marginal,
    validation_plot,
    x_y_plot
)


import mlflow
from pathlib import PurePosixPath

from dotenv import load_dotenv


load_dotenv()






dash.register_page(__name__,"/evaluation")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )



def get_mlflow_model(model_name, azure=True, staging="Staging"):

    if azure:
        azure_model_dir = os.getenv("MLFLOW_MODEL_DIRECTORY", "models:/")
        if staging == "Staging":
            model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
            artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
        elif staging == "Production":
            model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Production")
            artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
        else:
            print("Staging must be either 'Staging' or 'Production'. Default: Staging")
            model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
            artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
        
        artifact_path

        model = mlflow.pyfunc.load_model(str(artifact_path))
        print(f"Model {model_name} loaden from Azure: {artifact_path}")
        
    return model


layout = html.Div(
    children=[
        html.H1(children='This is our evaluation page'),
        html.Div(
            children=[
                html.Div([
                    standard_card(
                        id="evaluation_card",
                        header_text="Select a Model",
                        width="600px",
                        height="300px",
                        content=[
                            html.Div(
                                children=[
                                    html.H3("Selected Model"),
                                    html.H3(id="selected_model", style={"color": "blue"}),
                                ]
                            ),
                        ]
                    ),
                    standard_card(
                        id="evaluatin_upload_card",
                        header_text="Upload evaluation Data",
                        width="600px",
                        height="300px",
                        content=[
                            html.Div([
                                dcc.Upload(
                                    id='upload_evaluation_data',
                                    children=html.Div([
                                        'Drag and Drop or ',
                                        html.A('Select Files')
                                    ]),
                                    style={
                                        "width": "250px",
                                        "height": "120px",
                                        "lineHeight": "60px",
                                        "borderWidth": "1px",
                                        "borderStyle": "dashed",
                                        "borderRadius": "5px",
                                        "textAlign": "center",
                                        "margin": "10px"
                                    },
                                    multiple=False
                                ),
                            ],
                            style={
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center"
                            }
                            ),
                        ]
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center"
                }
                ),
                html.Div(
                    html.Div([
                        standard_card(
                            id="data_evaluation_visualization_card",
                            header_text="Evaluation of Data with registered Model",
                            content=[
                                html.Div([
                                    html.Div(id="output_evaluation"),
                                ])
                            ],
                            height="800px",
                            width="1800px"
                        )
                    ],
                    ),
                )
            ],
        )
    ],
)




@dash.callback(
    Output("selected_model", "children"),
    Input("project_model_name_session_store", "data"),
)
def get_model_name_downloaded(value):
    print(f"get_model_name_downloaded value: {value}")
    return value



@dash.callback(
    Output("project_evaluation_session_store", "data"),
    [
        Input("upload_evaluation_data", "contents"),
        Input("upload_evaluation_data", "filename"),
    ]
)
def get_evaluation_data(contents, filename):

    print(f"get_evaluation_data triggered")
    output = None

    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        if "csv" in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=";")

        if "xls" in filename:
            df = pd.read_excel(io.BytesIO(decoded))

        if "xlsx" in filename:
            df = pd.read_excel(io.BytesIO(decoded))

        if "parquet" in filename:
            df = pd.read_parquet(io.BytesIO(decoded))


        output=df.to_json(date_format='iso', orient='split')
        
        print(f"uploaded outputdata: {output}" )
        
    return output



@dash.callback(
    Output("output_evaluation", "children"),
    [
        Input("project_evaluation_session_store", "data"),
        Input("project_model_name_session_store", "data"),
    ]
)
def make_evaluation_graphic(data, model_name):

    if data is not None:
        print(f"make_evaluation_graphic data is not none")
        try:
            df = pd.read_json(data, orient='split')

            # mlflow_model = get_mlflow_model(model_name=model_name, azure=True, staging="Staging")

            target = "Yield"
            target_string = target+"_evaluation"

            # df[target_string] = mlflow_model.predict(df)

            df[target_string] = df[target]-0.7

            fig = validation_plot(df[target], df[target_string])

            output = dcc.Graph(figure=fig, style={"width": "1700px", "height": "700px"})

            return output


        except Exception as e:
            print(e)
            return None

    else:
        return None






















