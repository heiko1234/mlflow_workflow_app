
# landing page

import base64
import datetime
import io

import pandas as pd

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table

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
        html.Div([
            dcc.Tabs(id='data_tabs', value='tab_data_upload', children=[
                dcc.Tab(label='File Usage', value='tab_data_upload'),
                dcc.Tab(label='Blobstorage Usage', value='tab_data_load'),
            ]),
            html.Div(id='data_tabs_content'),
        ]),
    ]
)

# create the content of the tab_data_upload

tab_data_upload = html.Div([
    html.Div([
        dcc.Upload(
            id="upload_data",
            children=html.Div([
                "Drag and Drop or ",
                html.A("Select File")
            ]),
            style={
                "width": "25%",
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
])

# create the content of the tab_data_load, with a from to give basic information to chose a file from the blob storage and load it

tab_data_load = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Label("Container Name"),
                dcc.Input(
                    id="container_name",
                    type="text",
                    placeholder="Container Name",
                    value="data"
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Name"),
                dcc.Input(
                    id="file_name",
                    type="text",
                    placeholder="File Name",
                    value="data.csv"
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("Account Name"),
                dcc.Input(
                    id="account_name",
                    type="text",
                    placeholder="Account Name",
                    value="data"
                ),
            ], className="six columns"),
            html.Div([
                html.Label("Account Key"),
                dcc.Input(
                    id="account_key",
                    type="text",
                    placeholder="Account Key",
                    value="data"
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("SAS Token"),
                dcc.Input(
                    id="sas_token",
                    type="text",
                    placeholder="SAS Token",
                    value="data"
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Path"),
                dcc.Input(
                    id="file_path",
                    type="text",
                    placeholder="File Path",
                    value="data"
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("File Type"),
                dcc.Dropdown(
                    id="file_type",
                    options=[
                        {'label': 'csv', 'value': 'csv'},
                        {'label': 'xls', 'value': 'xls'},
                        {'label': 'parquet', 'value': 'parquet'},
                    ],
                    value='csv'
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Delimiter"),
                dcc.Input(
                    id="file_delimiter",
                    type="text",
                    placeholder="File Delimiter",
                    value=","
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("File Encoding"),
                dcc.Dropdown(
                    id="file_encoding",
                    options=[
                        {'label': 'utf-8', 'value': 'utf-8'},
                        {'label': 'latin-1', 'value': 'latin-1'},
                        {'label': 'iso-8859-1', 'value': 'iso-8859-1'},
                    ],
                    value='utf-8'
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Header"),
                dcc.Input(
                    id="file_header",
                    type="number",
                    placeholder="File Header",
                    value=0
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("File Footer"),
                dcc.Input(
                    id="file_footer",
                    type="number",
                    placeholder="File Footer",
                    value=0
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Sheet"),
                dcc.Input(
                    id="file_sheet",
                    type="number",
                    placeholder="File Sheet",
                    value=0
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("File Skip Rows"),
                dcc.Input(
                    id="file_skiprows",
                    type="number",
                    placeholder="File Skip Rows",
                    value=0
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Skip Footer"),
                dcc.Input(
                    id="file_skipfooter",
                    type="number",
                    placeholder="File Skip Footer",
                    value=0
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("File Compression"),
                dcc.Dropdown(
                    id="file_compression",
                    options=[
                        {'label': 'infer', 'value': 'infer'},
                        {'label': 'gzip', 'value': 'gzip'},
                        {'label': 'bz2', 'value': 'bz2'},
                        {'label': 'zip', 'value': 'zip'},
                        {'label': 'xz', 'value': 'xz'},
                        {'label': 'None', 'value': 'None'},
                    ],
                    value='infer'
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Decimal"),
                dcc.Input(
                    id="file_decimal",
                    type="text",
                    placeholder="File Decimal",
                    value="."
                ),
            ], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([
                html.Label("File Thousands"),
                dcc.Input(
                    id="file_thousands",
                    type="text",
                    placeholder="File Thousands",
                    value=","
                ),
            ], className="six columns"),
            html.Div([
                html.Label("File Date Format"),
                dcc.Input(
                    id="file_dateformat",
                    type="text",
                    placeholder="File Date Format",
                    value="%Y-%m-%d"
                ),
            ], className="six columns"),
        ], className="row"),
    ])
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





# layout = html.Div(
#     children=[
#         html.H1(children='This is our template page'),
#         html.Div(children='''
#             This is our landing page content.
#             '''),
#         html.Div([
#             dcc.Upload(
#                 id="upload_data",
#                 children=html.Div([
#                     "Drag and Drop or ",
#                     html.A("Select File")
#                 ]),
#                 style={
#                     "width": "25%",
#                     "height": "120px",
#                     "lineHeight": "60px",
#                     "borderWidth": "1px",
#                     "borderStyle": "dashed",
#                     "borderRadius": "5px",
#                     "textAlign": "center",
#                     "margin": "10px"
#                 },
#                 # Allo multiple files to be uploaded
#                 multiple=False
#             ),
#             html.Div(id="output_data_upload")
#         ])
#     ],
# )



# @dash.callback(
#     Output('output_data_upload', 'children'),
#     Input('upload_data', 'contents'),
#     State('upload_data', 'filename'),
#     State('upload_data', 'last_modified')
# )
# def update_output(list_of_contents, list_of_names, list_of_dates):

#     # print(list_of_contents)
#     # print(f"list_of_names: {list_of_names}")
#     # print(f"list_of_dates: {list_of_dates}")

#     if list_of_contents is not None:

#         output = [parse_contents(list_of_contents, list_of_names, list_of_dates)]

#     else:
#         output = None

#     return output



