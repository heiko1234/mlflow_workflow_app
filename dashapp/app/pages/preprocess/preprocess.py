

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
    control_chart_marginal
)

from app.utilities.spc import (
    transform_cleaning_table_in_dict,
    use_spc_cleaning_dict,
    create_limits_dict,
    update_nested_dict,
    filter_dataframe_by_limits
)



dash.register_page(__name__,"/preproces")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(
    id="preprocessing_page_content",
    className="analysis_page_content",
    children=[
        html.H1(children='Data Preprocessing'),
        html.Div(
            className="preprocessing_page_subcontent",
            children=[
                standard_card(
                    id="preprocessing_card",
                    header_text="Data Preprocessing",
                    content=
                    [
                        html.Div(
                            [
                                html.Div(id="preprocessing_card_content")
                            ]
                        )
                    ],
                    height="700px",
                    width="1700px",
                ),
                standard_card(
                    id="preprocessing_card_table",
                    header_text="Data Cleaning via SPC",
                    content=[
                        html.Div(
                            [
                                html.Div(id="preprocessing_card_table_content")
                            ]
                        )
                    ],
                    height="400px",
                    width="1900px",
                ),
                standard_card(
                    id="preprocessing_card_cleaned_data",
                    header_text="Cleaned Data",
                    content=[
                        html.Div(
                            [
                                html.Div(id="preprocessing_card_cleaned_data_content")
                            ]
                        )
                    ],
                    height="700px",
                    width="1700px",
                )
            ]
        ),
    ]
)




# callback to create preprocessing_card_content

@dash.callback(
    Output("preprocessing_card_content", "children"),
    Input("project_target_feature_session_store", "data"),
)
def create_preprocessing_card_content(target_feature):
    
    # print(f"create_preprocessing_card_content")
    
    if target_feature is None or len(target_feature) == 0:
        print(f"create_preprocessing_card_content: target_feature is None")
        return html.Div(
            [
                html.H3("Please select a target feature in the Analysis page.")
            ]
        )
    else:
        # read data from target_feature

        dict_target_feature = target_feature

        dd_list = []
        dd_list.append(dict_target_feature["target"])
        dd_list.extend(dict_target_feature["features"])

        # create a div with a dropdown list
        return html.Div(
            [
                dcc.Dropdown(
                    id="preprocessing_card_content_dropdown",
                    options=[{"label": i, "value": i} for i in dd_list],
                    value=dict_target_feature["target"],
                    style={"width": "250px"},
                ),
                html.Div(id="preprocessing_card_content_output"),
            ]
        )



@dash.callback(
    Output("preprocessing_card_content_output", "children"),
    Input("preprocessing_card_content_dropdown", "value"),
    State("project_target_feature_session_store", "data"),
    State("data_session_store", "data"),
)
def create_preprocessing_card_content_output(
    selected_feature, target_feature_dict, data
):
    # print(f"create_preprocessing_card_content_output: selected_feature={selected_feature}")
    
    if selected_feature is None:
        return html.Div(
            [
                html.H3("Please select a feature in the dropdown list.")
            ]
        )
    else:
        
        # list_of_features_and_target
        dd_list = []
        dd_list.append(target_feature_dict["target"])
        dd_list.extend(target_feature_dict["features"])
        
        # read data from data_session_store
        df = pd.read_json(data, orient="split")

        df = df[dd_list]
        df = pd.DataFrame(df[selected_feature])


        fig = control_chart_marginal(
            data=df,
            y_name=selected_feature,
            xlabel= None,
            title = "Controlchart",
            lsl = None,
            usl = None,
            outliers = True,
            annotations = True,
            lines = True,
            nelson=True,
            mean = None,
            sigma = None,
            markersize = 6,
            show=False)


        output = dcc.Graph(
            id="analysisplot",
            figure=fig,
            style={
                "width": "1600px",
                "height": "650px",
                "justify-content": "center",
                }
        )

        return output





# callback to create preprocessing_card_table_content

@dash.callback(
    Output("preprocessing_card_table_content", "children"),
    Input("project_target_feature_session_store", "data"),
    State("data_session_store", "data"),
)
def create_preprocessing_card_table_content(target_feature, data):
    
    # print(f"create_preprocessing_card_table_content")
    
    if target_feature is None or len(target_feature) == 0:
        print(f"create_preprocessing_card_table_content: target_feature is None")
        return html.Div(
            [
                html.H3("Please select a target feature in the Analysis page.")
            ]
        )
    else:
        # read data from target_feature
        dict_target_feature = target_feature

        dd_list = []
        dd_list.append(dict_target_feature["target"])
        dd_list.extend(dict_target_feature["features"])

        # read data from data_session_store
        df = pd.read_json(data, orient="split")

        df = df[dd_list]


        dft=df.describe().reset_index(drop = True).T
        dft = dft.reset_index(drop=False)
        dft.columns= ["description", "counts", "mean", "std", "min", "25%", "50%", "75%", "max"]
        dft["nan"]=df.isna().sum().values
        
        dft = dft.drop(["25%", "50%", "75%"], axis=1)
        
        dft["rule1"] = "no cleaning"
        dft["rule2"] = "no cleaning"
        dft["rule3"] = "no cleaning"
        dft["rule4"] = "no cleaning"
        dft["rule5"] = "no cleaning"
        dft["rule6"] = "no cleaning"
        dft["rule7"] = "no cleaning"
        dft["rule8"] = "no cleaning"


        dft["transformation"] = "no transformation"


        data_transformations = [
            {"label": "no transformation", "value": "no transformation"},
            {"label": "log", "value": "log"},
            {"label": "sqrt", "value": "sqrt"},
            {"label": "1/x", "value": "1/x"},
            {"label": "x^2", "value": "x^2"},
            {"label": "x^3", "value": "x^3"},
        ]
        
        spc_rules = [
            {"label": "no cleaning", "value": "no cleaning"},
            {"label": "remove data", "value": "remove data"},
        ]
        
        dft["usage"] = "feature"
        
        # for target, comming from dict_target_feature["target"], usage = "target" in dft table, column usage
        # dft.loc[dft["usage"] == dict_target_feature["target"]] = "target"
        # f.set_value('C', 'x', 10), 
        index_target_in_table = dft[dft["description"] == dict_target_feature["target"]].index[0]
        # dft.set_value(index_target_in_table, "usage", "target")
        dft.loc[index_target_in_table, "usage"] = "target"



        dft = dft.loc[:, ["description", "usage", "transformation", "counts", "mean", "std", "min", "max", "nan", "rule1", "rule2", "rule3", "rule4", "rule5", "rule6", "rule7", "rule8"]]


        # create dropdown columns
        dropdown_columns = ["transformation", "rule1", "rule2", "rule3", "rule4", "rule5", "rule6", "rule7", "rule8"]

        colums_options = []
        for i in dft.columns:
            if i not in dropdown_columns:
                colums_options.append({'name': i, 'id': i})
            elif i == "transformation":
                colums_options.append({'id': 'transformation', 'name': 'transformation', 'presentation': 'dropdown'})
            elif i == "rule1":
                colums_options.append({'id': 'rule1', 'name': 'rule1', 'presentation': 'dropdown'})
            elif i == "rule2":
                colums_options.append({'id': 'rule2', 'name': 'rule2', 'presentation': 'dropdown'})
            elif i == "rule3":
                colums_options.append({'id': 'rule3', 'name': 'rule3', 'presentation': 'dropdown'})
            elif i == "rule4":
                colums_options.append({'id': 'rule4', 'name': 'rule4', 'presentation': 'dropdown'})
            elif i == "rule5":
                colums_options.append({'id': 'rule5', 'name': 'rule5', 'presentation': 'dropdown'})
            elif i == "rule6":
                colums_options.append({'id': 'rule6', 'name': 'rule6', 'presentation': 'dropdown'})
            elif i == "rule7":
                colums_options.append({'id': 'rule7', 'name': 'rule7', 'presentation': 'dropdown'})
            elif i == "rule8":
                colums_options.append({'id': 'rule8', 'name': 'rule8', 'presentation': 'dropdown'})




        # round numbers in dft table
        
        dft["mean"] = dft["mean"].apply(lambda x: round(x, 2))
        dft["std"] = dft["std"].apply(lambda x: round(x, 2))
        dft["min"] = dft["min"].apply(lambda x: round(x, 2))
        dft["max"] = dft["max"].apply(lambda x: round(x, 2))


        table = dash_table.DataTable(
            id="preprocessing_table",
            columns=colums_options,
            data=dft.to_dict('records'),
            editable=True,
            dropdown={
                'transformation': {
                    'options': data_transformations
                },
                'rule1': {
                    'options': spc_rules
                },
                'rule2': {
                    'options': spc_rules
                },
                'rule3': {
                    'options': spc_rules
                },
                'rule4': {
                    'options': spc_rules
                },
                'rule5': {
                    'options': spc_rules
                },
                'rule6': {
                    'options': spc_rules
                },
                'rule7': {
                    'options': spc_rules
                },
                'rule8': {
                    'options': spc_rules
                },
            },
            style_cell={
                'textAlign': 'center',
                'minWidth': '75px', 'width': '75px', 'maxWidth': '250px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_table={
                'maxHeight': '500px',
                'overflowY': 'scroll'
            },
        )
        
        output = html.Div(
            children=[
                html.H2(),
                table
            ],
            style={
                "width": "1800px",
                "height": "350px",
                "justify-content": "center",
                }
        )
        
        return output



# callback to use preprocessing_card_table to save spc rules data preprocessing in session store 

@dash.callback(
    [
        Output("project_data_spc_cleaning_session_store", "data"),
        Output("project_data_limits_session_store", "data"),
    ],
    Input("preprocessing_table", "data"),
)
def save_spc_rules_in_session_store(data):

    # read data from table
    # df = pd.read_json(data, orient="split")
    df = pd.DataFrame(data)
    
    print(f"save_spc_rules_in_session_store: df: {df}")
    print("##### update #####")

    spc_cleaning_dict = transform_cleaning_table_in_dict(df)
    
    # limits_dict = create_limits_dict(df)
    limits_dict= []
    
    # print(f"save_spc_rules_in_session_store: spc_cleaning_dict: {spc_cleaning_dict}")
    
    return spc_cleaning_dict, limits_dict


# callback to use preprocessing_card_table to save limits in


# @dash.callback(
#     Output("project_data_limits_session_store", "data"),
#     Input("preprocessing_table", "data"),
# )
# def save_limits_in_session_store(data):
#     print("save_limits_in_session_store_callback")
#     # read data from table
#     # df = pd.read_json(data, orient="split")
#     df = pd.DataFrame(data)
    
#     limits_dict = create_limits_dict(df)
    
#     print(f"save_limits_in_session_store: limits_dict: {limits_dict}")
    
#     return limits_dict



# create plot of preprocessed, so cleaned data by limits and spc rules

@dash.callback(
    Output("preprocessing_card_cleaned_data_content", "children"),
    Input("project_target_feature_session_store", "data"),
)
def create_plot_preprocessed_data(target_feature):
    
    
    
    if target_feature is None or len(target_feature) == 0:
        print(f"create_preprocessing_card_content: target_feature is None")
        return html.Div(
            [
                html.H3("Please select a target feature in the Analysis page.")
            ]
        )
    else:
        # read data from target_feature

        dict_target_feature = target_feature

        dd_list = []
        dd_list.append(dict_target_feature["target"])
        dd_list.extend(dict_target_feature["features"])
        
        dd_options = [{"label": i, "value": i} for i in dd_list]


    output = html.Div(
        children=[
            html.H2(),
            dcc.Dropdown(
                id="preprocessing_card_cleaned_data_dropdown",
                options=dd_options,
                value=dict_target_feature["target"],
                style={
                    "width": "300px",
                }
            ),
            dcc.Loading(
                id="preprocessing_card_cleaned_data_loading",
            )
        ]
    )
    
    return output


# additional callback to populate the preprocessing_card_cleaned_data_loading with the plot

@dash.callback(
    Output("preprocessing_card_cleaned_data_loading", "children"),
    Input("project_target_feature_session_store", "data"),
    Input("preprocessing_card_cleaned_data_dropdown", "value"),
    Input("project_data_spc_limit_cleaning_session_store", "data"),
    Input("project_data_spc_cleaning_session_store", "data"),
    State("data_session_store", "data"),
)
def create_plot_preprocessed_data(dict_target_feature, selected_feature, limits_dict, spc_cleaning_dict, data):
    
    # read data from data_table_session_store
    
    if data is None or len(data) == 0:
        print(f"create_plot_preprocessed_data: data is None")
        return html.Div(
            [
                html.H3("Please select a target feature in the Analysis page.")
            ]
        )
    else:
        # read data 
        # read data from data_session_store
        df = pd.read_json(data, orient="split")



        dd_list = []
        dd_list.append(dict_target_feature["target"])
        dd_list.extend(dict_target_feature["features"])

        output_df = df[dd_list]
        
        
        # print(f"create_plot_preprocessed_data: spc_cleaning_dict: {spc_cleaning_dict}")
        # print(f"create_plot_preprocessed_data: limits_dict: {limits_dict}")

        
        # # filter data by spc and limits
        if spc_cleaning_dict is not None :
            output_df = use_spc_cleaning_dict(output_df, spc_cleaning_dict)
        if limits_dict is not None:
            output_df = filter_dataframe_by_limits(output_df, limits_dict)

        
        df = pd.DataFrame(output_df[selected_feature])

        fig = control_chart(
            data=output_df,
            y_name=selected_feature,
            xlabel= None,
            title = "Controlchart",
            lsl = None,
            usl = None,
            outliers = True,
            annotations = True,
            lines = True,
            nelson=True,
            mean = None,
            sigma = None,
            markersize = 6,
            show=False)


        output = dcc.Graph(
            id="preprocessing_card_cleaned_data_loading_analysisplot",
            figure=fig,
            style={
                "width": "1600px",
                "height": "650px",
                "justify-content": "center",
                }
        )

        return output














