
# landing page

import base64
import datetime
import io

import pandas as pd

# from upath import UPath

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table

from app.utilities.cards import (
    standard_card,
    form_card
)




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
                dcc.Tabs(id='data_tabs', value='tab_data_upload',
                    children=[
                        dcc.Tab(label='File Usage', value='tab_data_upload'),
                        dcc.Tab(label='Blobstorage Usage', value='tab_data_load'),
                    ]),
                html.Div(id='data_tabs_content'),
                html.Div(id="output_data_upload")
                ]
        ),
    ]
)

# create the content of the tab_data_upload

tab_data_upload = html.Div([
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
        html.Div(id="output_data_upload")
    ])
], style={"display": "flex", "justify-content": "center"}
)


tab_data_load = html.Div(
    id="blobdata_loading_div",
    children=[
        html.Div(
            id="blobdata_loading_subdiv",
            children=[
                standard_card(
                    id="blobdatacard",
                    header_text="Blob Data Access",
                    content=[
                        html.Div([
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
                        ]),
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



@dash.callback(
    Output('output_data_upload', 'children'),
    [
        Input('data_tabs', 'value'),
        Input('upload_data', 'filename'),
        Input('upload_data', 'last_modified')
    ]
)
def update_output(tab, list_of_names, list_of_dates):

    if tab == 'tab_data_upload':

        date = datetime.datetime.fromtimestamp(list_of_dates)
        date = date.strftime("%m.%d.%Y %H:%M:%S")



        # if "csv" in list_of_names:
        #     df = 
        # elif "xls" in list_of_names:
        #     df
        # elif "xlsx" in list_of_names:
        #     df
        # elif "parquet" in list_of_names:


        output =  html.Div(
            children=[
                html.H3(list_of_names),
                html.H3(date),
                html.Hr(),  # horizontal line
                html.H1(),
                # dash_table.DataTable(
                #     df.to_dict('records'),
                #     [{'name': i, 'id': i} for i in df.columns]
                # ),
            ]
        )

        return output








# callback to populate the dropdowns for the blobstorage environment

# @dash.callback(
#     Output('blobstorage_environment', 'options'),
#     [Input('blobstorage_environment', 'value')]
# )
# def populate_blobstorage_environment(value):
#     # if value is None:
        
#     # else:
#     #     return [
#     #         {"label": "blobstorage_environment_1", "value": "blobstorage_environment_1"},
#     #     ]

