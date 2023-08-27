


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
    control_chart_marginal,
    validation_plot
)


import mlflow



dash.register_page(__name__,"/validation")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


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
                    ])
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
    State("data_session_store", "data"),
)
def make_validation_graphic(model, data):
        
        try:
        
            import os
            from dotenv import load_dotenv
    
    
            load_dotenv()
    
    
            client = mlflow.MlflowClient()
            
            model = client.get_registered_model(model)
            
            model_version = model.latest_versions[0].version
            
            model = client.get_model_version(model.name, model_version)
            
            # TODO: not working yet
            
            model_path = model.source
            model_path = model_path.replace("file://", "")
            
            model = mlflow.pyfunc.load_model(model_path)
            
            df = pd.read_csv(data["data_path"])
            
            df = df.set_index("Time")
            
            df["Yield validation"] = model.predict(df)
            
            fig = validation_plot(df["Yield"], df["Yield validation"])
            
            return dcc.Graph(figure=fig)
        
        except Exception as e:
            print(e)
            return None



