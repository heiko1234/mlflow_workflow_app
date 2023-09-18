
# landing page

import base64
import datetime
import io

import pandas as pd

# from upath import UPath

import dash
from dash import ctx
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
from upath import UPath

from app.utilities.cards import (
    standard_card,
    form_card
)


from app.utilities.api_call_clients import APIBackendClient


dataclient=APIBackendClient()



dash.register_page(__name__,"/dataload")




def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            message = "csv"
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            message = "xls"
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))

        elif "parquet" in filename:
            message = "parquet"
            df = pd.read_parquet(io.BytesIO(decoded))


        dfa = df.head()


    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            dfa.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        # html.Hr(),  # horizontal line

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])





# layout with several tabs, tab1 contains the upload of files, tab2 contains the interaction with a azure blob storage to load one file from for the later analysis

layout = html.Div(
    id="dataload_page_content",
    className="dataload_page_content",
    children=[
        html.H1(children='Data'),
        html.Div(children='''
            Choose your data source.
            '''),
        html.H1(),
        html.Div(
            id="data_tabs_div",
            children=
                [
                    html.Div([
                        html.Div([
                            html.Div([
                                dcc.Tabs(id='data_tabs', value='tab_data_upload',
                                    children=[
                                        dcc.Tab(label='File Usage', value='tab_data_upload'),
                                        dcc.Tab(label='Blobstorage Usage', value='tab_data_load'),
                                    ],
                                    style={
                                        "display": "flex",
                                        "width": "500px",
                                        "align-items": "center",
                                        "justify-content": "center"
                                        }
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "align-items": "center",
                                    "justify-content": "center"
                                }
                            ),
                            html.Div(id='data_tabs_content'),
                            ],
                        ),
                        html.Div(children=[
                            html.Div([
                                standard_card(
                                    id="data_tabs_content_card",
                                    header_text="Example Data from Upload",
                                    content=[
                                        html.Div([
                                            html.Div(id="output_data_upload")
                                        ])
                                    ],
                                    height="500px",
                                    width="1000px"
                                )
                                ],
                            ),
                            html.Div([
                                standard_card(
                                    id="data_descriptive_card",
                                    header_text="Data Statistics",
                                    content=[
                                        html.Div([
                                            html.Div(id="data_descriptive")
                                        ])
                                    ],
                                    height="500px",
                                    width="1000px"
                                )
                            ])
                        ], style={"display": "flex", "justify-content": "center"}),
                    ],
                    style={
                        "display": "block",
                    }
                    )
                ],
            style={
                "display": "flex",
                "align-items": "center",
                "justify-content": "center"
            }
        )
    ]
)



# create the content of the tab_data_upload

tab_data_upload = html.Div([
    html.Div(
        className="blobdata_loading_div",
        children=
        [
        standard_card(
            id="upload_data_card",
            header_text="Drag and Drop your Data",
            width="600px",
            height="500px",
            content=[
                html.Div([
                    html.Div([
                        dcc.Upload(
                            id="upload_data",
                            children=html.Div(
                                [
                                    "Drag and Drop or ",
                                    html.A("Select File")
                                ]
                            ),
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
                            # Allo multiple files to be uploaded
                            multiple=False
                        ),
                    ],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center"
                        }
                    ),
                    html.Div([
                        # add download button for standard data for user testing
                        html.A(
                            html.Button(
                                "Download Example Data",
                                id="download_example_data_button",
                                style={
                                    "width": "250px",
                                    "height": "80px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px"
                                }
                            ),
                            # href="/sampledata/ChemicalManufacturingProcess.parquet",
                        ),
                        dcc.Download(id="download_example_data")
                    ],
                    style={
                        "display": "flex",
                        "align-items": "center",
                        "justify-content": "center"
                        }
                    )
                ]),
            ],
        )
    ])
])


tab_data_load = html.Div(
    className="blobdata_loading_div",   # id
    children=[
        html.Div(
            className="blobdata_loading_subdiv",
            children=[
                standard_card(
                    id="blobdatacard",
                    header_text="Blob Data Access",
                    content=[
                        html.Div(
                            [
                            html.Div([
                                html.H3("Blobstorage Environment", style={"margin": "10px", "width": "300px"}),
                                dcc.Dropdown(
                                    id="blobstorage_environment",
                                    style={"width": "400px"}
                                ),
                            ], className="six columns"),
                            html.Div([
                                html.H3("Container Name", style={"margin": "10px", "width": "300px"}),
                                dcc.Dropdown(
                                    id="container_name",
                                    style={"width": "400px"}
                                ),
                            ], className="six columns"),
                            html.Div([
                                html.H3("Subcontainer Name", style={"margin": "10px", "width": "300px"}),
                                dcc.Dropdown(
                                    id="subcontainer_name",
                                    style={"width": "400px"}
                                ),
                            ], className="six columns"),
                            html.Div([
                                html.H3("File Name", style={"margin": "10px", "width": "300px"}),
                                dcc.Dropdown(
                                    id="file_name",
                                    style={"width": "400px"}
                                ),
                            ], className="six columns"),
                        ],
                        ),
                    ],
                    height="500px",
                    width="600px"
                ),
            ],
            style={"display": "flex", "justify-content": "center"}
        )
])








# callback to show up tab_data_upload and tab_data_load when selecting the tab
@dash.callback(
    Output('data_tabs_content', 'children'),
    [Input('data_tabs', 'value')])
def render_content(tab):
    if tab == 'tab_data_upload':
        return tab_data_upload
    elif tab == 'tab_data_load':
        return tab_data_load



# @dash.callback(
#     [
#         Output('output_data_upload', 'children'),
#         Output("data_session_store", "data")
#     ],
#     [
#         Input('data_tabs', 'value'),
#         Input('upload_data', 'contents'),
#         Input('upload_data', 'filename'),
#         Input('upload_data', 'last_modified')
#     ]
# )
# def update_output(tab, content, list_of_names, list_of_dates):

#     button_triggered = ctx.triggered_id

#     if button_triggered == 'data_tabs':

#         output = None
#         df_json = None

#         return output, df_json

#     else:

#         if tab == 'tab_data_upload':

#             date = datetime.datetime.fromtimestamp(list_of_dates)
#             date = date.strftime("%m.%d.%Y %H:%M:%S")


#             content_type, content_string = content.split(',')
#             decoded = base64.b64decode(content_string)


#             # if csv file upload file to data_session_store

#             if "csv" in list_of_names:
#                 df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=";")

#             if "xls" in list_of_names:
#                 df = pd.read_excel(io.BytesIO(decoded))

#             if "xlsx" in list_of_names:
#                 df = pd.read_excel(io.BytesIO(decoded))

#             if "parquet" in list_of_names:
#                 df = pd.read_parquet(io.BytesIO(decoded))


#             output =  html.Div(
#                 children=[
#                     html.H3(list_of_names),
#                     html.H3(date),
#                     html.Hr(),  # horizontal line
#                     html.H1(),
#                     dash_table.DataTable(
#                         df.head().to_dict('records'),     #with or without head?
#                         [{'name': i, 'id': i} for i in df.columns],
#                         style_table={
#                             'overflowX': 'auto',
#                             "width": "900px",
#                             "height": "300px",
#                             },
#                         style_cell={
#                             # all three widths are needed
#                             'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
#                             'overflow': 'hidden',
#                             'textOverflow': 'ellipsis',
#                         }
#                     ),
#                 ],
#                 style={
#                     "justify-content": "center",
#                     }
#             )

#             df_json = df.to_json(date_format='iso', orient='split')

#             return output, df_json



# @dash.callback(
#     Output('data_descriptive', 'children'),
#     [
#         Input('data_session_store', 'data')
#     ]
# )
# def update_descriptive(df_json):
#     # load data from data_session_store and make pandas describe for output
#     if df_json is None:
#         return None
#     else:
#         df = pd.read_json(df_json, orient='split')

#         dft=df.describe().reset_index(drop = True).T
#         dft = dft.reset_index(drop=False)
#         dft.columns= ["description", "counts", "mean", "std", "min", "25%", "50%", "75%", "max"]
#         dft["nan"]=df.isna().sum().values

#         output_df=dft.round(2)

#         output = html.Div(
#             children=[
#                 html.H1(),
#                 dash_table.DataTable(
#                     output_df.to_dict('records'),
#                     [{'name': i, 'id': i} for i in output_df.columns],
#                     style_table={
#                         'overflowX': 'auto',
#                         "width": "900px",
#                         "height": "400px",
#                         },
#                     style_cell={
#                         # all three widths are needed
#                         'minWidth': '70px', 'width': '70px', 'maxWidth': '2500px',
#                         'overflow': 'hidden',
#                         'textOverflow': 'ellipsis',
#                     }
#                 ),
#             ],
#             style={
#                 "justify-content": "center",
#                 }
#         )

#     return output



# callback for the download of the ChemcialManufacturingProcess.parquet file

@dash.callback(
    Output("download_example_data", "data"),
    [
        Input("download_example_data_button", "n_clicks")
    ]
)
def download_example_data(n_clicks):

    if n_clicks is None:
        return None
    else:
        df = pd.read_parquet(UPath("sampledata/ChemicalManufacturingProcess.parquet"))
        return dcc.send_data_frame(df.to_parquet, "ChemicalManufacturingProcess.parquet")




# callback to populate the dropdowns for the blobstorage environment

@dash.callback(
    Output('blobstorage_environment', 'options'),
    [Input('blobstorage_environment', 'value')]
)
def populate_blobstorage_environment(value):

    headers = None
    endpoint = "list_available_accounts"


    response = dataclient.Backendclient.execute_get(
        headers=headers,
        endpoint=endpoint,
        )

    if response.status_code == 200:
        output = response.json()

        if isinstance(output, list):
            value = output
        else:
            value = [output]

    else:
        value = None
        output = None

    try:
        if value is not None:

            output = [
                {"label": i, "value": i} for i in value
            ]
    except Exception:
        output = None

    return output



@dash.callback(
    Output('container_name', 'options'),
    [
        Input('blobstorage_environment', 'value'),
        Input('container_name', 'value'),
    ]
)
def populate_blobstorage_container(blobstorage_environment, container_name):

    if blobstorage_environment is None:
        value = []

    else:

        headers = None
        endpoint = "list_available_blobs"


        data_statistics_dict = {
            "blobcontainer": None,
            "subcontainer": None,
            "file_name": None,
            "account": blobstorage_environment
        }



        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()

            if isinstance(output, list):
                value = output
            else:
                value = [output]

        else:
            value = None
            output = None

        # value = ["chemical-data", "model-container"]

    try:
        if value is not None:

            output = [
                {"label": i, "value": i} for i in value
            ]
    except Exception:
        output = None

    return output






@dash.callback(
    Output('subcontainer_name', 'options'),
    [
        Input('blobstorage_environment', 'value'),
        Input('container_name', 'value'),
        Input('subcontainer_name', 'value'),
    ]
)
def populate_subblobstorage_container(blobstorage_environment, container_name, subcontainer_name):


    if container_name is None:
        value = []

    else:
        headers = None
        endpoint = "list_available_subblobs"


        data_statistics_dict = {
            "blobcontainer": container_name,
            "subcontainer": None,
            "file_name": None,
            "account": blobstorage_environment
        }



        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()

            if isinstance(output, list):
                value = output
            else:
                value = [output]

        else:
            value = None
            output = None


    # value = ["chemical-data", "model-container"]

    try:
        if value is not None:

            output = [
                {"label": i, "value": i} for i in value
            ]
    except Exception:
        output = None

    return output





@dash.callback(
    Output('file_name', 'options'),
    [
        Input('blobstorage_environment', 'value'),
        Input('container_name', 'value'),
        Input('subcontainer_name', 'value'),
        Input('file_name', 'value'),
    ]
)
def populate_file_name(blobstorage_environment, container_name, subcontainer_name, file_name):


    value = None
    output = None

    if subcontainer_name is None:
        value = []

    else:
        headers = None
        endpoint = "list_available_files"

        data_statistics_dict = {
            "blobcontainer": container_name,
            "subcontainer": subcontainer_name,
            "file_name": None,
            "account": blobstorage_environment
        }


        response = dataclient.Backendclient.execute_post(
            headers=headers,
            endpoint=endpoint,
            json=data_statistics_dict
            )

        if response.status_code == 200:
            output = response.json()

            if isinstance(output, list):
                value = output
            else:
                value = [output]


    # value = ["ChemicalManufacturingProcess.parquet"]

    try:
        if value is not None:

            output = [
                {"label": i, "value": i} for i in value
            ]
    except Exception as e:
        print(f"populate_file_name: {e}")
        output = None

    return output




@dash.callback(
    Output('data_session_store', 'data'),
    [
        Input('file_name', 'value'),
        State('blobstorage_environment', 'value'),
        State('container_name', 'value'),
        State('subcontainer_name', 'value'),
    ]
)
def populate_data_sessionstore(file_name, blobstorage_environment, container_name, subcontainer_name, ):


    data_dict = {
        "blobcontainer": container_name,
        "subcontainer": subcontainer_name,
        "file_name": file_name,
        "account": blobstorage_environment
    }
    print(f"populate_data_sessionstore: {data_dict}")

    # data_dict = [data_dict]

    return data_dict



@dash.callback(
    Output('data_descriptive', 'children'),
    [
        Input('data_session_store', 'data')
    ]
)
def update_descriptive(data_dict):

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

        print("trigger update_descriptive done")
        print(f"update_descriptive: {response.status_code}")

        if response.status_code == 200:
            output = response.json()

            output_df = pd.read_json(output, orient='split')
            print(f"update_descriptive data head: {output_df.head()}")

            digits = 2
            output_df = output_df.round(digits)


            output = html.Div(
                children=[
                    html.H1(),
                    dash_table.DataTable(
                        output_df.to_dict('records'),
                        [{'name': i, 'id': i} for i in output_df.columns],
                        style_table={
                            'overflowX': 'auto',
                            "width": "900px",
                            "height": "400px",
                            },
                        style_cell={
                            # all three widths are needed
                            'minWidth': '70px', 'width': '70px', 'maxWidth': '2500px',
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




