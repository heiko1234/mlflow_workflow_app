

# model page



import dash

from dash import ctx
from dash import html, dcc

# import dash daq
import dash_daq as daq

from dash.dependencies import Input, Output, State

from app.utilities.cards import (
    standard_card,
    form_card,
)

from app.utilities.api_call_clients import APIBackendClient


dataclient=APIBackendClient()



dash.register_page(__name__,"/model")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )



model_card = html.Div([
    standard_card(
        id="model_card",
        header_text="Select a Model",
        width="800px",
        height="600px",
        content=[
            html.Div([
                html.H3("Model Selection"),
                dcc.Dropdown(
                    id="model_selection",
                ),
                html.H3("Data Scaler"),
                dcc.Dropdown(
                    id="data_scaler",
                ),
                html.H3("Data Splitter"),
                dcc.Dropdown(
                    id="data_splitter",
                ),
                html.H3("", style={"margin": "1em"}),
                html.Div([
                    html.H4("Advanced Parameters"),
                ], style={"margin": "2em"}),
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle_advanced_parameters',
                        label=['Advanced Parameters'],
                        labelPosition='bottom',
                        value=False,
                        color="blue"
                    ),
                    daq.ToggleSwitch(
                        id='toggle_local_usage',
                        label=['Local Usage'],
                        labelPosition='bottom',
                        value=True,
                        color="green"
                    ),
                    ], style={"display": "flex", "justify-content": "space-around", "margin": "1em"}),
            ],
            style={
                    # "height": "400px"
                    "overflow": "auto",
                }
            )
        ]
    )
])




# create a button to submit the form
Model_submit= html.Div(
    children=[
        html.Button('Start Modelling',
            className="submit_button",
            id='submit-model',
            n_clicks=0,
        )
    ],
    style={
        "display": "flex",
        "justify-content": "center",
        "margin": "20px",
    }
)


# submit_card = html.Div([
#     standard_card(
#         id="submit_card",
#         header_text="Submit Model",
#         width="400px",
#         height="200px",
#         content=[
#             html.Div(
#                 children=[
#                     html.Button('Submit',
#                         className="submit_button",
#                         id='submit-model',
#                         n_clicks=0,
#                     )
#                 ],
#                 style={
#                     "display": "flex",
#                     "justify-content": "center",
#                     "margin": "20px",
#                 }
#             )
#         ]
#     )
# ])



model_parameters_card = html.Div([
    standard_card(
        id="model_parameters_card",
        header_text="Model Parameters",
        width="800px",
        height="600px",
        content=[
            html.Div([
                dcc.Loading(
                    id="model_parameters_loading",
                ),
                html.H3(""),
            ],
            style={
                    "overflow": "auto",
                    "height": "450px"
                }
            )
        ]
    )
])


model_training_feedback_card = html.Div([
    standard_card(
        id="model_training_feedback_card",
        header_text="Model Training Feedback",
        width="800px",
        height="200px",
        content=[
            html.Div([
                dcc.Loading(
                    id="model_training_feedback_loading",
                ),
                html.H3(""),
            ],
            style={
                    "overflow": "auto",
                    "height": "100px"
                }
            )
        ]
    )
])




# create a card with an icon and text to start modelling
# start_modelling_process_card



layout = html.Div(
    children=[
        html.H1(children='Make an AI Model'),
        # html.Div(children='''
        #     This is our template page content.
        #     '''),
        html.Div([
            html.Div([
                model_card,
                model_parameters_card,
            ],
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center"
                },
            ),
        ]),
        html.Div([
            model_training_feedback_card,
        ],
        style={
            "display": "flex",
            "align-items": "center",
            "justify-content": "center"
            }
        ),
        Model_submit
        # html.Div([
        #     submit_card
        # ])
    ],
)



@dash.callback(
    [
        Output("model_selection", "options"),
        Output("model_selection", "value"),
    ],
    [
        Input("model_selection", "value"),
    ]
)
def update_model_selection(model_selection):
    output = [
        {"label": "LinearRegression", "value": "LinearRegression"},
        {"label": "Ridge", "value": "Ridge"},
        {"label": "RandomForestRegressor", "value": "RandomForestRegressor"},
        {"label": "DecisionTreeRegressor", "value": "DecisionTreeRegressor"},
        {"label": "AdaBoostRegressor", "value": "AdaBoostRegressor"},
        {"label": "NeuralNetwork", "value": "NeuralNetwork"},
    ]

    if model_selection is None:
        value = "LinearRegression"
    else:
        value = model_selection

    return output, value



@dash.callback(
    [
        Output("data_scaler", "options"),
        Output("data_scaler", "value"),
    ],
    [
        Input("data_scaler", "value"),
    ]
)
def update_data_scaler(data_scaler):
    output = [
        {"label": "MinMaxScaler", "value": "MinMaxScaler"},
        {"label": "StandardScaler", "value": "StandardScaler"},
        {"label": "RobustScaler", "value": "RobustScaler"},
        {"label": "Normalizer", "value": "Normalizer"},
        {"label": "QuantileTransformer", "value": "QuantileTransformer"},
        {"label": "PowerTransformer", "value": "PowerTransformer"},
        {"label": "MaxAbsScaler", "value": "MaxAbsScaler"},
        {"label": "None", "value": "None"},
        {"label": "", "value": ""},
    ]

    if data_scaler is None:
        value = "MinMaxScaler"
    else:
        value = data_scaler

    return output, value



@dash.callback(
    [
        Output("data_splitter", "options"),
        Output("data_splitter", "value"),
    ],
    [
        Input("data_splitter", "value"),
    ]
)
def update_data_splitter(data_splitter):
    output = [
        {"label": "No testsplit", "value": "No testsplit"},
        {"label": "10 % test", "value": "10 % test"},
        {"label": "20 % test", "value": "20 % test"},
        {"label": "30 % test", "value": "30 % test"},
        {"label": "40 % test", "value": "40 % test"},
        {"label": "50 % test", "value": "50 % test"},
        {"label": "-----------", "value": ""},
        {"label": "KFold", "value": "KFold"},
        {"label": "RepeatedKFold", "value": "RepeatedKFold"},
        {"label": "ShuffleSplit", "value": "ShuffleSplit"},
    ]

    if data_splitter is None:
        value = "20 % test"
    else:
        value = data_splitter


    return output, value





@dash.callback(
    [
        Output("model_parameters_loading", "children"),
    ],
    [
        Input("model_selection", "value"),
    ]
)
def update_model_parameters_loading(model_selection):

        # {"label": "LinearRegression", "value": "LinearRegression"},
        # {"label": "Ridge", "value": "Ridge"},
        # {"label": "RandomForestRegressor", "value": "RandomForestRegressor"},
        # {"label": "DecisionTreeRegressor", "value": "DecisionTreeRegressor"},
        # {"label": "AdaBoostRegressor", "value": "AdaBoostRegressor"},
        # {"label": "NeuralNetwork", "value": "NeuralNetwork"},

    # print(f"update model parameters loading: {model_selection}")

    if model_selection == "LinearRegression":
        output = [
            html.Div([
                html.P("No parameters to adjust, take it as it is"),
            ])
        ]
    elif model_selection == "Ridge":
        output = [
            html.Div([
                html.Div([
                    html.H3("Alpha"),
                    dcc.Input(
                        id={"type": "model_parameters", "index": "alpha"}, # id="model_parameters_alpha",
                        type="number",
                        value=1,
                        min=0,
                        max=1,
                        step=0.01,
                        size="40",
                        style={"width": "150px", "height": "35px", "margin": "1em"},
                    ),
                ],
                style={"display": "flex", "margin": "1em", "justify-content": "left"}),
            ])
        ]
    elif model_selection == "RandomForestRegressor":
        output = [
            html.Div([
                html.Div([
                    html.H3("n_estimators"),
                    dcc.Input(
                        id={"type": "model_parameters", "index": "n_estimators"}, # id="model_parameters_n_estimators",
                        type="number",
                        value=100,
                        min=0,
                        max=1000,
                        step=1,
                        size="40",
                        style={"width": "150px", "height": "35px", "margin": "1em"},
                    ),
                ],
                style={"display": "flex", "margin": "1em",  "justify-content": "left"}
                ),
                html.Div([
                    html.H3("max_depth"),
                    dcc.Input(
                        id={"type": "model_parameters", "index": "max_depth"}, # id="model_parameters_max_depth",
                        type="number",
                        value=10,
                        min=0,
                        max=100,
                        step=1,
                        size="40",
                        style={"width": "150px", "height": "35px", "margin": "1em"},
                    ),
                ],
                style={"display": "flex", "margin": "1em",  "justify-content": "left"}
                ),
                html.Div([
                    html.H3("min_samples_split"),
                    dcc.Input(
                        id={"type": "model_parameters", "index": "min_samples_split"}, # id="model_parameters_min_samples_split",
                        type="number",
                        value=2,
                        min=0,
                        max=100,
                        step=1,
                        size="40",
                        style={"width": "150px", "height": "35px", "margin": "1em"},
                    ),
                ],
                style={"display": "flex", "margin": "1em",  "justify-content": "left"}
                ),
                html.Div([
                    html.H3("min_samples_leaf"),
                    dcc.Input(
                        id={"type": "model_parameters", "index": "min_samples_leaf"}, # id="model_parameters_min_samples_leaf",
                        type="number",
                        value=1,
                        min=0,
                        max=100,
                        step=1,
                        size="40",
                        style={"width": "150px", "height": "35px", "margin": "1em"},
                    ),
                ],
                style={"display": "flex", "margin": "1em",  "justify-content": "left"}
                ),
                html.Div([
                    html.H3("max_features"),
                    dcc.Input(
                        id={"type": "model_parameters", "index": "max_features"}, #"model_parameters_max_features",
                        type="number",
                        value=1,
                        min=0,
                        max=100,
                        step=1,
                        size="40",
                        style={"width": "150px", "height": "35px", "margin": "1em"},
                    ),
                ],
                style={"display": "flex", "margin": "1em",  "justify-content": "left"}
                ),
            ])
        ]
    else:
        output = [
            html.Div([
                html.P("No parameters to adjust"),
            ])
        ]


    return output


# callback to save based on model_selection value the model parameters to a dict

@dash.callback(
    Output("project_model_configurartion_session_store", "data"),
    [
        Input("model_selection", "value"),
        # pattern matching callback
        Input({"type": "model_parameters", "index": dash.ALL}, "value")
        # Input("model_parameters_alpha", "value"),
        # Input("model_parameters_n_estimators", "value"),
        # Input("model_parameters_max_depth", "value"),
        # Input("model_parameters_min_samples_split", "value"),
        # Input("model_parameters_min_samples_leaf", "value"),
        # Input("model_parameters_max_features", "value"),
    ]
)
def save_model_parameters(
        model_selection,
        type_inputs
        # alpha,
        # n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features
        ):

        # print(f"save_model_parameters: {type_inputs}")

        if model_selection == "LinearRegression":
            model_parameters_dict = {}

        elif model_selection == "Ridge":
            model_parameters_dict = {
                # "alpha": alpha,
                "alpha": type_inputs[0],
            }

        elif model_selection == "RandomForestRegressor":
            model_parameters_dict = {
                "n_estimators": type_inputs[0],
                "max_depth": type_inputs[1],
                "min_samples_split": type_inputs[2],
                "min_samples_leaf": type_inputs[3],
                "max_features": type_inputs[4],
            }
        else:
            # TODO: write more model inputs, pattern matching
            model_parameters_dict = {}

        print(f"model parameters dict final: {model_parameters_dict}")

        return model_parameters_dict



# TODO: remove test callback

# @dash.callback(
#     Output("model_training_feedback_loading", "children"),
#     [
#         Input("submit-model", "n_clicks"),
#         State("project_model_configurartion_session_store","data")
#     ]
# )
# def show_inputs(n_clicks, model_configs):


#     print(f"train model callback, see model configs: {model_configs}")

#     output = html.H3("any output")

#     return output



# TODO

@dash.callback(
    [
        Output("model_training_feedback_loading", "children"),
    ],
    [
        Input("submit-model", "n_clicks"),
        State("project_target_feature_session_store", "data"),
        State("project_data_spc_cleaning_session_store", "data"),
        State("project_data_spc_limit_cleaning_session_store", "data"),
        State("project_data_spc_transformation_cleaning_session_store", "data"),
        State("data_session_store", "data"),
        State("data_splitter", "value"),
        State("data_scaler", "value"),
        State("model_selection", "value"),
        State("project_model_configurartion_session_store","data"),
        State("project_basic_session_store", "data"),
    ]
)
def train_model(n_clicks, dict_target_feature, spc_cleaning_dict, limits_dict, transformation_dict, data_dict, data_splitter, data_scaler, model_selection, model_configs, model_basics):

    headers = None
    endpoint = "train_model"


    # class train_modeling(BaseModel):
    #     blobcontainer: str | None = Field(example="chemical-data")
    #     subcontainer: str | None = Field(example="chemical-data")
    #     file_name: str | None = Field(example="ChemicalManufacturingProcess.parquet")
    #     account: str | None = Field(example="devstoreaccount1")
    #     features: List[str] | None = Field(example=["BioMaterial1", "BioMaterial2", "ProcessValue1"])
    #     spc_cleaning_dict: Dict[str, Dict[str, str]] | None = Field(example={"BioMaterial1": {"rule1": "no cleaning"}, "BioMaterial2": {"rule1":"remove data"}})
    #     limits_dict: Dict[str, Dict[str, Union[str, int, float]]] | None = Field(example={"BioMaterial1": {"min": 10, "max": 20}})
    #     transformation_dict: Dict[str, str] | None = Field(example={"Yield": "no transformation", "BioMaterial1": "log", "BioMaterial2": "sqrt", "ProcessValue1": "1/x"})
    #     target: str| None = Field(example="Yield")
    #     features: List[str] | None = Field(example=["BioMaterial1", "BioMaterial2", "ProcessValue1"])
    #     test_size: float | None = Field(example="0.2")
    #     scaler_expand_by: str | None = Field(example="std")
    #     model_name: str | None = Field(example="my_model_name")
    #     model_parameter: Dict[str, Union[str, int, float]] | None = Field(example={"alpha": 0.5})
    #     model_typ: str | None = Field(example="linear_regression")

    if data_splitter is not None:
        data_splitter_dict ={
            "No testsplit": None,
            "10 % test": 0.1,
            "20 % test": 0.2,
            "30 % test": 0.3,
            "40 % test": 0.4,
            "50 % test": 0.5,
            "KFold": "KFold",
            "RepeatedKFold": "RepeatedKFold",
            "ShuffleSplit": "ShuffleSplit",
        }
        data_splitter_value = data_splitter_dict[data_splitter]
    else:
        data_splitter_value = None


    if model_selection is not None:
        model_selection_dict ={
            "LinearRegression": "linear_regression",
            "RandomForestRegressor": "random_forest",
            "DecisionTreeRegressor": "decision_tree",
            "Ridge": "ridge",
            "ElasticNet": "elastic_net",
            "AdaBoostRegressor": "ada_boost",
        }
        model_selection_value = model_selection_dict[model_selection]



    scaler_expand_by = "std"   # or None
    model_parameters = None

    # TODO: add model parameters
    # TODO: Done
    data_scaler # not used so far
    model_parameters # needs to be modeified
    model_configs # model_parametres

    print(f"train model callback, see model configs: {model_configs}")
    print("use model configs")
    model_parameters = model_configs

    # TODO, take model_basics["projectname"] as modelname, like "projectname" + maybe the target
    # project_basic_session_store["projectname"], project_basic_session_store["organization"], project_basic_session_store["project_manager_name"]
    print(f"train model callback, see model basics: {model_basics}")



    if dict_target_feature is not None:
        dd_list = []
        dd_list.append(dict_target_feature["target"])
        dd_list.extend(dict_target_feature["features"])


        data_statistics_dict = {
            # Load files from blob storage
            "blobcontainer": data_dict["blobcontainer"],
            "subcontainer": data_dict["subcontainer"],
            "file_name": data_dict["file_name"],
            "account": data_dict["account"],
            # data precleaning for modelling
            "features": dd_list,
            "spc_cleaning_dict": spc_cleaning_dict,
            "limits_dict": limits_dict,
            "transformation_dict": transformation_dict,
            # modelling
            "target": dict_target_feature["target"],
            "use_model_features": dict_target_feature["features"],
            "test_size": data_splitter_value,
            "scaler_expand_by": scaler_expand_by,
            "use_model_name": "project_name",   # TODO: any_project_name: AreaKey of Kusto + ModelName
            "use_model_parameter": model_parameters,
            "use_model_typ": model_selection_value
        }


    response = dataclient.Backendclient.execute_post(
        headers=headers,
        endpoint=endpoint,
        json=data_statistics_dict
        )

    if response.status_code == 200:
        output = response.json()


    if output == "Done":
        output = [
            html.Div([
                html.P("Model trained successfully", style={"color": "green"}),
            ])
        ]

    else:
        output = [
            html.Div([
                html.P("Model training failed", style={"color": "red"}),
            ])
        ]

    return output



