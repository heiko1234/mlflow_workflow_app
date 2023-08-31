

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



dash.register_page(__name__,"/validation")

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
        html.H1(children='This is our validation page'),
        html.Div(children=[
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




@dash.callback(
    Output("model_download_dd", "options"),
    Input("model_download_dd", "value"),
)
def get_model_download_options(value):
    
    try:
    
        import os
        from dotenv import load_dotenv


        load_dotenv()


        client = mlflow.MlflowClient()
        
        
        output = []


        for rm in client.search_registered_models():
            output.append({"label": rm.name, "value": rm.name})
            
        return output
    
    except Exception as e:
        print(e)
        return None



@dash.callback(
    Output("output_validation", "children"),
    Input("model_download_dd", "value"),
    Input("plot_toggle", "value"),
    State("data_session_store", "data"),
)
def make_validation_graphic(model_name, plot_mode, data):
        
        try:


            mlflow_model = get_mlflow_model(model_name=model_name, azure=True, staging="Staging")
            
            
            print(mlflow_model)

            df = pd.read_json(data, orient="split")
            
            print(df)
            
            df_predict = df
            
            df_predict["Yield"] = df["Yield"]
            
            df_predict["Yield validation"] = df_predict["Yield"]-0.5
            
            # print(df_predict)
            
            # df_predict["Yield validation"] = mlflow_model.predict(df_predict)
            
            if plot_mode == False:
            
                fig = validation_plot(df_predict["Yield"], df_predict["Yield validation"])
                
                return dcc.Graph(figure=fig, style={"width": "1700px", "height": "700px"})
            
            else:
                fig = x_y_plot(df_predict["Yield"], df_predict["Yield validation"])
                
                return dcc.Graph(figure=fig, style={"width": "1700px", "height": "700px"})
        
        except Exception as e:
            print(e)
            return None



