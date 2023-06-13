
# landing page

import base64
import datetime
import io

import pandas as pd

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table

dash.register_page(__name__,"/landing")




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




layout = html.Div(
    children=[
        html.H1(children='This is our template page'),
        html.Div(children='''
            This is our landing page content.
            '''),
        html.Div([
            dcc.Upload(
                id="upload_data",
                children=html.Div([
                    "Drag and Drop or ",
                    html.A("Select File")
                ]),
                style={
                    "width": "25%",
                    "height": "60px",
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
    ],
)



@dash.callback(
    Output('output_data_upload', 'children'),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
    State('upload_data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):

    # print(list_of_contents)
    # print(f"list_of_names: {list_of_names}")
    # print(f"list_of_dates: {list_of_dates}")

    if list_of_contents is not None:

        output = [parse_contents(list_of_contents, list_of_names, list_of_dates)]

    else:
        output = None

    return output



