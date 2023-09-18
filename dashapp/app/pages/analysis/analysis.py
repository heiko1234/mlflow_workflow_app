

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

from app.utilities.api_call_clients import APIBackendClient


dataclient=APIBackendClient()



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
    # prevent_initial_call=True,
)
def update_analysis_content(data_dict):
    """Update the content of the analysis card"""

    if data_dict is None:
        return None

    else:

        headers = None
        endpoint = "data_statistics"

        data_statistics_dict = {
            "blobcontainer": data_dict["blobcontainer"],
            "subcontainer": data_dict["subcontainer"],
            "file_name": data_dict["file_name"],
            "account": data_dict["account"]
        }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )


        if response.status_code == 200:
            output = response.json()

            output_df = pd.read_json(output, orient='split')

            digits = 2
            output_df = output_df.round(digits)

            dft = output_df

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

        else:
            return None




@dash.callback(
        [
            Output("dd_columns", "options"),
            Output("dd_columns", "value"),
        ],
    Input("data_session_store", "data"),
)
def update_dd_columns(data_dict):
    """Update the content of the analysis card"""

    if data_dict is None:
        return None

    else:

        headers = None
        endpoint = "data_columns"

        data_statistics_dict = {
            "blobcontainer": data_dict["blobcontainer"],
            "subcontainer": data_dict["subcontainer"],
            "file_name": data_dict["file_name"],
            "account": data_dict["account"]
        }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()

        columns = output

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
def update_analysisplot_card_content(data_dict, column, transformation):
    """Update the content of the analysis card"""

    if data_dict is None:
        return None

    else:

        headers = None
        endpoint = "data_series"

        data_statistics_dict = {
            "blobcontainer": data_dict["blobcontainer"],
            "subcontainer": data_dict["subcontainer"],
            "file_name": data_dict["file_name"],
            "account": data_dict["account"],
            "column_name": column
        }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()
            data = output
            # data = pd.read_json(output, orient='split')
            data = [float(data[i]) for i in data.keys()]
            data = pd.DataFrame(data=data, columns=[column])


        if column is None:
            return None
        else:
            if transformation == "no transformation":
                data = data[column]
            elif transformation == "log":
                data = data[column].apply(lambda x: np.log(x))
            elif transformation == "sqrt":
                data = data[column].apply(lambda x: np.sqrt(x))
            elif transformation == "1/x":
                data = data[column].apply(lambda x: 1/x)
            elif transformation == "x^2":
                data = data[column].apply(lambda x: x**2)
            elif transformation == "x^3":
                data = data[column].apply(lambda x: x**3)

        df = pd.DataFrame(data=data, columns=[column])

        fig = control_chart(
            data=df,
            y_name=column,
            xlabel= None,
            title = "Controlchart",
            lsl = None,
            usl = None,
            outliers = False,
            annotations = True,
            lines = True,
            nelson=False,
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





# with user selection for targer calculat the correlations and present in the analysis_table


# callback to update the data from analysis_table to analysis_table

@dash.callback(
    Output("analysis_table", "data"),
    [
        Input("analysis_table", "data"),
        State("data_session_store", "data"),
    ]
)
def update_target_analysis_table(data, data_dict):


    dd = pd.DataFrame(data=data)


    try:
        name_of_target = dd.loc[dd['usage'] == 'target']['description'].values[0]

    except BaseException:
        name_of_target = None


    if name_of_target is None:
        dd['correlation'] = None

    else:
        headers = None
        endpoint = "data_target_correlation"

        data_statistics_dict = {
            "blobcontainer": data_dict["blobcontainer"],
            "subcontainer": data_dict["subcontainer"],
            "file_name": data_dict["file_name"],
            "account": data_dict["account"],
            "column_name": name_of_target
        }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()
            data = output

        dd['correlation'] = data


    output = dd.to_dict('records')

    return output




# callback to etract the target and the selected features from the analysis_table to sessionstore project_target_feature_session_store

@dash.callback(
    Output("project_target_feature_session_store", "data"),
    Input("analysis_table", "data"),
)
def update_project_target_feature_session_store(data):

    dd = pd.DataFrame(data=data)

    try:
        name_of_target = dd.loc[dd['usage'] == 'target']['description'].values[0]

    except BaseException:
        name_of_target = None

    try:
        name_of_features = list(dd.loc[dd['usage'] == 'feature']['description'].values)

    except BaseException:
        name_of_features = None

    output_dict = {"target": name_of_target, "features": name_of_features}

    return output_dict















