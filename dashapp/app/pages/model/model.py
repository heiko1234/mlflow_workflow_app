

# model page



import dash

from dash import ctx
from dash import html, dcc
from dash.dependencies import Input, Output, State

from app.utilities.cards import (
    standard_card,
    form_card,
)


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
        height="500px",
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
                html.H3(""),
            ],
            style={
                    # "height": "400px"
                    "overflow": "auto",
                }
            )
        ]
    )
])


model_parameters_card = html.Div([
    standard_card(
        id="model_parameters_card",
        header_text="Model Parameters",
        width="800px",
        height="500px",
        content=[
            html.Div([
                html.H3("Model Parameters"),
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


# create a card with an icon and text to start modelling
# start_modelling_process_card



layout = html.Div(
    children=[
        html.H1(children='This is our model page'),
        # html.Div(children='''
        #     This is our template page content.
        #     '''),
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
    ]
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
        [
            {"label": "DecisionTreeRegressor", "value": "DecisionTreeRegressor"},
            {"label": "RandomForestRegressor", "value": "RandomForestRegressor"},
            {"label": "Ridge", "value": "Ridge"},
            {"label": "LinearRegression", "value": "LinearRegression"},
            {"label": "AdaBoostRegressor", "value": "AdaBoostRegressor"},
            {"label": "NeuralNetwork", "value": "NeuralNetwork"},
        ],
        "LinearRegression"
    ]
    
    return output



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
        [
            {"label": "MinMaxScaler", "value": "MinMaxScaler"},
            {"label": "StandardScaler", "value": "StandardScaler"},
            {"label": "RobustScaler", "value": "RobustScaler"},
            {"label": "Normalizer", "value": "Normalizer"},
            {"label": "QuantileTransformer", "value": "QuantileTransformer"},
            {"label": "PowerTransformer", "value": "PowerTransformer"},
            {"label": "MaxAbsScaler", "value": "MaxAbsScaler"},
            {"label": "None", "value": "None"},
            {"label": "", "value": ""},
        ],
        "MinMaxScaler"
    ]
    
    return output



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
        [

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
        ],
        "10 % test"
    ]
    
    return output





@dash.callback(
    [
        Output("model_parameters_loading", "children"),
    ],
    [
        Input("model_selection", "value"),
    ]
)
def update_model_parameters_loading(model_selection):
    output = [
        html.Div([
            html.P("Select a model to see its parameters"),
        ])
    ]
    
    return output





