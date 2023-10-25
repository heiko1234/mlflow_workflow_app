

import os
import io
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



from app.utilities.api_call_clients import APIBackendClient
from dotenv import load_dotenv


load_dotenv()


dataclient=APIBackendClient()







dash.register_page(__name__,"/validation")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )



# def get_mlflow_model(model_name, azure=True, staging="Staging"):

#     if azure:
#         azure_model_dir = os.getenv("MLFLOW_MODEL_DIRECTORY", "models:/")
#         if staging == "Staging":
#             model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
#             artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
#         elif staging == "Production":
#             model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Production")
#             artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)
#         else:
#             print("Staging must be either 'Staging' or 'Production'. Default: Staging")
#             model_stage = os.getenv("MLFLOW_MODEL_STAGE", "Staging")
#             artifact_path = PurePosixPath(azure_model_dir).joinpath(model_name, model_stage)

#         artifact_path

#         model = mlflow.pyfunc.load_model(str(artifact_path))
#         print(f"Model {model_name} loaden from Azure: {artifact_path}")

#     return model





layout = html.Div(
    children=[
        html.H1(children='This is our validation page'),
        html.Div(children=[
            html.Div([
                standard_card(
                    id="validation_card",
                    header_text="Select a Model",
                    width="600px",
                    height="300px",
                    content=
                    [
                        html.Div([
                            dcc.Dropdown(
                                id="model_download_dd",
                                style={"width": "80%"},
                            ),
                            # add a toggle
                            html.Br(),
                            html.H3("Select a plot mode"),
                            daq.ToggleSwitch(
                                id="plot_toggle",
                                label=["Overlay", "X-y plot"],
                                color="blue",
                                value=False,
                                style={"width": "80%", "margin-top": "20px"}
                            ),
                        ],
                        style={"display": "block"}
                        )
                    ]
                )
                ,
                standard_card(
                    id="validation_card_info",
                    header_text="Model info",
                    width="300px",
                    height="300px",
                    content=[
                        html.Div([
                            html.Div([
                                html.H3("Modelversion: "),
                                html.H4(id="model_version_id", style={"color": "blue", "margin-left": "10px"})
                                ],
                                style = {
                                    "width": "80%",
                                    "margin-top": "20px",
                                    "display": "flex",
                                    "margin": "5px"
                                    }
                            ),
                            html.Div([
                                html.H3("R2 Training: "),
                                html.H4(id="r2_training_id", style={"color": "blue", "margin-left": "10px",})
                            ],
                            style = {"width": "80%",
                                "display": "flex",
                                "margin": "5px"
                                }
                            ),
                            html.Div([
                                html.H3("R2 Test: "),
                                html.H4(id="r2_test_id",
                                    style={
                                        "color": "blue",
                                        "margin-left": "10px",
                                    })
                            ],
                            style = {
                                "width": "80%",
                                "display": "flex",
                                "margin": "5px"
                            }
                            ),
                        ])
                    ]
                ),
                standard_card(
                    id="validation_card_model_to_production",
                    header_text="Do you like to use the model in Production?",
                    width="300px",
                    height="300px",
                    content=[
                        html.Div([
                            html.Button("Send to Production",
                                        className="submit_button",
                                        id="send_to_production_button",
                                        n_clicks=0,
                                ),
                            ],
                            style={"display": "flex",
                                "justify-content": "center",
                                "margin": "20px"
                                }
                            )
                    ]
                ),
            ],
            style = {"display": "flex"}
            )
        ]
        ),
        html.Div(
            html.Div([
                standard_card(
                    id="data_validation_card",
                    header_text="Validation of the trained Model",
                    content=[
                        html.Div([
                            html.Div(id="output_validation"),
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




# @dash.callback(
#     Output("model_download_dd", "options"),
#     Input("model_download_dd", "value"),
# )
# def get_model_download_options(value):

#     try:

#         import os
#         from dotenv import load_dotenv


#         load_dotenv()


#         client = mlflow.MlflowClient()


#         output = []


#         for rm in client.search_registered_models():
#             output.append({"label": rm.name, "value": rm.name})

#         return output

#     except Exception as e:
#         print(e)
#         return None



@dash.callback(
    Output("model_download_dd", "options"),
    Input("model_download_dd", "value"),
)
def get_model_download_value(model_selected):

    # print(f"get_model_download_value model_selected: {model_selected}")

    try:
        headers = None
        endpoint = "list_available_models"


        response = dataclient.Backendclient.execute_get(
            headers=headers,
            endpoint=endpoint,
            )

        if response.status_code == 200:
            output = response.json()


            # TODO: remove fix model name
            # output = ["project_name"]


            if isinstance(output, list):
                listed_models = output
            else:
                listed_models = [output]

        else:
            listed_models = None
            options = None
            value = None

            return value


        listed_models = list(set(listed_models))


        options = [
            {"label": i, "value": i} for i in listed_models
        ]

        return options


    except Exception as e:
        print(f"get_model_download_value exception: {e}")
        options = None
        value = None

        return options




@dash.callback(
    Output("model_version_id", "children"),
    Input("model_download_dd", "value"),
    State("data_session_store", "data")
)
def get_model_version(model_selected, data_dict):

    try:
        headers = None
        endpoint = "get_model_version"

        data_statistics_dict = {
                "account": data_dict["account"],
                "use_model_name": model_selected,
                "staging": "Staging"
            }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()

        return output


    except Exception as e:
        print(f"get_model_version exception: {e}")
        output = None


        return output




@dash.callback(
    [
        Output("r2_training_id", "children"),
        Output("r2_test_id", "children"),
    ],
    Input("model_download_dd", "value"),
    State("data_session_store", "data")
)
def get_model_metrics(model_selected, data_dict):

    try:
        headers = None
        endpoint = "get_model_artifact"


        artifact_value = "metrics.json"

        data_statistics_dict = {
                "account": data_dict["account"],
                "use_model_name": model_selected,
                # "staging": "Staging"
                "artifact": artifact_value,
            }

        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()

            print(f" get_model_metrics: {output}")

            try:
                r2_training = round(output["r2_training"], 3)
                r2_test = round(output["r2_test"], 3)
            except Exception as e:
                print(f"get_model_metrics exception: {e}")
                r2_training = None
                r2_test = None

        return r2_training, r2_test


    except Exception as e:
        print(f"get_model_version exception: {e}")

        r2_training = None
        r2_test = None

        return r2_training, r2_test







@dash.callback(
    [
        Output("output_validation", "children"),
        Output("project_model_name_session_store", "data"),
    ],
    Input("model_download_dd", "value"),
    Input("plot_toggle", "value"),
    State("data_session_store", "data"),
)
def make_validation_graphic(model_name, plot_mode, data_dict):

    try:

        if data_dict is None:
            return None, model_name

        else:
            headers = None
            endpoint = "model_validation"
            # endpoint = "model_validation_graphics"

            data_statistics_dict = {
                "blobcontainer": data_dict["blobcontainer"],
                "subcontainer": data_dict["subcontainer"],
                "file_name": data_dict["file_name"],
                "account": data_dict["account"],
                "use_model_name": model_name
            }

            # print(f"data_statistics_dict: {data_statistics_dict}")

            response = dataclient.Backendclient.execute_post(
                headers=headers,
                endpoint=endpoint,
                json=data_statistics_dict
                )


            if response.status_code == 200:
                output = response.json()

                # # vielleicht so: 
                # load_IO = io.StringIO()
                # output = load_IO(output)

                output_df = pd.read_json(output, orient="split")

                if plot_mode == False:
                    fig = validation_plot(output_df["actual"], output_df["prediction"])

                    output = dcc.Graph(
                        figure=fig,
                        style={
                            "width": "1700px",
                            "height": "700px"
                            }
                    )

                else:
                    fig = x_y_plot(output_df["actual"], output_df["prediction"])

                    output = dcc.Graph(
                        figure=fig,
                        style={
                            "width": "1700px",
                            "height": "700px"
                            }
                    )

                # fig = output["fig"]

                # if plot_mode == False:

                #     output = dcc.Graph(
                #         figure = fig,
                #         style={
                #             "width": "1700px",
                #             "height": "700px"
                #             }
                #         )


    except Exception as e:
        print(e)
        output = None

    return output, model_name
















