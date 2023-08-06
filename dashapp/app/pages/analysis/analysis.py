

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



dash.register_page(__name__,"/analysis")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(
    id="analysis_page_content",
    className="analysis_page_content",
    children=[
        html.H1(children='Analysis'),
        html.Div(
            className="analysis_page_subcontent",
            children=[
                standard_card(
                    id="analysiscard",
                    header_text="Choose and Analyse the Data",
                    content=[
                        html.Div(
                            [
                                html.Div(id="analysis_card_content"),
                            ],
                        )
                    ],
                    height="400px",
                    width="1700px",
                ),
            ]
        ),
        html.Div(
            className="analysis_page_subcontent",
            children=[
                standard_card(
                    id="analysisplotcard",
                    header_text="Plot of Data",
                    content=[
                        html.Div([
                            html.Div([
                                # dropdown with columns
                                dcc.Dropdown(id="dd_columns", style={"width": "200px"}),
                                dcc.Dropdown(id="dd_transformation", style={"width": "200px"}),
                                ],
                                style={"display": "flex"}
                            ),
                            html.Div(
                                [
                                    dcc.Loading(id="analysisplot_card_content"),
                                ],
                                style={
                                    "justify-content": "center",
                                    "align-items": "center",
                                    "display": "flex"
                                }
                            )
                        ])
                    ],
                    height="700px",
                    width="1700px",
                ),
            ]
        ),
    ]
)




@dash.callback(
    Output("analysis_card_content", "children"),
    Input("data_session_store", "data"),
)
def update_analysis_content(df_json):
    """Update the content of the analysis card"""

    if df_json is None:
        return None
    else:
        df = pd.read_json(df_json, orient='split')


        dft=df.describe().reset_index(drop = True).T
        dft = dft.reset_index(drop=False)
        dft.columns= ["description", "counts", "mean", "std", "min", "25%", "50%", "75%", "max"]
        dft["nan"]=df.isna().sum().values

        dft["usage"] = "no usage"
        dft["transformation"] = "no transformation"
        
        dft["correlation"]=None

        dft=dft.round(2)

        # output_df=dft[["description", "usage", "transformation", "correlation", "counts", "mean", "std", "min", "25%", "50%", "75%", "max", "nan"]]
        output_df=dft[["description", "usage", "correlation", "counts", "mean", "std", "min", "25%", "50%", "75%", "max", "nan"]]


        usage_options = [
            {"label": "no usage", "value": "no usage"},
            {"label": "target", "value": "target"},
            {"label": "feature", "value": "feature"},
            ]

        data_transformations = [
            {"label": "no transformation", "value": "no transformation"},
            {"label": "log", "value": "log"},
            {"label": "sqrt", "value": "sqrt"},
            {"label": "1/x", "value": "1/x"},
            {"label": "x^2", "value": "x^2"},
            {"label": "x^3", "value": "x^3"},
        ]


        dropdown_columns = ["usage", "transformation"]

        colums_options = []
        for i in output_df.columns:
            if i not in dropdown_columns:
                colums_options.append({'name': i, 'id': i})
            elif i == "usage":
                colums_options.append({'id': 'usage', 'name': 'usage', 'presentation': 'dropdown'})
            elif i == "transformation":
                colums_options.append({'id': 'transformation', 'name': 'transformation', 'presentation': 'dropdown'})

        output = html.Div(
            children=[
                html.H1(),
                dash_table.DataTable(
                    # header of datatable fix when scrolling
                    id="analysis_table",
                    editable=True,
                    data=output_df.to_dict('records'),
                    columns=colums_options,
                    dropdown={
                        'usage':
                            {"options": usage_options},
                        'transformation':
                            {"options": data_transformations},
                    },
                    fixed_rows={'headers': True},
                    style_table={
                        'overflowX': 'auto',
                        "width": "1600px",
                        "height": "300px",
                        },
                    style_cell={
                        # all three widths are needed
                        'minWidth': '70px', 'width': '70px', 'maxWidth': '250px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                    }
                ),
            ],
            style={
                "justify-content": "center",
                }
        )

    return output


@dash.callback(
        [
            Output("dd_columns", "options"),
            Output("dd_columns", "value"),
        ],
    Input("data_session_store", "data"),
)
def update_dd_columns(df_json):
    """Update the content of the analysis card"""

    if df_json is None:
        return None
    else:
        df = pd.read_json(df_json, orient='split')

        columns = df.columns

        options = []
        for i in columns:
            options.append({"label": i, "value": i})

        first_value = columns[0]

        return options, first_value


@dash.callback(
    [
        Output("dd_transformation", "options"),
        Output("dd_transformation", "value"),
    ],
    Input("data_session_store", "data"),
)
def update_dd_transformation(df_json):
    data_transformations = [
            {"label": "no transformation", "value": "no transformation"},
            {"label": "log", "value": "log"},
            {"label": "sqrt", "value": "sqrt"},
            {"label": "1/x", "value": "1/x"},
            {"label": "x^2", "value": "x^2"},
            {"label": "x^3", "value": "x^3"},
        ]

    first_value = "no transformation"

    return data_transformations, first_value



# analysisplot_card_content

@dash.callback(
    Output("analysisplot_card_content", "children"),
    Input("data_session_store", "data"),
    Input("dd_columns", "value"),
    Input("dd_transformation", "value"),
)
def update_analysisplot_card_content(df_json, column, transformation):
    """Update the content of the analysis card"""

    if df_json is None:
        return None
    else:
        df = pd.read_json(df_json, orient='split')

        if column is None:
            return None
        else:
            if transformation == "no transformation":
                data = df[column]
            elif transformation == "log":
                data = df[column].apply(lambda x: np.log(x))
            elif transformation == "sqrt":
                data = df[column].apply(lambda x: np.sqrt(x))
            elif transformation == "1/x":
                data = df[column].apply(lambda x: 1/x)
            elif transformation == "x^2":
                data = df[column].apply(lambda x: x**2)
            elif transformation == "x^3":
                data = df[column].apply(lambda x: x**3)

        df = pd.DataFrame(data=data, columns=[column])


        fig = control_chart(
            data=df,
            y_name=column,
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
        
        # fig = control_chart_marginal(
        #     data=df,
        #     y_name=column,
        #     xlabel= None,
        #     title = "Controlchart",
        #     lsl = None,
        #     usl = None,
        #     outliers = True,
        #     annotations = True,
        #     lines = True,
        #     nelson=True,
        #     mean = None,
        #     sigma = None,
        #     markersize = 6,
        #     show=False)


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





# with user selection for targer calculat the correlations and present in the analysis_table


# callback to update the data from analysis_table to analysis_table

@dash.callback(
    Output("analysis_table", "data"),
    [
        Input("analysis_table", "data"),
        State("data_session_store", "data"),
    ]
)
def update_target_analysis_table(data, df_json):


    dd = pd.DataFrame(data=data)
    
    # print(f"analysis_table1: {dd.head()}")
    
    try:

        name_of_target = dd.loc[dd['usage'] == 'target']['description'].values[0]

        # print(f"name_of_target: {name_of_target}")
        
    except BaseException:
        name_of_target = None

    # get data from data_session_store
    if df_json is not None:
        df = pd.read_json(df_json, orient='split')
        # print(f"session store: {df}")
        
    # TODO: info for data transformation sahould be sed for correlation calculation


    # calculate correlations for name_of_target and ignore if column may contains none values use numpy corrcoef
    
    if name_of_target is not None:
    
        correlations = []
        for i in df.columns:
            if i != name_of_target:
                corr = np.corrcoef(df[name_of_target], df[i])[0, 1]
                correlations.append(corr)
            else:
                correlations.append(1)

        # print(f"correlations: {correlations}")
        # print(f"len of correlations: {len(correlations)}")
        # print(f"analysis_table before2: {dd.head()}")
        # print(f"len of analysis_table before: {len(dd)}")

        # round all values in list correlation to  4 digits
        correlations = [round(i, 4) for i in correlations]

        dd['correlation'] = correlations
        
    else:
        dd['correlation'] = None

    # print(f"update_target_analysis_table analysis_table3: {dd.head()}")

    output = dd.to_dict('records')

    return output




# callback to etract the target and the selected features from the analysis_table to sessionstore project_target_feature_session_store

@dash.callback(
    Output("project_target_feature_session_store", "data"),    
    Input("analysis_table", "data"),
)
def update_project_target_feature_session_store(data):
    
    dd = pd.DataFrame(data=data)
    
    # print(f"analysis_table1: {dd.head()}")
    
    try:

        name_of_target = dd.loc[dd['usage'] == 'target']['description'].values[0]

        # print(f"name_of_target: {name_of_target}")
        
    except BaseException:
        name_of_target = None

    try:
        name_of_features = list(dd.loc[dd['usage'] == 'feature']['description'].values)
        
    except BaseException:
        name_of_features = None

    output_dict = {"target": name_of_target, "features": name_of_features}
    
    # print(f"update_project_target_feature_session_store: {output_dict}")
    
    return output_dict















